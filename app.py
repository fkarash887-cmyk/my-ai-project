import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import streamlit.components.v1 as components

# ------------------- КОНФИГУРАЦИЯ -------------------
st.set_page_config(
    page_title="Abbas AI Portfolio",
    layout="wide"
)

# ------------------- ДИЗАЙН -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
[data-testid="stAppViewContainer"] { background-color: #000000 !important; }
* { color: #00ff00 !important; font-family: 'Share Tech Mono', monospace !important; }
.abbas-card { border: 2px solid #00ff00; padding: 20px; text-align: center; margin-bottom: 20px; }
.stMetric { border: 1px solid #00ff00; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ------------------- МОДЕЛЬ -------------------
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ------------------- ШАПКА -------------------
st.markdown("<div class='abbas-card'><h1>РАЗРАБОТЧИК: АББАС</h1><h3>ТЕЛ: +996 559 021 309</h3></div>", unsafe_allow_html=True)

# ------------------- КОНТЕНТ -------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Анализатор фото")
    uploaded = st.file_uploader("Загрузить изображение", type=["jpg", "jpeg", "png"])
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        res = model(img)[0]
        count = sum(1 for b in res.boxes if int(b.cls) == 0)
        st.image(cv2.cvtColor(res.plot(), cv2.COLOR_BGR2RGB))
        st.metric("ЛЮДЕЙ НА ФОТО", count)

with col2:
    st.subheader("🌐 Мои проекты")
    # Здесь можно поставить ссылку на другой твой сайт
    components.iframe("https://docs.ultralytics.com/", height=500)

st.markdown("---")
st.subheader("📹 Работа с камерой")
cam = st.camera_input("Сделать снимок")

if cam:
    img_cam = cv2.imdecode(np.frombuffer(cam.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    res_cam = model(img_cam)[0]
    count_cam = sum(1 for b in res_cam.boxes if int(b.cls) == 0)
    st.image(cv2.cvtColor(res_cam.plot(), cv2.COLOR_BGR2RGB))
    st.success(f"Аббас, система обнаружила {count_cam} чел.")
