"""Demo server with PostgreSQL integration for scalable meal planning"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.gmm_model import GMMMealRecommender
from backend.database import PostgreSQLManager
import pandas as pd
import numpy as np
import joblib
import random
from datetime import datetime

class NutriWiseDemoHandler(BaseHTTPRequestHandler):
    # Class variables to maintain state across requests
    _db_manager = None
    _model = None
    _last_recommendations = {}
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize database and model only once
        if NutriWiseDemoHandler._db_manager is None:
            self._initialize_database_and_model()
    
    def _initialize_database_and_model(self):
        """Initialize PostgreSQL database and GMM model"""
        try:
            # Initialize PostgreSQL manager
            NutriWiseDemoHandler._db_manager = PostgreSQLManager()
            
            # Create tables if they don't exist
            NutriWiseDemoHandler._db_manager.create_tables()
            
            # Check if data exists, if not migrate from Excel
            meals_df = NutriWiseDemoHandler._db_manager.get_meals()
            if meals_df.empty:
                excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'meal_data.xlsx')
                if os.path.exists(excel_path):
                    NutriWiseDemoHandler._db_manager.migrate_excel_to_postgres(excel_path)
                    print(f"✅ Migrated meal data from {excel_path} to PostgreSQL")
                else:
                    print(f"⚠️  Excel file not found at {excel_path}")
            
            # Initialize and train GMM model
            NutriWiseDemoHandler._model = GMMMealRecommender(n_components=8, random_state=42)
            
            # Load or train the model
            model_path = 'gmm_model.pkl'
            try:
                NutriWiseDemoHandler._model.load_model(model_path)
                print("✅ Loaded existing GMM model")
            except:
                # Train the model with data from PostgreSQL
                clustering_df = NutriWiseDemoHandler._db_manager.get_meals_for_clustering()
                if not clustering_df.empty:
                    features = clustering_df[['calories_kcal', 'protein_g', 'fat_g', 'carbohydrates_g']]
                    NutriWiseDemoHandler._model.fit(features)
                    NutriWiseDemoHandler._model.save_model(model_path)
                    print("✅ Trained and saved new GMM model")
                else:
                    print("⚠️  No meal data available for training GMM model")
                    
        except Exception as e:
            print(f"❌ Error initializing database and model: {e}")
            # Fallback to Excel-based approach
            self._fallback_to_excel()
    
    def _fallback_to_excel(self):
        """Fallback to Excel-based meal data when PostgreSQL is not available"""
        try:
            NutriWiseDemoHandler._model = GMMMealRecommender(n_components=8, random_state=42)
            excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'meal_data.xlsx')
            
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                features = df[['Calories (kcal)', 'Protein (g)', 'Fat (g)', 'Carbohydrates (g)']]
                NutriWiseDemoHandler._model.fit(features)
                print("✅ Fallback: Using Excel data for GMM model")
            else:
                print(f"❌ Excel file not found at {excel_path}")
        except Exception as e:
            print(f"❌ Fallback initialization failed: {e}")

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_json_response({
                "message": "NutriWise Demo API v2.0 - Enhanced with Modern Stack",
                "status": "running",
                "endpoints": ["/", "/health", "/recommendations"]
            })
        elif self.path == '/health':
            self.send_json_response({"status": "healthy", "version": "2.0.0-demo"})
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/recommendations':
            self._handle_recommendations()
        else:
            self.send_error(404, "Endpoint not found")
    
    def _handle_recommendations(self):
        """Handle meal recommendation requests with improved clustering"""
        try:
            # Read request data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract user profile
            age = data.get('age', 25)
            weight = data.get('weight', 70)
            height = data.get('height', 170)
            gender = data.get('gender', 'male')
            activity_level = data.get('activityLevel', 'moderate')
            goal = data.get('goal', 'maintain')
            dietary_preference = data.get('dietaryPreference', 'mixed')
            
            # Calculate daily calories
            daily_calories = self._calculate_daily_calories(age, weight, height, gender, activity_level, goal)
            
            # Generate meal recommendations
            if dietary_preference.lower() == 'vegetarian':
                recommendations = self._get_vegetarian_meals(daily_calories)
            else:
                recommendations = self._get_mixed_meals(daily_calories)
            
            # Add timestamp to ensure different recommendations
            recommendations['generated_at'] = datetime.now().isoformat()
            recommendations['daily_calories'] = daily_calories
            
            self.send_json_response(recommendations)
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            self.send_json_response({
                "error": "Failed to generate meal recommendations",
                "details": str(e)
            }, status_code=500)

    def send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def _calculate_daily_calories(self, age: int, weight: float, height: float, gender: str, activity_level: str, goal: str) -> float:
        """Calculate daily calorie needs based on user profile"""
        # Calculate BMR using Mifflin-St Jeor Equation
        if gender.lower() == 'male':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        
        # Activity multipliers
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        # Calculate TDEE
        tdee = bmr * activity_multipliers.get(activity_level.lower(), 1.55)
        
        # Adjust for goal
        goal_multipliers = {
            'lose': 0.8,
            'maintain': 1.0,
            'gain': 1.2
        }
        
        daily_calories = tdee * goal_multipliers.get(goal.lower(), 1.0)
        return round(daily_calories, 2)
    
    def _get_vegetarian_meals(self, daily_calories: float) -> Dict[str, Any]:
        """Generate vegetarian meal recommendations using GMM clustering"""
        try:
            # Try PostgreSQL first
            if NutriWiseDemoHandler._db_manager:
                meals_df = NutriWiseDemoHandler._db_manager.get_meals_for_clustering('Vegetarian')
                if not meals_df.empty:
                    return self._generate_clustered_meals(meals_df, daily_calories, 'vegetarian')
            
            # Fallback to Excel
            return self._generate_excel_based_meals(daily_calories, 'vegetarian')
            
        except Exception as e:
            print(f"❌ Error generating vegetarian meals: {e}")
            return self._generate_fallback_meals(daily_calories, 'vegetarian')
    
    def _get_mixed_meals(self, daily_calories: float) -> Dict[str, Any]:
        """Generate mixed diet meal recommendations using GMM clustering"""
        try:
            # Try PostgreSQL first
            if NutriWiseDemoHandler._db_manager:
                meals_df = NutriWiseDemoHandler._db_manager.get_meals_for_clustering()
                if not meals_df.empty:
                    return self._generate_clustered_meals(meals_df, daily_calories, 'mixed')
            
            # Fallback to Excel
            return self._generate_excel_based_meals(daily_calories, 'mixed')
            
        except Exception as e:
            print(f"❌ Error generating mixed meals: {e}")
            return self._generate_fallback_meals(daily_calories, 'mixed')
    
    def _generate_clustered_meals(self, meals_df: pd.DataFrame, daily_calories: float, diet_type: str) -> Dict[str, Any]:
        """Generate meals using GMM clustering with randomization for different results"""
        try:
            # Prepare features for clustering
            features = meals_df[['calories_kcal', 'protein_g', 'fat_g', 'carbohydrates_g']].fillna(0)
            
            # Use GMM model to get cluster assignments
            if NutriWiseDemoHandler._model:
                clusters = NutriWiseDemoHandler._model.predict(features)
                meals_df = meals_df.copy()
                meals_df['cluster'] = clusters
                
                # Find the best cluster based on calorie target
                cluster_means = []
                for cluster_id in range(NutriWiseDemoHandler._model.n_components):
                    cluster_meals = meals_df[meals_df['cluster'] == cluster_id]
                    if not cluster_meals.empty:
                        mean_calories = cluster_meals['calories_kcal'].mean()
                        cluster_means.append((cluster_id, mean_calories))
                
                # Sort clusters by proximity to target calories
                cluster_means.sort(key=lambda x: abs(x[1] - daily_calories/4))  # Average meal calories
                
                # Generate meal plan with randomization
                meal_plan = self._create_meal_plan_from_clusters(meals_df, cluster_means, daily_calories)
                
                return {
                    "breakfast": meal_plan['breakfast'],
                    "lunch": meal_plan['lunch'],
                    "dinner": meal_plan['dinner'],
                    "snacks": meal_plan['snacks'],
                    "total_calories": meal_plan['total_calories'],
                    "diet_type": diet_type,
                    "clustering_used": True
                }
            
            # If no model, fall back to random selection
            return self._generate_random_meals_from_df(meals_df, daily_calories, diet_type)
            
        except Exception as e:
            print(f"❌ Error in clustered meal generation: {e}")
            return self._generate_random_meals_from_df(meals_df, daily_calories, diet_type)
    
    def _create_meal_plan_from_clusters(self, meals_df: pd.DataFrame, cluster_means: list, daily_calories: float) -> Dict[str, Any]:
        """Create a balanced meal plan from clustered data with randomization"""
        # Calorie distribution
        breakfast_calories = daily_calories * 0.25
        lunch_calories = daily_calories * 0.35
        dinner_calories = daily_calories * 0.30
        snack_calories = daily_calories * 0.10
        
        meal_plan = {
            'breakfast': [],
            'lunch': [],
            'dinner': [],
            'snacks': [],
            'total_calories': 0
        }
        
        # Add randomization seed based on current time to ensure different results
        random.seed(int(datetime.now().timestamp() * 1000) % 10000)
        
        # Select meals from appropriate clusters with randomization
        for meal_type, target_calories in [('breakfast', breakfast_calories), ('lunch', lunch_calories), 
                                         ('dinner', dinner_calories), ('snacks', snack_calories)]:
            
            selected_meals = []
            remaining_calories = target_calories
            
            # Try to select from best clusters first, with randomization
            for cluster_id, _ in cluster_means[:3]:  # Use top 3 clusters
                cluster_meals = meals_df[meals_df['cluster'] == cluster_id]
                
                # Filter by meal type if available
                if 'meal_type' in cluster_meals.columns:
                    type_meals = cluster_meals[cluster_meals['meal_type'].str.lower().str.contains(meal_type.lower(), na=False)]
                    if type_meals.empty:
                        type_meals = cluster_meals  # Use all if no specific type found
                else:
                    type_meals = cluster_meals
                
                if not type_meals.empty and remaining_calories > 0:
                    # Select meals that fit the calorie budget
                    suitable_meals = type_meals[type_meals['calories_kcal'] <= remaining_calories * 1.2]  # Allow 20% flexibility
                    
                    if not suitable_meals.empty:
                        # Randomly select a meal
                        selected_meal = suitable_meals.sample(n=1).iloc[0]
                        selected_meals.append({
                            'name': selected_meal['food_item'],
                            'calories': round(selected_meal['calories_kcal'], 1),
                            'protein': round(selected_meal['protein_g'], 1),
                            'fat': round(selected_meal['fat_g'], 1),
                            'carbs': round(selected_meal['carbohydrates_g'], 1),
                            'cluster': int(selected_meal['cluster'])
                        })
                        remaining_calories -= selected_meal['calories_kcal']
                        
                        if len(selected_meals) >= 2:  # Limit meals per type
                            break
            
            # If no meals selected, pick random meals from any cluster
            if not selected_meals and not meals_df.empty:
                random_meals = meals_df.sample(n=min(2, len(meals_df)))
                for _, meal in random_meals.iterrows():
                    selected_meals.append({
                        'name': meal['food_item'],
                        'calories': round(meal['calories_kcal'], 1),
                        'protein': round(meal['protein_g'], 1),
                        'fat': round(meal['fat_g'], 1),
                        'carbs': round(meal['carbohydrates_g'], 1),
                        'cluster': int(meal.get('cluster', 0))
                    })
            
            meal_plan[meal_type] = selected_meals
            meal_plan['total_calories'] += sum(meal['calories'] for meal in selected_meals)
        
        return meal_plan
    
    def generate_demo_recommendations(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """Legacy method for backward compatibility"""
        age = profile.get('age', 30)
        weight = profile.get('weight', 70)
        height = profile.get('height', 170)
        gender = profile.get('gender', 'male')
        activity_level = profile.get('activity_level', 'moderate')
        goal = profile.get('goal', 'maintain')
        dietary_preference = profile.get('dietary_preference', 'mixed')
        
        daily_calories = self._calculate_daily_calories(age, weight, height, gender, activity_level, goal)
        
        if dietary_preference.lower() == 'vegetarian':
            return self._get_vegetarian_meals(daily_calories)
        else:
            return self._get_mixed_meals(daily_calories)

    def _generate_excel_based_meals(self, daily_calories: float, diet_type: str) -> Dict[str, Any]:
        """Generate meals from Excel file when PostgreSQL is not available"""
        try:
            excel_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'meal_data.xlsx')
            df = pd.read_excel(excel_path)
            
            if diet_type == 'vegetarian':
                filtered_df = df[df['Category'] == 'Vegetarian']
            else:
                filtered_df = df  # Use all meals for mixed diet
            
            if not filtered_df.empty:
                features = filtered_df[['Calories (kcal)', 'Protein (g)', 'Fat (g)', 'Carbohydrates (g)']].fillna(0)
                
                # Use GMM model if available
                if NutriWiseDemoHandler._model:
                    clusters = NutriWiseDemoHandler._model.predict(features)
                    filtered_df = filtered_df.copy()
                    filtered_df['cluster'] = clusters
                    
                    # Convert column names to match PostgreSQL format
                    filtered_df = filtered_df.rename(columns={
                        'Food Item': 'food_item',
                        'Calories (kcal)': 'calories_kcal',
                        'Protein (g)': 'protein_g',
                        'Fat (g)': 'fat_g',
                        'Carbohydrates (g)': 'carbohydrates_g'
                    })
                    
                    return self._generate_random_meals_from_df(filtered_df, daily_calories, diet_type)
                else:
                    return self._generate_fallback_meals(daily_calories, diet_type)
            else:
                return self._generate_fallback_meals(daily_calories, diet_type)
                
        except Exception as e:
            print(f"❌ Error generating Excel-based meals: {e}")
            return self._generate_fallback_meals(daily_calories, diet_type)
    
    def _generate_random_meals_from_df(self, meals_df: pd.DataFrame, daily_calories: float, diet_type: str) -> Dict[str, Any]:
        """Generate random meal selection from DataFrame"""
        try:
            # Calorie distribution
            breakfast_calories = daily_calories * 0.25
            lunch_calories = daily_calories * 0.35
            dinner_calories = daily_calories * 0.30
            snack_calories = daily_calories * 0.10
            
            meal_plan = {
                'breakfast': [],
                'lunch': [],
                'dinner': [],
                'snacks': [],
                'total_calories': 0
            }
            
            # Add randomization
            random.seed(int(datetime.now().timestamp() * 1000) % 10000)
            
            # Select meals for each type
            for meal_type, target_calories in [('breakfast', breakfast_calories), ('lunch', lunch_calories), 
                                             ('dinner', dinner_calories), ('snacks', snack_calories)]:
                
                selected_meals = []
                
                # Try to select appropriate meals
                suitable_meals = meals_df[meals_df['calories_kcal'] <= target_calories * 1.5]
                if suitable_meals.empty:
                    suitable_meals = meals_df  # Use any meals if none fit
                
                # Select 1-2 random meals
                n_meals = min(2, len(suitable_meals))
                if n_meals > 0:
                    random_meals = suitable_meals.sample(n=n_meals)
                    
                    for _, meal in random_meals.iterrows():
                        selected_meals.append({
                            'name': meal.get('food_item', meal.get('Food Item', 'Unknown')),
                            'calories': round(meal.get('calories_kcal', meal.get('Calories (kcal)', 0)), 1),
                            'protein': round(meal.get('protein_g', meal.get('Protein (g)', 0)), 1),
                            'fat': round(meal.get('fat_g', meal.get('Fat (g)', 0)), 1),
                            'carbs': round(meal.get('carbohydrates_g', meal.get('Carbohydrates (g)', 0)), 1),
                            'cluster': int(meal.get('cluster', 0))
                        })
                
                meal_plan[meal_type] = selected_meals
                meal_plan['total_calories'] += sum(meal['calories'] for meal in selected_meals)
            
            return {
                "breakfast": meal_plan['breakfast'],
                "lunch": meal_plan['lunch'],
                "dinner": meal_plan['dinner'],
                "snacks": meal_plan['snacks'],
                "total_calories": meal_plan['total_calories'],
                "diet_type": diet_type,
                "clustering_used": 'cluster' in meals_df.columns
            }
            
        except Exception as e:
            print(f"❌ Error in random meal generation: {e}")
            return self._generate_fallback_meals(daily_calories, diet_type)
    
    def _generate_fallback_meals(self, daily_calories: float, diet_type: str) -> Dict[str, Any]:
        """Generate fallback meal recommendations when other methods fail"""
        # Simple fallback meals
        sample_meals = {
            'vegetarian': {
                'breakfast': [{'name': 'Oatmeal with fruits', 'calories': 350, 'protein': 12, 'fat': 8, 'carbs': 60, 'cluster': 0}],
                'lunch': [{'name': 'Vegetable curry with rice', 'calories': 450, 'protein': 15, 'fat': 12, 'carbs': 70, 'cluster': 1}],
                'dinner': [{'name': 'Lentil soup with bread', 'calories': 400, 'protein': 18, 'fat': 10, 'carbs': 65, 'cluster': 2}],
                'snacks': [{'name': 'Mixed nuts', 'calories': 200, 'protein': 8, 'fat': 16, 'carbs': 8, 'cluster': 3}]
            },
            'mixed': {
                'breakfast': [{'name': 'Eggs with toast', 'calories': 380, 'protein': 20, 'fat': 15, 'carbs': 35, 'cluster': 0}],
                'lunch': [{'name': 'Chicken salad', 'calories': 420, 'protein': 35, 'fat': 18, 'carbs': 25, 'cluster': 1}],
                'dinner': [{'name': 'Grilled fish with vegetables', 'calories': 450, 'protein': 40, 'fat': 20, 'carbs': 30, 'cluster': 2}],
                'snacks': [{'name': 'Greek yogurt', 'calories': 150, 'protein': 15, 'fat': 5, 'carbs': 12, 'cluster': 3}]
            }
        }
        
        meals = sample_meals.get(diet_type, sample_meals['mixed'])
        total_calories = sum(meal['calories'] for meal_list in meals.values() for meal in meal_list)
        
        return {
            **meals,
            "total_calories": total_calories,
            "diet_type": diet_type,
            "clustering_used": False,
            "fallback": True
        }
    
    def get_vegetarian_meals(self, daily_calories: float) -> Dict[str, Any]:
        """Legacy method - redirects to new implementation"""
        return self._get_vegetarian_meals(daily_calories)
    
    def get_mixed_meals(self, daily_calories: float) -> Dict[str, Any]:
        """Legacy method - redirects to new implementation"""
        return self._get_mixed_meals(daily_calories)

def run_demo_server(port=8000):
    """Run the demo server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, NutriWiseDemoHandler)
    print(f"🚀 NutriWise Demo Server running on http://localhost:{port}")
    print("📱 Frontend should connect to this server automatically")
    print("⚡ This is a demo version - install full dependencies for production features")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == "__main__":
    run_demo_server()
