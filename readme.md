NutriWise – Data-Driven Meal Planner
Overview
NutriWise is an intelligent meal planning application that provides personalized Indian meal recommendations based on a user's Basal Metabolic Rate (BMR), dietary preferences, and health goals. It features a Tkinter GUI, an interactive recommendation system, and an optional GMM cluster visualization to showcase the nutritional relationship between different food items.

Features
Personalized Meal Planning – Calculates BMR and recommends meals based on macronutrient targets.
Vegetarian & Non-Vegetarian Options – Users can filter meal choices based on dietary preferences.
Randomized Meal Suggestions – Users can generate new meal plans dynamically.
GMM-Based Clustering (Optional Visualization) – Uses Gaussian Mixture Models (GMM) and PCA to group foods based on nutritional content.
Modular & Maintainable Codebase – Structured into separate modules for data processing, recommendations, GUI, and visualization.
Installation & Setup
1. Clone the Repository
''' bash git clone https://github.com/yourusername/NutriWise.git cd NutriWise '''

2. Create a Virtual Environment (Recommended)
''' bash python -m venv .venv

Windows
..venv\Scripts\activate

OR macOS/Linux
source .venv/bin/activate
'''

3. Install Dependencies
''' bash pip install -r requirements.txt '''

How to Run the Application
Run the Main File
After setting up, start the GUI by running:
''' bash python main.py '''

Project Structure
''' plaintext NutriWise/ │-- Data/ │ └── Updated_500_Indian_Food_Nutritional_Data.xlsx │-- modules/ │ │-- init.py # Makes the directory a package │ │-- data_preprocessing.py # Loads and cleans dataset │ │-- recommendation.py # BMR calculation & meal recommendation logic │ │-- gui.py # Tkinter GUI interface │ │-- graph.py # GMM visualization │-- tests/ # (Optional) Unit tests │ │-- test_data_preprocessing.py │ │-- test_recommendation.py │-- main.py # Entry point of the application │-- README.md # Documentation │-- requirements.txt # List of dependencies │-- .gitignore # Files to be ignored in Git │-- LICENSE # License file (if applicable) '''

Usage Guide
1. Enter User Details
Age, Height, Weight, Gender
Select Goal – Weight Loss, Normal, or High Protein
Select Vegetarian or Non-Vegetarian Option
Click "Calculate & Recommend"
2. View Recommendations
The recommended meal plan will be displayed.
Click "Randomize" to generate new meal suggestions.
3. Optional: View GMM Cluster Graph
Click "Show GMM Graph" to visualize nutritional clustering.
Technologies Used
Python – Core language
Pandas & OpenPyXL – Data processing
Scikit-learn – Machine learning (PCA, GMM clustering)
Matplotlib – Data visualization
Tkinter – Graphical User Interface (GUI)
Tabulate – Formatting output in tables
Troubleshooting & Common Issues
Matplotlib Not Found
If you see:
''' plaintext ModuleNotFoundError: No module named 'matplotlib' ''' Install it manually:
''' bash pip install matplotlib '''

Tkinter Issues (Linux Users)
If Tkinter isn't installed:
''' bash sudo apt-get install python3-tk '''

Module Import Errors
If you see:
''' plaintext ModuleNotFoundError: No module named 'modules' ''' Ensure you’re running Python inside the project folder:
''' bash cd NutriWise python main.py '''

License
This project is licensed under the MIT License – you are free to use and modify it.

Next Steps
✅ Add requirements.txt
✅ Add .gitignore
✅ Add LICENSE
✅ (Optional) Add tests/ for unit testing