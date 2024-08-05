import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA 


class KMeans:
    """
    A custom implementation of the K-Means clustering algorithm.
    """

    def __init__(self, n_clusters ):
        """
        Initialize the KMeans class with the number of clusters.

        Parameters:
        n_clusters (int): The number of clusters to form as well as the number of centroids to generate.
        """
        self.n_clusters = n_clusters
        self.n_interation = 0
        self.centers = None
    
    def fit(self, data_set):
        """
        Compute K-Means clustering.

        This function clusters the input data into 'n_clusters' clusters using the K-Means algorithm.
        It iteratively updates the centroids until convergence.

        Parameters:
        data_set (numpy.ndarray): The dataset to be clustered, where each row represents a data point.

        Returns:
        None
        """
        # Initialize labels and centroids
        self.labels = np.array(data_set.shape[0])  # creats a vector in length of dataset
        random_indices = np.random.choice(data_set.shape[0], self.n_clusters, replace=False)
        self.centroids = data_set[random_indices]
        
        while True:
            # Count the iteration number
            self.n_interation += 1
            # Assign labels to each datapoint based on centroids
            self.labels = self.select_labels(data_set)
            
            # Update centroids
            new_centroids = self.update_centroids(data_set)
            
            # Plot clusters
            self.display_clusters(data_set)
            
            # Check if centroids moved less than epsilon
            if np.linalg.norm(new_centroids - self.centroids) < 0.001:
                self.n_interation = 0
                self.centers = new_centroids
                break
            
            self.centroids = new_centroids
    
    def select_labels(self, data):
        """
        Assign labels to each datapoint based on the closest centroid.

        This function calculates the distance of each data point from the centroids and
        assigns the data point to the nearest centroid.

        Parameters:
        data (numpy.ndarray): The dataset to be clustered.

        Returns:
        numpy.ndarray: An array of cluster labels for each datapoint in the dataset.
        """
        # Calculate distances between data points and centroids
        distances = np.sqrt(((data - self.centroids[:, np.newaxis])**2).sum(axis=2))
        return np.argmin(distances, axis=0)
    
    def update_centroids(self,data ):
        """
        Calculate new centroids as the mean of the points in each cluster.

        This function recalculates the centroid of each cluster by taking the mean
        of all points assigned to that cluster.

        Parameters:
        data (numpy.ndarray): The dataset to be clustered.

        Returns:
        numpy.ndarray: An array of new centroids for each cluster.
        """
        new_centroids = []
        for i in range(self.n_clusters):
            new_centroids.append(np.mean(data[self.labels == i], axis=0))
        return np.array(new_centroids)
    
    def display_clusters(self, final_clusters):
        """
        Display the clusters and centroids using a scatter plot.

        This function plots each cluster with a different color and marks the centroids
        with a red 'x'. It shows the clusters at the current iteration.

        Parameters:
        final_clusters (numpy.ndarray): The dataset to be clustered.

        Returns:
        None
        """
        plt.figure()
        plt.title(f'KMeans Clustering Figure no.{self.n_interation}')
        for i in range(self.n_clusters):
            cluster_points = final_clusters[self.labels == i]
            plt.scatter(cluster_points[:, 0], cluster_points[:, 1])
        plt.scatter(self.centroids[:, 0], self.centroids[:, 1], marker='x', s=100, linewidths=3 , color='red')
        plt.show()

# Set seed numbers to 42
np.random.seed(42)

# Give inputs
df = pd.read_csv('Dry_Bean.csv')
df_encoded = pd.get_dummies(df, columns=['Class'])

# Using PCA method to reduce dimensions
pca = PCA(n_components=2)
reduced = pca.fit_transform(df_encoded)

# Run algorithm
kmeans = KMeans(n_clusters=3)
kmeans.fit(reduced)

# Get the cluster labels and cluster centers
centers = kmeans.centers
labels = kmeans.select_labels(reduced)

# Plot the clusters with different colors
plt.scatter(reduced[:, 0], reduced[:, 1], c=labels, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], marker='x', s=100, linewidths=3, color='red')
plt.title('K-Means Clustering final figure')
plt.show()
