import numpy as np

def process_data(data):
    """Performs advanced data processing on the input data."""
    # Preprocess the data
    data = np.log1p(data)
    data = (data - np.mean(data)) / np.std(data)

    # Apply principal component analysis
    pca = PCA(n_components=10)
    data_transformed = pca.fit_transform(data)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=5, random_state=0)
    labels = kmeans.fit_predict(data_transformed)

    return data_transformed, labels

if __name__ == '__main__':
    # Example usage
    data = np.random.rand(1000, 100)
    processed_data, labels = process_data(data)
    print(f'Processed data shape: {processed_data.shape}')
    print(f'Cluster labels: {labels}')