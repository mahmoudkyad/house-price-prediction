import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import shap
import time

# =====================================
# Page Config
# =====================================

st.set_page_config(
    page_title="AI House Price Predictor",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# CSS
# =====================================

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
font-size:60px;
font-weight:bold;
color:white;
margin-top:120px;
}

.subtitle{
text-align:center;
font-size:24px;
color:white;
}

.stButton>button{
background:linear-gradient(90deg,#3b82f6,#6366f1);
color:white;
font-size:20px;
border-radius:12px;
padding:14px 40px;
border:none;
}

.stButton>button:hover{
transform:scale(1.08);
}

.card{
background:#111827;
padding:25px;
border-radius:18px;
box-shadow:0 10px 30px rgba(0,0,0,0.4);
}

.metric{
font-size:40px;
font-weight:bold;
color:#22c55e;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# Session State
# =====================================

if "page" not in st.session_state:
    st.session_state.page="start"

# =====================================
# START PAGE
# =====================================

if st.session_state.page=="start":

    st.markdown('<div class="title">🏠 AI House Price Prediction</div>',unsafe_allow_html=True)

    st.markdown('<div class="subtitle">Machine Learning Real Estate System</div>',unsafe_allow_html=True)

    col1,col2,col3=st.columns([1,1,1])

    with col2:
        if st.button("🚀 Start System"):
            st.session_state.page="video"
            st.rerun()

    st.stop()

# =====================================
# VIDEO PAGE
# =====================================

if st.session_state.page=="video":

    st.markdown(
    """
    <video autoplay muted width="100%">
        <source src="intro.mp4" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
    )

    time.sleep(6)

    st.session_state.page="app"
    st.rerun()

    st.stop()

# =====================================
# Load Model
# =====================================

model = joblib.load("house_price_mode55.pkl")

# =====================================
# HERO
# =====================================

st.title("🏡 AI Real Estate Prediction System")

st.write("Enter house features to predict the price")

# =====================================
# Layout
# =====================================

col1,col2,col3=st.columns([1,1,1])

# =====================================
# INPUT
# =====================================

with col1:

    st.markdown("### Property Features")

    OverallQual=st.slider("Overall Quality",1,10,5)

    GrLivArea=st.number_input("Living Area",500,5000,1500)

    GarageCars=st.slider("Garage Capacity",0,4,2)

    TotalBsmtSF=st.number_input("Basement Area",0,3000,800)

    YearBuilt=st.slider("Year Built",1900,2024,2000)

# =====================================
# Prediction
# =====================================

with col2:

    st.markdown("### Prediction Result")

    input_data=pd.DataFrame({

    "Overall Qual":[OverallQual],
    "Gr Liv Area":[GrLivArea],
    "Garage Cars":[GarageCars],
    "Total Bsmt SF":[TotalBsmtSF],
    "Year Built":[YearBuilt]

    })

    if st.button("💰 Predict Price"):

        prediction=model.predict(input_data)[0]

        st.markdown(
        f"""
        <div class="card">
        <h3>Estimated House Price</h3>
        <div class="metric">${int(prediction):,}</div>
        </div>
        """,
        unsafe_allow_html=True
        )

        df_price=pd.DataFrame({

        "Type":["Prediction"],
        "Price":[prediction]

        })

        fig=px.bar(df_price,x="Type",y="Price",color="Type")

        st.plotly_chart(fig,use_container_width=True)

# =====================================
# SHAP Explainable AI
# =====================================

with col3:

    st.markdown("### Explainable AI")

    try:

        explainer=shap.TreeExplainer(model)

        shap_values=explainer.shap_values(input_data)

        df=pd.DataFrame({

        "Feature":input_data.columns,
        "Impact":shap_values[0]

        })

        fig2=px.bar(df,x="Impact",y="Feature",orientation="h")

        st.plotly_chart(fig2,use_container_width=True)

    except:

        st.info("SHAP explanation unavailable")

# =====================================
# ChatGPT Link
# =====================================

st.markdown("---")

st.subheader("🤖 AI Assistant")

st.write("Click the button to chat with AI about house prices")

st.markdown(
"""
<a href="https://chat.openai.com" target="_blank">
<button style="
background:linear-gradient(90deg,#10b981,#06b6d4);
color:white;
padding:15px 30px;
border:none;
border-radius:10px;
font-size:18px;
">
Open AI Chat Assistant
</button>
</a>
""",
unsafe_allow_html=True
)

# =====================================
# Footer
# =====================================

st.markdown("---")

st.write("AI Real Estate Prediction System | Machine Learning Project")
