import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# Load Crop Dataset
crop_df = pd.read_csv('Crop_recommendation.csv')

# Function to predict the crop
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

# Function to show crop image
def show_crop_image(crop_name):
    image_path = os.path.join('crop_images', crop_name.lower() + '.jpg')
    if os.path.exists(image_path):
        st.image(image_path, caption=f"Recommended crop: {crop_name}", use_column_width=True)

# UI for Crop Recommendation
st.header("🌾 Crop Recommendation System")
st.sidebar.header("Enter Crop Details")

# Input Fields
nitrogen = st.sidebar.number_input("Nitrogen", min_value=0.0, max_value=140.0, value=0.0, step=0.1)
phosphorus = st.sidebar.number_input("Phosphorus", min_value=0.0, max_value=145.0, value=0.0, step=0.1)
potassium = st.sidebar.number_input("Potassium", min_value=0.0, max_value=205.0, value=0.0, step=0.1)
temperature = st.sidebar.number_input("Temperature (°C)", min_value=0.0, max_value=51.0, value=0.0, step=0.1)
humidity = st.sidebar.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
ph = st.sidebar.number_input("pH Level", min_value=0.0, max_value=14.0, value=0.0, step=0.1)
rainfall = st.sidebar.number_input("Rainfall (mm)", min_value=0.0, max_value=500.0, value=0.0, step=0.1)

# Predict Crop
if st.sidebar.button("Predict"):
    if all(v == 0.0 for v in [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]):
        st.error("Please enter valid values before predicting.")
    else:
        prediction = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)
        st.success(f"🌾 Recommended Crop: **{prediction}**")
        show_crop_image(prediction)
