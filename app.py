import streamlit as st
import pandas as pd
from joblib import load
import numpy as np

# Load pre-trained models
# @st.cache_resource
# def load_models():
#     demand_forecasting_model = load('demand_forecasting_model.joblib')
#     inventory_management_model = load('inventory_management_model.joblib')
#     customer_segmentation_model = load('customer_segmentation_model.joblib')
#     recommendation_model = load('recommendation_model.joblib')
#     return (demand_forecasting_model, inventory_management_model, customer_segmentation_model, recommendation_model)

# demand_forecasting_model, inventory_management_model, customer_segmentation_model, recommendation_model = load_models()

st.title("Retail Management System")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Demand Forecasting", "Inventory Management", "Customer Segmentation & Recommendations"])

if page == "Demand Forecasting":
    st.header("Demand Forecasting")

    # User input for date selection
    year = st.number_input("Select Year", min_value=2000, max_value=2100, value=2024)
    month = st.selectbox("Select Month", options=list(range(1, 13)), index=0)
    day = st.selectbox("Select Day", options=list(range(1, 32)), index=0)

    # User input for promotional impact and other factors
    promo_effect = st.slider("Promotional Impact (0-100%)", min_value=0, max_value=100, value=50)
    seasonality_factor = st.slider("Seasonality Factor (0-100%)", min_value=0, max_value=100, value=50)
    external_factor = st.slider("External Factors Impact (0-100%)", min_value=0, max_value=100, value=50)

    if st.button("Predict Demand"):
        # Combine inputs into a feature vector (this should be aligned with how your model was trained)
        input_data = np.array([[year, month, day, promo_effect, seasonality_factor, external_factor]])

        # Predict future sales
        predictions = demand_forecasting_model.predict(input_data)

        st.subheader("Predicted Future Sales")
        st.line_chart(predictions)

elif page == "Inventory Management":
    st.header("Inventory Management")

    # User input for demand forecast, current inventory, and lead time
    forecasted_demand = st.number_input("Forecasted Demand", min_value=0)
    current_inventory = st.number_input("Current Inventory Levels", min_value=0)
    lead_time = st.number_input("Lead Time (in days)", min_value=0)

    if st.button("Optimize Inventory"):
        # Combine inputs into a feature vector
        input_data = np.array([[forecasted_demand, current_inventory, lead_time]])

        # Predict reorder quantities
        reorder_quantities = inventory_management_model.predict(input_data)

        st.subheader("Recommended Reorder Quantities and Timing")
        st.write(reorder_quantities)

elif page == "Customer Segmentation & Recommendations":
    st.header("Customer Segmentation & Recommendations")

    # User input for customer and product details
    customer_age = st.number_input("Customer Age", min_value=0)
    customer_income = st.number_input("Customer Income", min_value=0)
    product_price = st.number_input("Product Price", min_value=0)
    product_category = st.selectbox("Product Category", options=["Electronics", "Clothing", "Grocery", "Home", "Other"])

    if st.button("Get Recommendations"):
        # Combine inputs into a feature vector
        input_data = np.array([[customer_age, customer_income, product_price]])

        # Segment customer and recommend products
        segments = customer_segmentation_model.predict(input_data)
        recommendations = recommendation_model.recommend(input_data)

        st.subheader("Customer Segmentation")
        st.write(segments)

        st.subheader("Product Recommendations")
        st.write(recommendations)
