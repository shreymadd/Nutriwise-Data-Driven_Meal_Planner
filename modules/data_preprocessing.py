import re
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def load_data(file_path):
    """
    Loads the Excel file from the given file path.
    """
    if not file_path:
        print("DEBUG: file_path is empty or None.")
        return None  # or raise ValueError("No file path provided.")
    df = pd.read_excel(file_path, engine="openpyxl")
    print(f"DEBUG: Loaded data with shape={df.shape}")
    return df  # <--- Must return!

def clean_data(df):
    if df is None:
        print("DEBUG: clean_data received None.")
        return None
    for column in ['Carbohydrates (g)', 'Protein (g)', 'Fat (g)', 'Calories (kcal)']:
        df[column] = df[column].apply(
            lambda x: convert_to_float(x)
        )
    print("DEBUG: After cleaning, df shape =", df.shape)
    return df  # <--- Must return!

def convert_to_float(value):
    import pandas as pd
    if pd.isnull(value):
        return 0.0
    cleaned = re.sub(r'[^0-9.]', '', str(value))
    if cleaned in ('.', ''):
        return 0.0
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def preprocess_data_with_pca(df):
    if df is None:
        return None
    features = df[['Carbohydrates (g)', 'Protein (g)', 'Fat (g)']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(scaled_features)
    return pca_features
