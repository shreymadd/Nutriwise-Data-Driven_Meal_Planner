import pandas as pd

def calculate_bmr(weight_kg, height_cm, age, gender='male'):
    """
    Calculates the Basal Metabolic Rate (BMR) using the Mifflin-St Jeor equation.
    """
    if gender == 'male':
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

def recommend_food(df, meal_calories, carb_ratio, fat_ratio, protein_ratio, is_vegetarian=False):
    """
    Recommends foods from df based on target macros.
    Introduces randomness by shuffling the data with sample(frac=1).
    If is_vegetarian is True, filter Category == 'Vegetarian'.
    """
    if is_vegetarian:
        df = df[df['Category'] == 'Vegetarian'].copy()

    carb_target = meal_calories * carb_ratio
    fat_target = meal_calories * fat_ratio
    protein_target = meal_calories * protein_ratio
    recommendations = []
    selected_items = set()

    nutrient_targets = [
        ('Carbohydrates (g)', carb_target),
        ('Fat (g)', fat_target),
        ('Protein (g)', protein_target)
    ]

    for nutrient, target_calories in nutrient_targets:
        # Shuffle the items (sample(frac=1)) with no fixed random_state
        nutrient_df = df[
            (df['Calories (kcal)'] > 0) & (~df['Food Item'].isin(selected_items))
        ].sample(frac=1)

        selected = False
        for _, item in nutrient_df.iterrows():
            item_calories_per_100g = item['Calories (kcal)']
            required_portion = (target_calories / item_calories_per_100g) * 100
            if 50 <= required_portion <= 150:
                if item['Food Item'] not in selected_items:
                    item_with_portion = item[[
                        'Food Item','Carbohydrates (g)','Protein (g)','Fat (g)','Category'
                    ]].copy()
                    item_with_portion['Calories'] = round(target_calories, 2)
                    item_with_portion['Portion (g)'] = round(required_portion, 2)
                    recommendations.append(item_with_portion)
                    selected_items.add(item['Food Item'])
                    selected = True
                    break

        # If no item fits the 50-150g portion range, pick the first available item
        if not selected:
            for _, item in nutrient_df.iterrows():
                if item['Food Item'] not in selected_items:
                    item_with_portion = item[[
                        'Food Item','Carbohydrates (g)','Protein (g)','Fat (g)','Category'
                    ]].copy()
                    item_with_portion['Calories'] = round(target_calories, 2)
                    portion_calc = (target_calories / item['Calories (kcal)']) * 100
                    item_with_portion['Portion (g)'] = round(portion_calc, 2)
                    recommendations.append(item_with_portion)
                    selected_items.add(item['Food Item'])
                    break

    return pd.DataFrame(recommendations)
