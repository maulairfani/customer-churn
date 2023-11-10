import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans 
import matplotlib.pyplot as plt
import seaborn as sns

# Prepare data
df = pd.read_excel("data/Telco_customer_churn_adapted_v2.xlsx")
columns = ["Tenure Months", "Monthly Purchase (Thou. IDR)", "CLTV (Predicted Thou. IDR)"]
churners = df[df["Churn Label"] == "Yes"][columns]
non_churners = df[df["Churn Label"] == "No"][columns]

def segmentation(data):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)

    k=3
    kmeans = KMeans(n_clusters=k, random_state=0, n_init="auto")
    kmeans.fit(data_scaled)
    data["Cluster"] = kmeans.labels_

    return data



