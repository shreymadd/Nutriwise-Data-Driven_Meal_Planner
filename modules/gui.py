import tkinter as tk
from tkinter import ttk, Text, Scrollbar, messagebox
from tabulate import tabulate

# Import your logic modules
from .recommendation import calculate_bmr, recommend_food


def create_app(df):
    """
    Builds and returns the main Tkinter application (root).
    df is the DataFrame loaded & cleaned.
    """
    root = tk.Tk()
    root.title("Dietary Recommendation System")
    root.state('zoomed')
    root.resizable(True, True)

    # Notebook for 2 tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    # Tabs
    input_tab = ttk.Frame(notebook)
    recommendation_tab = ttk.Frame(notebook)

    notebook.add(input_tab, text="Input")
    notebook.add(recommendation_tab, text="Recommendations")

    # Variables
    age_var = tk.StringVar()
    height_var = tk.StringVar()
    weight_var = tk.StringVar()
    gender_var = tk.StringVar()
    goal_var = tk.StringVar()
    veg_var = tk.StringVar()

    # Input Tab
    input_frame = ttk.Frame(input_tab, padding=20)
    input_frame.pack(fill='both', expand=True)

    ttk.Label(input_frame, text="Age").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    age_entry = ttk.Entry(input_frame, textvariable=age_var, width=25)
    age_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    ttk.Label(input_frame, text="Height (cm)").grid(row=1, column=0, padx=5, pady=5, sticky='e')
    height_entry = ttk.Entry(input_frame, textvariable=height_var, width=25)
    height_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    ttk.Label(input_frame, text="Weight (kg)").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    weight_entry = ttk.Entry(input_frame, textvariable=weight_var, width=25)
    weight_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    ttk.Label(input_frame, text="Gender").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    gender_combo = ttk.Combobox(input_frame, textvariable=gender_var, values=["Male", "Female"], width=23)
    gender_combo.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    gender_combo.current(0)

    ttk.Label(input_frame, text="Goal").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    goal_combo = ttk.Combobox(input_frame, textvariable=goal_var, values=["Weight Loss", "Normal", "High Protein"], width=23)
    goal_combo.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    goal_combo.current(1)

    ttk.Label(input_frame, text="Vegetarian?").grid(row=5, column=0, padx=5, pady=5, sticky='e')
    veg_combo = ttk.Combobox(input_frame, textvariable=veg_var, values=["No", "Yes"], width=23)
    veg_combo.grid(row=5, column=1, padx=5, pady=5, sticky='w')
    veg_combo.current(0)

    # Recommendation Tab
    result_frame = ttk.Frame(recommendation_tab, padding=20)
    result_frame.pack(fill='both', expand=True)

    recommendation_text = Text(result_frame, wrap='word')
    recommendation_text.pack(side='left', fill='both', expand=True)

    scrollbar = Scrollbar(result_frame, command=recommendation_text.yview)
    scrollbar.pack(side='right', fill='y')
    recommendation_text.config(yscrollcommand=scrollbar.set)

    # Logic
    def calculate_and_recommend():
        """
        Called when user clicks 'Calculate & Recommend'.
        """
        try:
            age = int(age_var.get())
            height_cm = float(height_var.get())
            weight_kg = float(weight_var.get())
            gender = gender_var.get().lower()
            goal = goal_var.get()
            vegetarian_choice = veg_var.get()

            bmr = calculate_bmr(weight_kg, height_cm, age, gender)
            meal_calories = (bmr * 1.55) / 3

            if goal == "Weight Loss":
                carb_ratio, fat_ratio, protein_ratio = 0.4, 0.25, 0.35
            elif goal == "High Protein":
                carb_ratio, fat_ratio, protein_ratio = 0.3, 0.3, 0.4
            else:
                carb_ratio, fat_ratio, protein_ratio = 0.5, 0.25, 0.25

            is_veg = (vegetarian_choice == "Yes")

            recs = recommend_food(
                df,
                meal_calories,
                carb_ratio,
                fat_ratio,
                protein_ratio,
                is_vegetarian=is_veg
            )

            notebook.select(recommendation_tab)
            recommendation_text.delete('1.0', 'end')
            recommendation_text.insert('end', "Recommended Foods for One Meal with Adjusted Portions:\n\n")
            recommendation_text.insert(
                'end',
                tabulate(recs, headers='keys', tablefmt='psql', showindex=False)
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def randomize_recommendations():
        """
        Called when user clicks 'Randomize'.
        """
        calculate_and_recommend()

    calc_button = ttk.Button(input_frame, text="Calculate & Recommend", command=calculate_and_recommend)
    calc_button.grid(row=6, column=0, columnspan=2, pady=10)

    rand_button = ttk.Button(result_frame, text="Randomize", command=randomize_recommendations)
    rand_button.pack(pady=10)

    # GMM Graph Button
    def show_clusters():
        from modules.graph import show_gmm_graph
        show_gmm_graph(df, n_components=3)  # or more components as you wish

    cluster_button = ttk.Button(result_frame, text="Show GMM Graph", command=show_clusters)
    cluster_button.pack(pady=10)

    return root
