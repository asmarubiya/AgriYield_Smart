import streamlit as st
import pandas as pd
import numpy as np

# Load Fertilizer Dataset
fertilizer_df = pd.read_csv('Fertilizer Prediction.csv')

# Function to recommend fertilizer
def recommend_fertilizer(soil_type, crop_type, temparature, humidity , nitrogen, phosphorous, potassium):
    fertilizer_df["distance"] = np.sqrt(
        (fertilizer_df["Soil Type"] == soil_type).astype(int) +
        (fertilizer_df["Crop Type"] == crop_type).astype(int) +
        (fertilizer_df["Temparature"] - temparature) ** 2 +
        (fertilizer_df["Humidity "] - humidity ) ** 2 +
        (fertilizer_df["Nitrogen"] - nitrogen) ** 2 +
        (fertilizer_df["Phosphorous"] - phosphorous) ** 2 +
        (fertilizer_df["Potassium"] - potassium) ** 2
    )
    recommended_fertilizer = fertilizer_df.loc[fertilizer_df["distance"].idxmin(), "Fertilizer Name"]
    return recommended_fertilizer

# UI for Fertilizer Recommendation
st.header("🌿 Fertilizer Recommendation System")
st.sidebar.header("Enter Fertilizer Details")

# Dropdowns for categorical values
soil_type = st.sidebar.selectbox("Select Soil Type", ["Sandy", "Loamy", "Black", "Red", "Clayey"])
crop_type = st.sidebar.selectbox("Select Crop Type", ["Wheat", "Maize", "Rice", "Sugarcane", "Cotton"])

# Input Fields
temperature = st.sidebar.number_input("Temperature (°C)", min_value=0.0, max_value=51.0, value=0.0, step=0.1)
humidity = st.sidebar.number_input("Humidity  (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
nitrogen = st.sidebar.number_input("Nitrogen", min_value=0.0, max_value=140.0, value=0.0, step=0.1)
phosphorus = st.sidebar.number_input("Phosphorus", min_value=0.0, max_value=145.0, value=0.0, step=0.1)
potassium = st.sidebar.number_input("Potassium", min_value=0.0, max_value=205.0, value=0.0, step=0.1)

# Predict Fertilizer
if st.sidebar.button("Recommend Fertilizer"):
    if all(v == 0.0 for v in [temperature, humidity, nitrogen, phosphorus, potassium]):
        st.error("Please enter valid values before predicting.")
    else:
        recommendation = recommend_fertilizer(soil_type, crop_type, temperature, humidity, nitrogen, phosphorus, potassium)
        st.success(f"🌿 Recommended Fertilizer: **{recommendation}**")
