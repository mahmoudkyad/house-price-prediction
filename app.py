import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# ==================================
# Page Config
# ==================================

st.set_page_config(
    page_title="AI House Price Predictor",
    page_icon="🏠",
    layout="wide"
)
# ===============================
# Start Button State
# ===============================

if "started" not in st.session_state:
    st.session_state.started = False

# ===============================
# Start Screen
# ===============================

if not st.session_state.started:

    st.title("🏠 AI House Price Prediction")

    st.write("Welcome to the AI Real Estate Prediction System")

    if st.button("Start"):

        st.session_state.started = True
        st.rerun()

    st.stop()
    # ===============================
# Intro Video
# ===============================

st.video("intro.mp4")

st.markdown("---")
# ==================================
# Custom CSS
# ==================================

st.markdown("""
<style>

.main {
background-color:#0b1120;
}

.block-container{
padding-top:2rem;
}

h1,h2,h3{
color:white;
}

p{
color:#cbd5e1;
}

.card{
background:#111827;
padding:25px;
border-radius:16px;
box-shadow:0 10px 30px rgba(0,0,0,0.4);
}

.metric{
font-size:40px;
font-weight:bold;
color:#22c55e;
}

.stButton>button{

background:linear-gradient(90deg,#3b82f6,#6366f1);
color:white;
font-size:18px;
border-radius:12px;
padding:12px 28px;
border:none;

}

.stButton>button:hover{

background:linear-gradient(90deg,#2563eb,#4f46e5);

}

</style>
""", unsafe_allow_html=True)

# ==================================
# Load Model
# ==================================

model = joblib.load("house_price_mode55.pkl")

# ==================================
# HERO IMAGE
# ==================================

st.image("hero.png", use_container_width=True)

st.markdown("##")

# ==================================
# Layout
# ==================================

col1,col2,col3 = st.columns([1,1,1])

# ==================================
# INPUT CARD
# ==================================

with col1:

    st.markdown("### Property Features")

    OverallQual = st.slider("Overall Quality",1,10,5)

    GrLivArea = st.number_input(
        "Living Area (sq ft)",
        500,5000,1500
    )

    GarageCars = st.slider(
        "Garage Capacity",
        0,4,2
    )

    TotalBsmtSF = st.number_input(
        "Basement Area",
        0,3000,800
    )

    YearBuilt = st.slider(
        "Year Built",
        1900,2024,2000
    )

# ==================================
# Prediction Card
# ==================================

with col2:

    st.markdown("### Prediction Result")

    input_data = pd.DataFrame({

    "Overall Qual":[OverallQual],
    "Gr Liv Area":[GrLivArea],
    "Garage Cars":[GarageCars],
    "Total Bsmt SF":[TotalBsmtSF],
    "Year Built":[YearBuilt]

    })

    if st.button("💰 Predict Price"):

        prediction = model.predict(input_data)[0]

        st.markdown(
        f"""
        <div class="card">
        <h3>Estimated House Price</h3>
        <div class="metric">${int(prediction):,}</div>
        </div>
        """,
        unsafe_allow_html=True
        )

        price_data = pd.DataFrame({

        "Type":["Predicted Price"],
        "Price":[prediction]

        })

        fig = px.bar(
            price_data,
            x="Type",
            y="Price",
            color="Type"
        )

        st.plotly_chart(fig,use_container_width=True)

# ==================================
# Feature Importance
# ==================================

with col3:

    st.markdown("### Feature Importance")

    try:

        importance = model.feature_importances_

        features = [
        "Overall Qual",
        "Gr Liv Area",
        "Garage Cars",
        "Total Bsmt SF",
        "Year Built"
        ]

        df = pd.DataFrame({
        "Feature":features,
        "Importance":importance
        })

        fig2 = px.bar(
            df,
            x="Importance",
            y="Feature",
            orientation="h"
        )

        st.plotly_chart(fig2,use_container_width=True)

    except:
        st.info("Feature importance unavailable.")

# ==================================
# Footer
# ==================================

st.markdown("---")

st.write(
"AI Real Estate Prediction System | Machine Learning Project"
)

