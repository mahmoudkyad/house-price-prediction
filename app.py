import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Page Config
# ==============================

st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# ==============================
# Load Model
# ==============================

model = joblib.load("house_price_mode55.pkl")

# ==============================
# Title
# ==============================

st.title("🏠 House Price Prediction")
st.write("Enter house features to estimate the price")

# ==============================
# Input Section
# ==============================

st.sidebar.header("Property Details")

OverallQual = st.sidebar.slider(
    "Overall Quality",
    1,10,5
)

GrLivArea = st.sidebar.number_input(
    "Living Area (sq ft)",
    500,5000,1500
)

GarageCars = st.sidebar.slider(
    "Garage Capacity",
    0,4,2
)

TotalBsmtSF = st.sidebar.number_input(
    "Basement Area",
    0,3000,800
)

YearBuilt = st.sidebar.slider(
    "Year Built",
    1900,2024,2000
)

# ==============================
# Create DataFrame
# ==============================

input_data = pd.DataFrame({

"Overall Qual":[OverallQual],
"Gr Liv Area":[GrLivArea],
"Garage Cars":[GarageCars],
"Total Bsmt SF":[TotalBsmtSF],
"Year Built":[YearBuilt]

})

# ==============================
# Prediction
# ==============================

if st.button("Predict Price 💰"):

    prediction = model.predict(input_data)[0]

    st.success(f"💰 Estimated House Price: ${int(prediction):,}")

    # ==============================
    # Chart
    # ==============================

    fig, ax = plt.subplots()

    ax.bar(["Predicted Price"], [prediction])

    ax.set_ylabel("Price ($)")
    ax.set_title("Predicted House Price")

    st.pyplot(fig)

# ==============================
# Feature Importance
# ==============================

st.subheader("📊 Feature Importance")

try:

    importance = model.feature_importances_

    features = [
        "Overall Qual",
        "Gr Liv Area",
        "Garage Cars",
        "Total Bsmt SF",
        "Year Built"
    ]

    importance_df = pd.DataFrame({
        "Feature":features,
        "Importance":importance
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )

    fig2, ax2 = plt.subplots()

    ax2.barh(
        importance_df["Feature"],
        importance_df["Importance"]
    )

    ax2.set_title("Feature Importance")

    st.pyplot(fig2)

except:
    st.info("Feature importance not available for this model.")

# ==============================
# Footer
# ==============================

st.markdown("---")
st.write("Machine Learning House Price Prediction Project")