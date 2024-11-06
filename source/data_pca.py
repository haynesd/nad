import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def perform_pca_and_plot(X_train, y_train, feature_names, n_components=2):
    # Standardize the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # PCA parameters
    whiten = False
    random_state = 42
    pca = PCA(n_components=n_components,
              whiten=whiten, random_state=random_state)

    # Apply PCA transformation
    X_train_PCA = pca.fit_transform(X_train_scaled)
    x_train_PCA = pd.DataFrame(data=X_train_PCA, index=range(len(X_train)))

    # Print explained variance
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = explained_variance.cumsum()  # Cumulative variance explained
    print("Explained variance for each component:")
    for i, variance in enumerate(explained_variance, start=1):
        print(
            f"Principal Component {i}: {variance:.4f} ({variance * 100:.2f}%)")
        if i <= 2:
            print(
                f"Cumulative variance after Component {i}: {cumulative_variance[i-1] * 100:.2f}%")

    # Map actual feature names
    loadings = pd.DataFrame(pca.components_[:2].T, columns=[
                            "PC1", "PC2"], index=feature_names)
    print("\nFeature loadings for the first two principal components:")
    print(loadings)

    # Optional: visualize feature loadings
    plt.figure(figsize=(10, 6))
    plt.bar(feature_names, loadings["PC1"], alpha=0.6, label="PC1")
    plt.bar(feature_names, loadings["PC2"], alpha=0.6, label="PC2")
    plt.xlabel("Features")
    plt.ylabel("Loadings")
    plt.title("Feature Loadings for the First Two Principal Components")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    # Scatter plot of the first two principal components
    plt.figure(figsize=(8, 6))
    plt.scatter(x_train_PCA.iloc[:, 0], x_train_PCA.iloc[:,
                1], c=y_train, cmap='viridis', alpha=0.7)
    plt.colorbar(label='Target')
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title("PCA of X_train Data (First 2 Components)")
    plt.grid()
    plt.show()