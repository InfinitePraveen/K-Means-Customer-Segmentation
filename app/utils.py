import pandas as pd
import numpy as np
import joblib
import os


def load_models():
    """Load all saved models"""
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    scaler = joblib.load(os.path.join(model_path, "scaler.pkl"))
    kmeans = joblib.load(os.path.join(model_path, "kmeans_model.pkl"))
    pca = joblib.load(os.path.join(model_path, "pca_model.pkl"))
    return scaler, kmeans, pca


def get_cluster_description(cluster_id):
    """Get human-readable description for each cluster"""
    descriptions = {
        0: "Premium Customers - High income, high spending. Your most valuable segment.",
        1: "Value Seekers - High income but low spending. Potential for upselling.",
        2: "Regular Customers - Average income and spending. Stable segment.",
        3: "Budget Conscious - Low income, low spending. Price-sensitive customers.",
        4: "Aspirational Shoppers - Low income but high spending. Brand-loyal customers.",
    }
    return descriptions.get(cluster_id, "Unknown Segment")


def generate_recommendations(cluster_id):
    """Generate business recommendations based on cluster"""
    recommendations = {
        0: [
            "Offer premium loyalty programs",
            "Exclusive early access to new products",
            "Personal shopping assistant service",
        ],
        1: [
            "Highlight value-for-money products",
            "Bundle deals and package offers",
            "Educational content on product value",
        ],
        2: [
            "Maintain consistent quality",
            "Regular promotional offers",
            "Email newsletters with personalized deals",
        ],
        3: [
            "Budget-friendly product lines",
            "Clear pricing and transparent costs",
            "Discount coupons and seasonal sales",
        ],
        4: [
            "Buy-now-pay-later options",
            "Installment payment plans",
            "Social proof and reviews",
        ],
    }
    return recommendations.get(cluster_id, [])
