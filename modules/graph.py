import matplotlib
matplotlib.use("TkAgg")  # So Matplotlib can show in a Tkinter environment
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture

from modules.data_preprocessing import preprocess_data_with_pca

def show_gmm_graph(df, n_components=3):
    """
    Fits a Gaussian Mixture Model with n_components on the PCA-reduced data,
    then plots the results in a scatter plot.
    """
    # PCA reduce to 2D
    pca_feat = preprocess_data_with_pca(df)

    # Fit GMM
    gmm = GaussianMixture(n_components=n_components)
    gmm.fit(pca_feat)

    # Predict cluster labels
    labels = gmm.predict(pca_feat)

    # Plot each point, color-coded by cluster label
    plt.figure()
    plt.scatter(pca_feat[:, 0], pca_feat[:, 1], c=labels, cmap='viridis')
    plt.title(f"GMM Clusters with {n_components} Components (PCA Projection)")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.show()
