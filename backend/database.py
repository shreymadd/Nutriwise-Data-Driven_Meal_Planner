"""
PostgreSQL Database Manager for NutriWise
Replaces Supabase with direct PostgreSQL connection
"""
import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PostgreSQLManager:
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize PostgreSQL connection
        
        Args:
            connection_string: PostgreSQL connection string
                             If None, uses environment variables or defaults to local
        """
        if connection_string:
            self.connection_string = connection_string
        else:
            # Use environment variables or default to local PostgreSQL
            host = os.getenv('POSTGRES_HOST', 'localhost')
            port = os.getenv('POSTGRES_PORT', '5432')
            database = os.getenv('POSTGRES_DB', 'nutriwise')
            user = os.getenv('POSTGRES_USER', 'postgres')
            password = os.getenv('POSTGRES_PASSWORD', 'password')
            
            self.connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        
        # Create SQLAlchemy engine
        self.engine = create_engine(self.connection_string)
        logger.info("PostgreSQL connection initialized")
    
    def create_tables(self):
        """Create necessary tables for NutriWise"""
        create_meals_table = """
        CREATE TABLE IF NOT EXISTS meals (
            id SERIAL PRIMARY KEY,
            food_item VARCHAR(255) NOT NULL,
            category VARCHAR(100),
            meal_type VARCHAR(50),
            calories_kcal FLOAT,
            protein_g FLOAT,
            fat_g FLOAT,
            carbohydrates_g FLOAT,
            fiber_g FLOAT,
            sugar_g FLOAT,
            sodium_mg FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_user_profiles_table = """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id SERIAL PRIMARY KEY,
            age INTEGER,
            weight FLOAT,
            height FLOAT,
            gender VARCHAR(10),
            activity_level VARCHAR(50),
            goal VARCHAR(50),
            dietary_preference VARCHAR(50),
            daily_calories FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_meal_plans_table = """
        CREATE TABLE IF NOT EXISTS meal_plans (
            id SERIAL PRIMARY KEY,
            user_profile_id INTEGER REFERENCES user_profiles(id),
            plan_date DATE DEFAULT CURRENT_DATE,
            breakfast_ids INTEGER[],
            lunch_ids INTEGER[],
            dinner_ids INTEGER[],
            snack_ids INTEGER[],
            total_calories FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_meals_table))
                conn.execute(text(create_user_profiles_table))
                conn.execute(text(create_meal_plans_table))
                conn.commit()
                logger.info("Tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    def migrate_excel_to_postgres(self, excel_path: str):
        """
        Migrate meal data from Excel to PostgreSQL
        
        Args:
            excel_path: Path to the Excel file containing meal data
        """
        try:
            # Read Excel data
            df = pd.read_excel(excel_path)
            logger.info(f"Read {len(df)} rows from Excel file")
            
            # Standardize column names
            column_mapping = {
                'Food Item': 'food_item',
                'Category': 'category',
                'Meal Type': 'meal_type',
                'Calories (kcal)': 'calories_kcal',
                'Protein (g)': 'protein_g',
                'Fat (g)': 'fat_g',
                'Carbohydrates (g)': 'carbohydrates_g',
                'Fiber (g)': 'fiber_g',
                'Sugar (g)': 'sugar_g',
                'Sodium (mg)': 'sodium_mg'
            }
            
            # Rename columns to match database schema
            df = df.rename(columns=column_mapping)
            
            # Select only columns that exist in both DataFrame and database
            db_columns = ['food_item', 'category', 'meal_type', 'calories_kcal', 
                         'protein_g', 'fat_g', 'carbohydrates_g', 'fiber_g', 
                         'sugar_g', 'sodium_mg']
            
            available_columns = [col for col in db_columns if col in df.columns]
            df_clean = df[available_columns]
            
            # Insert data into PostgreSQL
            df_clean.to_sql('meals', self.engine, if_exists='replace', index=False)
            logger.info(f"Successfully migrated {len(df_clean)} meals to PostgreSQL")
            
        except Exception as e:
            logger.error(f"Error migrating Excel data: {e}")
            raise
    
    def get_meals(self, category: Optional[str] = None, meal_type: Optional[str] = None) -> pd.DataFrame:
        """
        Get meals from database with optional filtering
        
        Args:
            category: Filter by category (e.g., 'Vegetarian', 'Non-Vegetarian')
            meal_type: Filter by meal type (e.g., 'Breakfast', 'Lunch', 'Dinner', 'Snack')
            
        Returns:
            DataFrame containing meal data
        """
        try:
            query = "SELECT * FROM meals WHERE 1=1"
            params = {}
            
            if category:
                query += " AND category = %(category)s"
                params['category'] = category
                
            if meal_type:
                query += " AND meal_type = %(meal_type)s"
                params['meal_type'] = meal_type
            
            df = pd.read_sql_query(query, self.engine, params=params)
            logger.info(f"Retrieved {len(df)} meals from database")
            return df
            
        except Exception as e:
            logger.error(f"Error retrieving meals: {e}")
            raise
    
    def get_meals_for_clustering(self, category: Optional[str] = None) -> pd.DataFrame:
        """
        Get meals with nutritional features for GMM clustering
        
        Args:
            category: Filter by dietary category
            
        Returns:
            DataFrame with nutritional features
        """
        try:
            query = """
            SELECT id, food_item, category, meal_type,
                   calories_kcal, protein_g, fat_g, carbohydrates_g
            FROM meals 
            WHERE calories_kcal IS NOT NULL 
              AND protein_g IS NOT NULL 
              AND fat_g IS NOT NULL 
              AND carbohydrates_g IS NOT NULL
            """
            
            params = {}
            if category:
                query += " AND category = %(category)s"
                params['category'] = category
            
            df = pd.read_sql_query(query, self.engine, params=params)
            logger.info(f"Retrieved {len(df)} meals for clustering")
            return df
            
        except Exception as e:
            logger.error(f"Error retrieving meals for clustering: {e}")
            raise
    
    def save_user_profile(self, profile_data: Dict[str, Any]) -> int:
        """
        Save user profile to database
        
        Args:
            profile_data: Dictionary containing user profile information
            
        Returns:
            ID of the saved profile
        """
        try:
            query = """
            INSERT INTO user_profiles (age, weight, height, gender, activity_level, 
                                     goal, dietary_preference, daily_calories)
            VALUES (%(age)s, %(weight)s, %(height)s, %(gender)s, %(activity_level)s,
                    %(goal)s, %(dietary_preference)s, %(daily_calories)s)
            RETURNING id;
            """
            
            with self.engine.connect() as conn:
                result = conn.execute(text(query), profile_data)
                profile_id = result.fetchone()[0]
                conn.commit()
                logger.info(f"Saved user profile with ID: {profile_id}")
                return profile_id
                
        except Exception as e:
            logger.error(f"Error saving user profile: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'engine'):
            self.engine.dispose()
            logger.info("Database connection closed")
