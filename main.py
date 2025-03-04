import os
from modules.data_preprocessing import load_data, clean_data
from modules.gui import create_app

def main():
    # Adjust the path to your dataset
    project_dir = os.path.dirname(__file__)
    data_path = os.path.join(project_dir, "data", "Updated_500_Indian_Food_Nutritional_Data.xlsx")

    # Load and clean
    df = load_data(data_path)
    df = clean_data(df)

    # Create GUI app with df
    root = create_app(df)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
