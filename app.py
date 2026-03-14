import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import streamlit.components.v1 as components

# ------------------- КОНФИГУРАЦИЯ -------------------
st.set_page_config(
    page_title=f"Abbas | AI Portfolio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------- ХАКЕРСКИЙ ДИЗАЙН -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #000000 !important;
}

* {
    color: #00ff00 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

h1 {
    text-align: center;
    text-shadow: 0 0 15px #00ff00;
    border-bottom: 2px solid #00ff00;
}

.stImage, iframe, [data-testid="stMetricValue"], .stCameraInput {
    border: 1px solid #00ff00 !important;
    box-shadow: 0 0 10px #00ff00;
}

/* Персональный блок Аббаса */
.abbas-card {
    border: 2px double #00ff00;
    padding: 20px;
    margin-bottom: 20px;
    text-align: center;
    background: rgba(0, 255, 0, 0.05);
}
</style>
""", unsafe_allow_html=True)

# ------------------- ЗАГРУЗКА МОДЕЛИ -------------------
@st.cache_resource
def load_yolo():
    return YOLO("yolov8n.pt")

model = load_yolo()

# ------------------- ШАПКА САЙТА -------------------
st.markdown("<h1>PEOPLE COUNTING SYSTEM</h1>", unsafe_allow_html=True)

# ТВОИ ДАННЫЕ ЗДЕСЬ
st.markdown(f"""
<div class="abbas-card">
    <h2 style="margin:0;">РАЗРАБОТЧИК: АББАС</h2>
    <p style="font-size: 22px; margin:10px 0;">CONTACT: +996 559 021 309</p>
    <p style="font-size: 14px; color: #008800 !important;">ACCESS LEVEL: ADMINISTRATOR</p>
</div>
""", unsafe_allow_html=True)

# ------------------- КОНТЕНТ -------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📷 СКАНЕР ИЗОБРАЖЕНИЙ")
    uploaded = st.file_uploader("Загрузить объект...", type=["jpg", "png", "jpeg"])
    
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        results = model(img)[0]
        
        people_count = sum(1 for b in results.boxes if int(b.cls) == 0)
        st.image(cv2.cvtColor(results.plot(), cv2.COLOR_BGR2RGB))
        st.metric("ОБНАРУЖЕНО ЛЮДЕЙ", people_count)

with col2:
    st.subheader("🌐 ВНЕШНИЕ ПРОЕКТЫ")
    # Сюда можно поставить ссылку на твой GitHub или другой проект
    components.iframe("https://docs.ultralytics.com/", height=500)

st.markdown("---")

# ------------------- КАМЕРА -------------------
st.subheader("📹 ЖИВОЙ ПОТОК")
cam_img = st.camera_input("СДЕЛАТЬ СНИМОК ДЛЯ АНАЛИЗА")

if cam_img:
    bytes_data = cam_img.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    res = model(cv2_img)[0]
    count = sum(1 for b in res.boxes if int(b.cls) == 0)
    
    st.image(cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB))
    st.success(f"АББАС, АНАЛИЗ ЗАВЕРШЕН. В КАДРЕ: {count}")

st.markdown("<p style='text-align:center;'>Created by Abbas | 2026</p>", unsafe_allow_html=True)
