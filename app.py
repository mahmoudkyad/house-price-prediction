import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import shap
import time

# =========================================
# Page Config
# =========================================

st.set_page_config(
    page_title="AI House Price Prediction",
    page_icon="🤖",
    layout="wide"
)

# =========================================
# Background + Animations
# =========================================

st.markdown("""
<style>

.stApp{
background: linear-gradient(-45deg,#0f2027,#203a43,#2c5364,#1c92d2);
background-size:400% 400%;
animation:gradient 12s ease infinite;
}

@keyframes gradient{
0%{background-position:0% 50%}
50%{background-position:100% 50%}
100%{background-position:0% 50%}
}

.title{
text-align:center;
font-size:65px;
font-weight:bold;
color:white;
margin-top:120px;
}

.subtitle{
text-align:center;
font-size:26px;
color:#e2e8f0;
margin-bottom:40px;
}

.stButton>button{
background:linear-gradient(135deg,#6366f1,#3b82f6);
color:white;
font-size:22px;
padding:16px 50px;
border-radius:15px;
border:none;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.12);
box-shadow:0px 10px 40px rgba(0,0,0,0.5);
}

.card{
background:#111827;
padding:25px;
border-radius:18px;
box-shadow:0 15px 40px rgba(0,0,0,0.4);
}

.metric{
font-size:45px;
font-weight:bold;
color:#22c55e;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# Session State
# =========================================

if "page" not in st.session_state:
    st.session_state.page = "start"

# =========================================
# START PAGE
# =========================================

if st.session_state.page == "start":

    st.markdown('<div class="title">🏠 AI House Price Prediction</div>',unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict Real Estate Prices Using Machine Learning</div>',unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("🚀 Start AI System"):
            st.session_state.page = "video"
            st.rerun()

    st.stop()

# =========================================
# VIDEO PAGE
# =========================================

if st.session_state.page == "video":

    st.title("🎬 AI System Loading")

    video_file = open("intro.mp4","rb")
    video_bytes = video_file.read()

    st.video(video_bytes, autoplay=True)

    time.sleep(6)

    st.session_state.page="loading"
    st.rerun()

    st.stop()

# =========================================
# LOADING PAGE
# =========================================

if st.session_state.page == "loading":

    st.title("🤖 AI is Preparing the Prediction Engine...")

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.02)
        progress.progress(i+1)

    st.session_state.page="app"
    st.rerun()

    st.stop()

# =========================================
# LOAD MODEL
# =========================================

model = joblib.load("house_price_mode55.pkl")

# =========================================
# HERO
# =========================================

st.title("🏡 AI Real Estate Prediction System")

st.write("Enter property features to estimate the house price")

st.markdown("")

# =========================================
# Layout
# =========================================

col1,col2,col3 = st.columns([1,1,1])

# =========================================
# INPUT CARD
# =========================================

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

# =========================================
# Prediction
# =========================================

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

# =========================================
# Explainable AI (SHAP)
# =========================================

with col3:

    st.markdown("### Explainable AI")

    try:

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(input_data)

        shap_df = pd.DataFrame({
            "Feature":input_data.columns,
            "Impact":shap_values[0]
        })

        fig3 = px.bar(
            shap_df,
            x="Impact",
            y="Feature",
            orientation="h"
        )

        st.plotly_chart(fig3,use_container_width=True)

    except:

        st.info("SHAP explanation unavailable")

# =========================================
# AI Assistant
# =========================================

st.markdown("---")

st.subheader("🤖 AI Assistant")

st.markdown(
"""
<a href="https://chat.openai.com" target="_blank">
<button style="
background:linear-gradient(90deg,#10b981,#06b6d4);
color:white;
padding:15px 30px;
border:none;
border-radius:10px;
font-size:18px;">
Open AI Chat Assistant
</button>
</a>
""",
unsafe_allow_html=True
)

# =========================================
# Footer
# =========================================

st.markdown("---")

st.write("AI Real Estate Prediction System | Machine Learning Graduation Project")
