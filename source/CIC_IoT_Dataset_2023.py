from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# Canadian Institute for Cybersecurity - CIC IoT Dataset 2023
#
# A real-time dataset and benchmark for large-scale attacks in IoT environment
# The main goal of this research is to propose a novel and extensive IoT attack
# dataset to foster the development of security analytics applications in real
# IoT operations. To accomplish this, 33 attacks are executed in an IoT topology
# composed of 105 devices.
#
# These attacks are classified into seven categories, namely DDoS, DoS, Recon,
# Web-based, Brute Force, Spoofing, and Mirai. Finally, all attacks are executed
# by malicious IoT devices targeting other IoT device
#
# https://www.unb.ca/cic/datasets/iotdataset-2023.html


# engineered = only engineered features
# selected = only selected features
# both = both engineered and selected features
def getTrainTestDataFromCSV(csv_file):
    data = pd.read_csv(csv_file)

    # Ensure label column is properly formatted
    data["Label"] = data["Label"].apply(lambda x: 0 if x == "BENIGN" else 1)

    # Selected Features
    selected_features = [
        "Header_Length", "Protocol Type", "Time_To_Live", "Rate", "fin_flag_number",
        "syn_flag_number", "rst_flag_number", "psh_flag_number", "ack_flag_number",
        "ece_flag_number", "cwr_flag_number", "ack_count", "syn_count", "fin_count",
        "rst_count", "HTTP", "HTTPS", "DNS", "Telnet", "SMTP", "SSH", "IRC",
        "TCP", "UDP", "DHCP", "ARP", "ICMP", "IGMP", "IPv", "LLC", "Tot sum",
        "Min", "Max", "AVG", "Std", "Tot size", "IAT", "Number", "Variance"
    ]

    X = data[selected_features].copy()

    # Convert all features to numeric
    X = X.apply(pd.to_numeric, errors='coerce')

    # Handle missing values and infinite values
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X.fillna(X.median(), inplace=True)
    X.clip(lower=-1e6, upper=1e6, inplace=True)
    assert not X.isnull().values.any(), "NaN values found after preprocessing"

    y = data["Label"]

    # Train-test split
    X_benign = X[y == 0]
    X_anomalies = X[y == 1]
    train_benign_size = int(len(X_benign) * 0.70)
    X_train = X_benign.sample(n=train_benign_size, random_state=42)
    y_train = pd.Series(0, index=X_train.index)
    test_benign_size = int(len(X_benign) * 0.20)
    test_anomalies_size = int(test_benign_size * 0.18)
    X_test_benign = X_benign.drop(X_train.index).sample(
        n=test_benign_size, random_state=42)
    X_test_anomalies = X_anomalies.sample(
        n=test_anomalies_size, random_state=42)
    X_test = pd.concat([X_test_benign, X_test_anomalies], axis=0)
    y_test = pd.concat([pd.Series(0, index=X_test_benign.index),
                        pd.Series(1, index=X_test_anomalies.index)], axis=0)
    X_test, y_test = shuffle(X_test, y_test, random_state=42)

    # Display packet counts
    print(f"Number of benign packets in training: {len(X_train)}")
    print(f"Number of benign packets in testing: {len(X_test_benign)}")
    print(f"Number of anomaly packets in testing: {len(X_test_anomalies)}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # w/o PCA: return X_train_scaled, y_train, X_test_scaled, y_test
    return X_train_scaled, y_train, X_test_scaled, y_test
