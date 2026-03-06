import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import shap
import numpy as np
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
# Background + CSS
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
font-size:20px;
padding:14px 40px;
border-radius:12px;
border:none;
transition:0.3s;
}

.stButton>button:hover{
transform:scale(1.1);
}

.card{
background:#111827;
padding:25px;
border-radius:18px;
box-shadow:0 10px 40px rgba(0,0,0,0.5);
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
    st.markdown('<div class="subtitle">Machine Learning Real Estate System</div>',unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,1,1])

    with col2:
        if st.button("🚀 Start System"):
            st.session_state.page = "video"
            st.rerun()

    st.stop()

# =========================================
# VIDEO PAGE
# =========================================

if st.session_state.page == "video":

    st.title("🎬 AI Introduction")

    video_file = open("intro.mp4","rb")
    video_bytes = video_file.read()

    st.video(video_bytes)

    time.sleep(6)

    st.session_state.page="loading"
    st.rerun()

    st.stop()

# =========================================
# LOADING PAGE
# =========================================

if st.session_state.page == "loading":

    st.title("🤖 Loading AI Model")

    progress = st.progress(0)

    for i in range(100):
        time.sleep(0.02)
        progress.progress(i+1)

    st.session_state.page="app"
    st.rerun()

    st.stop()

# =========================================
# Load Model
# =========================================

model = joblib.load("house_price_mode55.pkl")

# =========================================
# HERO
# =========================================

st.title("🏡 AI Real Estate Prediction System")

st.write("Enter property information to predict the price")

# =========================================
# Layout
# =========================================

col1,col2,col3 = st.columns([1,1,1])

# =========================================
# INPUT
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

input_data = pd.DataFrame({

"Overall Qual":[OverallQual],
"Gr Liv Area":[GrLivArea],
"Garage Cars":[GarageCars],
"Total Bsmt SF":[TotalBsmtSF],
"Year Built":[YearBuilt]

})

# =========================================
# Prediction
# =========================================

with col2:

    st.markdown("### Prediction")

    if st.button("💰 Predict Price"):

        prediction = model.predict(input_data)[0]

        st.markdown(
        f"""
        <div class="card">
        <h3>Estimated Price</h3>
        <div class="metric">${int(prediction):,}</div>
        </div>
        """,
        unsafe_allow_html=True
        )

        df_price = pd.DataFrame({

        "Type":["Prediction"],
        "Price":[prediction]

        })

        fig = px.bar(df_price,x="Type",y="Price",color="Type")

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

        fig2 = px.bar(
        shap_df,
        x="Impact",
        y="Feature",
        orientation="h",
        color="Impact"
        )

        st.plotly_chart(fig2,use_container_width=True)

    except:

        st.info("SHAP explanation unavailable")

# =========================================
# AI Chatbot
# =========================================

st.markdown("---")

st.title("🤖 AI Real Estate Assistant")

if "messages" not in st.session_state:
    st.session_state.messages=[]

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask about house prices, features, or the model...")

if prompt:

    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("user"):
        st.write(prompt)

    response = ""

    if "price" in prompt.lower():
        response="House prices depend on quality, size, garage capacity, basement area, and year built."

    elif "model" in prompt.lower():
        response="This system uses a Machine Learning model trained on real estate data to predict house prices."

    else:
        response="I can help explain house prices, features, or how the AI prediction works."

    st.session_state.messages.append({"role":"assistant","content":response})

    with st.chat_message("assistant"):
        st.write(response)

# =========================================
# Footer
# =========================================

st.markdown("---")

st.write("AI Real Estate Prediction System | Graduation Project")
