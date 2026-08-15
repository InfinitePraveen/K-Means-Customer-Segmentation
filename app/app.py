from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Load models
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
scaler = joblib.load(os.path.join(model_path, "scaler.pkl"))
kmeans = joblib.load(os.path.join(model_path, "kmeans_model.pkl"))
pca = joblib.load(os.path.join(model_path, "pca_model.pkl"))

# Load cluster centers
cluster_centers = pd.read_csv(os.path.join(model_path, "cluster_centers.csv"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get data from request
        data = request.json
        annual_income = float(data["annual_income"])
        spending_score = float(data["spending_score"])

        # Create feature array
        features = np.array([[annual_income, spending_score]])

        # Scale features
        features_scaled = scaler.transform(features)

        # Predict cluster
        cluster = kmeans.predict(features_scaled)[0]

        # Get PCA coordinates
        pca_coords = pca.transform(features_scaled)[0]

        # Get cluster center
        center = cluster_centers.iloc[cluster].to_dict()

        # Generate description based on cluster
        descriptions = {
            0: "High Income, High Spending - Premium Customers",
            1: "High Income, Low Spending - Value Seekers",
            2: "Average Income, Average Spending - Regular Customers",
            3: "Low Income, Low Spending - Budget Conscious",
            4: "Low Income, High Spending - Aspirational Shoppers",
        }

        return jsonify(
            {
                "cluster": int(cluster),
                "description": descriptions.get(cluster, "Unknown Segment"),
                "center": center,
                "pca_coords": pca_coords.tolist(),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
