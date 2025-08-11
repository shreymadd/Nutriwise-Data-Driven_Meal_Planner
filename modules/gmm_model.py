import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
import joblib

class GMMMealRecommender:
    def __init__(self, n_components=5, random_state=42):
        self.n_components = n_components
        self.random_state = random_state
        self.model = GaussianMixture(n_components=n_components, random_state=random_state)

    def fit(self, data):
        self.model.fit(data)

    def predict(self, data):
        return self.model.predict(data)

    def recommend_meals(self, data, target_calories, n_recommendations=5):
        # Cluster the data
        clusters = self.predict(data)
        data['cluster'] = clusters

        # Find the cluster whose centroids are closest to the target calories
        centroids = self.model.means_
        # Find the cluster with the centroid that has the closest calories to the target
        # Note: we assume the first feature is calories
        closest_cluster = np.argmin(np.abs(centroids[:,0] - target_calories))

        # Get meals from the closest cluster
        cluster_meals = data[data['cluster'] == closest_cluster]
        # Randomly select n_recommendations meals
        return cluster_meals.sample(n_recommendations)

    def save_model(self, filepath):
        joblib.dump(self.model, filepath)

    def load_model(self, filepath):
        self.model = joblib.load(filepath)
