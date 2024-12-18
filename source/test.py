import data_pca
import supervised_models
import unsupervised_models
import data_preparation
import data_processing
import visualization
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Todo: Fix Elliptical
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def run_test():
    base_dir = os.getcwd()  # Current working directory
    # Path to /nad/data folder
    data_folder = os.path.join(base_dir, "data")
    # Path to test.csv file
    csv_file = os.path.join(data_folder, "ACI-IoT-2023-Payload.csv")

    X_train, y_train, X_test, y_test, feature_names = data_processing.load_and_preprocess_data(
        csv_file)

    # Perform PCA and get transformed training and test sets
    X_train_pca, X_test_pca = data_pca.perform_pca_and_plot(
        X_train, y_train, feature_names, X_test=X_test)

    # Check shapes of transformed data
    print(
        f"X_train_pca shape: {X_train_pca.shape}, y_train shape: {y_train.shape}")
    print(
        f"X_test_pca shape: {X_test_pca.shape}, y_test shape: {y_test.shape}")

    # Initialize lists for storing model metrics
    model_names = []
    accuracies = []
    train_times = []
    pred_times = []

    # Train and evaluate Random Forest (supervised) with PCA-transformed data
    print("Training Random Forest...")
    rf_model, rf_acc, rf_train_time, rf_pred_time = supervised_models.train_random_forest(
        X_train_pca, y_train, X_test_pca, y_test
    )
    print(f"Random Forest Accuracy: {rf_acc:.2f}")
    model_names.append("Random Forest")
    accuracies.append(rf_acc)
    train_times.append(rf_train_time)
    pred_times.append(rf_pred_time)

    # Train and evaluate Isolation Forest (unsupervised) with PCA-transformed data
    print("Training Isolation Forest...")
    iso_forest_model, iso_forest_acc, iso_forest_train_time, iso_forest_pred_time = unsupervised_models.train_isolation_forest(
        X_train_pca, X_test_pca
    )
    print(f"Isolation Forest Accuracy: {iso_forest_acc:.2f}")
    model_names.append("Isolation Forest")
    accuracies.append(iso_forest_acc)
    train_times.append(iso_forest_train_time)
    pred_times.append(iso_forest_pred_time)

    # Train and evaluate Elliptic Envelope (unsupervised) with PCA-transformed data
    print("Training Elliptic Envelope...")
    elliptic_env_model, elliptic_env_acc, elliptic_env_train_time, elliptic_env_pred_time = unsupervised_models.train_elliptic_envelope(
        X_train_pca, X_test_pca
    )
    print(f"Elliptic Envelope Accuracy: {elliptic_env_acc:.2f}")
    model_names.append("Elliptic Envelope")
    accuracies.append(elliptic_env_acc)
    train_times.append(elliptic_env_train_time)
    pred_times.append(elliptic_env_pred_time)

    # Train and evaluate Local Outlier Factor (LOF) (unsupervised) with PCA-transformed data
    print("Training LOF...")
    lof_model, lof_acc, lof_train_time, lof_pred_time = unsupervised_models.train_local_outlier_factor(
        X_train_pca, X_test_pca
    )
    print(f"LOF Accuracy: {lof_acc:.2f}")
    model_names.append("LOF")
    accuracies.append(lof_acc)
    train_times.append(lof_train_time)
    pred_times.append(lof_pred_time)

    # Train and evaluate HDBSCAN (unsupervised) with PCA-transformed data
    print("Training HDBSCAN...")
    hdbscan_model, hdbscan_acc, hdbscan_train_time, hdbscan_pred_time = unsupervised_models.train_hdbscan(
        X_train_pca, X_test_pca, min_samples=5, min_cluster_size=10
    )
    print(f"HDBSCAN Accuracy: {hdbscan_acc:.2f}")
    model_names.append("HDBSCAN")
    accuracies.append(hdbscan_acc)
    train_times.append(hdbscan_train_time)
    pred_times.append(hdbscan_pred_time)


if __name__ == "__main__":
    run_test()

    