import streamlit as st
import time

# --------------------------------
# Page Config
# --------------------------------
st.set_page_config(
    page_title="AI House Price Prediction",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------
# Background + Button Animation
# --------------------------------
st.markdown("""
<style>

/* خلفية متحركة */
.stApp {
background: linear-gradient(-45deg,#1e3c72,#2a5298,#6dd5ed,#2193b0);
background-size: 400% 400%;
animation: gradient 15s ease infinite;
}

@keyframes gradient {
0%{background-position:0% 50%}
50%{background-position:100% 50%}
100%{background-position:0% 50%}
}

/* زرار متحرك */
.stButton > button {
background: linear-gradient(135deg,#00c6ff,#0072ff);
color:white;
padding:18px 45px;
border-radius:15px;
font-size:22px;
font-weight:bold;
border:none;
transition:0.3s;
}

.stButton > button:hover{
transform:scale(1.1);
box-shadow:0px 10px 30px rgba(0,0,0,0.4);
}

/* عنوان */
.title{
text-align:center;
font-size:60px;
font-weight:bold;
color:white;
margin-top:100px;
}

.subtitle{
text-align:center;
font-size:25px;
color:white;
margin-bottom:50px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# Session State
# --------------------------------
if "start" not in st.session_state:
    st.session_state.start=False

if "video_done" not in st.session_state:
    st.session_state.video_done=False

# --------------------------------
# الصفحة الأولى
# --------------------------------
if not st.session_state.start:

    st.markdown('<div class="title">🏠 AI House Price Prediction</div>',unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict house prices using Artificial Intelligence</div>',unsafe_allow_html=True)

    col1,col2,col3=st.columns([1,1,1])

    with col2:
        if st.button("START"):
            st.session_state.start=True
            st.rerun()

# --------------------------------
# الفيديو
# --------------------------------
elif st.session_state.start and not st.session_state.video_done:

    st.title("🎬 AI Introduction")

    video_file = open("intro.mp4","rb")
    video_bytes = video_file.read()

    st.video(video_bytes, autoplay=True)

    time.sleep(6)

    st.session_state.video_done=True
    st.rerun()

# --------------------------------
# واجهة التنبؤ
# --------------------------------
else:

    st.title("🏡 House Price Prediction")

    st.write("Enter house features")

    col1,col2=st.columns(2)

    with col1:
        GrLivArea = st.number_input("Living Area",500,5000,1500)
        OverallQual = st.slider("Overall Quality",1,10,5)
        GarageCars = st.slider("Garage Capacity",0,4,2)

    with col2:
        TotalBsmtSF = st.number_input("Basement Area",0,3000,800)
        YearBuilt = st.number_input("Year Built",1900,2025,2005)

    if st.button("🔮 Predict Price"):

        # مثال فقط للتجربة
        price = (GrLivArea*120)+(OverallQual*10000)+(GarageCars*5000)

        st.success(f"💰 Predicted Price: ${price:,.0f}")
