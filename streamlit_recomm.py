import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from sklearn.base import BaseEstimator, RegressorMixin

class EnsembleRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, base_models=None):
        # Assume base_models is a list of trained models
        self.base_models = base_models if base_models is not None else []

    def fit(self, X, y):
        # Fit each model (this would be done during training)
        for model in self.base_models:
            model.fit(X, y)
        return self

    def predict(self, X):
        # Aggregate predictions from each model (simple averaging)
        predictions = np.column_stack([model.predict(X) for model in self.base_models])
        return np.mean(predictions, axis=1)

# Load the models
@st.cache_resource
def load_models():
    recommendation_model = load('./ensemble_recommendation_model.joblib')
    demand_data = load('./high_demand_df.joblib')
    return recommendation_model, demand_data

recommendation_model, demand_data = load_models()

# Streamlit app
st.title("Retail Management System")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Demand Forecasting", "Customer Recommendations"])

if page == "Demand Forecasting":
    st.header("Demand Forecasting")

    # Display the high demand data
    st.subheader("High Demand Products")
    st.dataframe(demand_data)

    # Interactive components for user input
    year = st.number_input("Select Year", min_value=2000, max_value=2100, value=2024)
    month = st.selectbox("Select Month", options=list(range(1, 13)), index=0)
    day = st.selectbox("Select Day", options=list(range(1, 32)), index=0)
    
    if st.button("Show Demand Data"):
        # Filter the demand data based on user input
        filtered_data = demand_data[(demand_data['year'] == year) & 
                                    (demand_data['month'] == month) & 
                                    (demand_data['day'] == day)]
        st.write("Filtered Demand Data:")
        st.dataframe(filtered_data)

elif page == "Customer Recommendations":
    st.header("Customer Recommendations")

    # User inputs for customer features
    customer_age = st.number_input("Customer Age", min_value=0)
    customer_income = st.number_input("Customer Income", min_value=0)
    product_price = st.number_input("Product Price", min_value=0)
    product_category = st.selectbox("Product Category", options=["Electronics", "Clothing", "Grocery", "Home", "Other"])

    if st.button("Get Recommendations"):
        # Combine inputs into a feature vector
        input_data = np.array([[customer_age, customer_income, product_price]])

        # Get recommendations from the model
        recommendations = recommendation_model.predict(input_data)

        st.subheader("Product Recommendations")
        st.write(recommendations)

    # Optionally display the top recommended products
    if st.button("Show Top Products"):
        # Example: Just displaying high demand products
        st.write("Top High Demand Products:")
        st.dataframe(demand_data.sort_values(by='demand', ascending=False).head(10))

