import streamlit as st
import numpy as np
import pandas as pd
import os
from PIL import Image

# Load Datasets
crop_df = pd.read_csv('Crop_recommendation.csv')
fertilizer_df = pd.read_csv('Fertilizer Prediction.csv')

# Display Header Image
img = Image.open("crop.png")
st.image(img)

#st.markdown("<h1 style='text-align: center;'>SMART AGRICULTURE SYSTEM</h1>", unsafe_allow_html=True)
st.sidebar.title("AgriYield")

# Select Feature (Include 'web' as the initial page)
page = st.sidebar.radio("Select Feature", ["web", "Crop Recommendation", "Fertilizer Recommendation"])

# -------------------- Crop Recommendation Function --------------------
def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    crop_df["distance"] = np.sqrt(
        (crop_df["N"] - nitrogen) ** 2 +
        (crop_df["P"] - phosphorus) ** 2 +
        (crop_df["K"] - potassium) ** 2 +
        (crop_df["temperature"] - temperature) ** 2 +
        (crop_df["humidity"] - humidity) ** 2 +
        (crop_df["ph"] - ph) ** 2 +
        (crop_df["rainfall"] - rainfall) ** 2
    )
    recommended_crop = crop_df.loc[crop_df["distance"].idxmin(), "label"]
    return recommended_crop

# -------------------- Fertilizer Recommendation Function --------------------
def recommend_fertilizer(soil_type, crop_type, temparature, humidity , nitrogen, phosphorous, potassium):
    # Ensure correct column names
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

# -------------------- Main Interface Logic --------------------
if page == "web":
    st.markdown("<h1 style='text-align: center;'>SMART AGRICULTURE SYSTEM</h1>", unsafe_allow_html=True)
    st.write("### Welcome to AgriYield - Your Smart Agriculture Assistant! 🌾🚜")
    st.write("Choose a feature from the sidebar to get started.")

elif page == "Crop Recommendation":
    st.markdown("<h1 style='text-align: center;'>Smart Crop Recommendation</h1>", unsafe_allow_html=True)
    #st.write("### Smart Crop Recommendation")
    st.sidebar.header("Enter Crop Details")

    nitrogen = st.sidebar.number_input("Nitrogen", min_value=0.0, max_value=140.0, value=0.0, step=0.1)
    phosphorus = st.sidebar.number_input("Phosphorus", min_value=0.0, max_value=145.0, value=0.0, step=0.1)
    potassium = st.sidebar.number_input("Potassium", min_value=0.0, max_value=205.0, value=0.0, step=0.1)
    temperature = st.sidebar.number_input("Temperature (°C)", min_value=0.0, max_value=51.0, value=0.0, step=0.1)
    humidity = st.sidebar.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    ph = st.sidebar.number_input("pH Level", min_value=0.0, max_value=14.0, value=0.0, step=0.1)
    rainfall = st.sidebar.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=0.0, step=0.1)

    if st.sidebar.button("Predict Crop"):
        if all(v == 0.0 for v in [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]):
            st.error("Please enter valid input values before predicting.")
        else:
            prediction = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
            st.success(f"🌾 Recommended Crop: **{prediction}**")

elif page == "Fertilizer Recommendation":
    st.markdown("<h1 style='text-align: center;Fertilizer Recommendation</h1>", unsafe_allow_html=True)
    st.sidebar.header("Enter Fertilizer Details")

    soil_type = st.sidebar.selectbox("Select Soil Type", ["Sandy", "Loamy", "Black", "Red", "Clayey"])
    crop_type = st.sidebar.selectbox("Select Crop Type", ["Wheat", "Maize", "Rice", "Sugarcane", "Cotton"])

    temperature = st.sidebar.number_input("Temperature (°C)", min_value=0.0, max_value=51.0, value=0.0, step=0.1)
    humidity = st.sidebar.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    nitrogen = st.sidebar.number_input("Nitrogen", min_value=0.0, max_value=140.0, value=0.0, step=0.1)
    phosphorus = st.sidebar.number_input("Phosphorus", min_value=0.0, max_value=145.0, value=0.0, step=0.1)
    potassium = st.sidebar.number_input("Potassium", min_value=0.0, max_value=205.0, value=0.0, step=0.1)

    if st.sidebar.button("Recommend Fertilizer"):
        if all(v == 0.0 for v in [temperature, humidity, nitrogen, phosphorus, potassium]):
            st.error("Please enter valid input values before predicting.")
        else:
            recommendation = recommend_fertilizer(soil_type, crop_type, temperature, humidity, nitrogen, phosphorus, potassium)
            st.success(f"🌿 Recommended Fertilizer: **{recommendation}**")
