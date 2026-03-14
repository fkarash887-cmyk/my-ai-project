import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO

# ------------------- КОНФИГУРАЦИЯ -------------------
st.set_page_config(
    page_title="Abbas AI Portfolio",
    layout="wide"
)

# ------------------- ДИЗАЙН (ХАКЕРСКИЙ) -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
[data-testid="stAppViewContainer"] { background-color: #000000 !important; }
* { color: #00ff00 !important; font-family: 'Share Tech Mono', monospace !important; }

.abbas-card { 
    border: 2px solid #00ff00; 
    padding: 20px; 
    text-align: center; 
    margin-bottom: 20px; 
    box-shadow: 0 0 15px #00ff00; 
}

.stMetric { border: 1px solid #00ff00; padding: 10px; background: rgba(0,255,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ------------------- ЗАГРУЗКА ИИ -------------------
@st.cache_resource
def load_yolo():
    return YOLO("yolov8n.pt")

model = load_yolo()

# ------------------- ПАНЕЛЬ АББАСА -------------------
st.markdown(f"""
<div class='abbas-card'>
    <h1>DEVELOPER: ABBAS</h1>
    <h3 style="letter-spacing: 2px;">CONTACT: +996 559 021 309</h3>
    <p style="color: #008800 !important;">AI SCANNER: ACTIVE</p>
</div>
""", unsafe_allow_html=True)

# ------------------- ОСНОВНОЙ КОНТЕНТ -------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📷 АНАЛИЗ ФОТО")
    uploaded = st.file_uploader("Загрузить файл", type=["jpg", "jpeg", "png"])
    
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        # Запуск ИИ
        results = model(img)[0]
        count = sum(1 for b in results.boxes if int(b.cls) == 0)
        
        st.image(cv2.cvtColor(results.plot(), cv2.COLOR_BGR2RGB), use_container_width=True)
        st.metric("НАЙДЕНО ЛЮДЕЙ", count)

with col2:
    st.subheader("🛠 ТЕХНОЛОГИИ")
    st.markdown("""
    - **AI Engine:** YOLOv8
    - **Frontend:** Streamlit
    - **Vision:** OpenCV
    - **Language:** Python 3.11
    """)
    st.write("---")
    wa_link = "https://wa.me/996559021309"
    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; cursor:pointer; padding:10px; border:1px solid #00ff00; background:#051a05; color:#00ff00;">НАПИСАТЬ АББАСУ</button></a>', unsafe_allow_html=True)

st.markdown("---")

# ------------------- КАМЕРА С ИИ -------------------
st.subheader("📹 ЖИВОЙ СКАНЕР (ВЕБ-КАМЕРА)")
cam = st.camera_input("СДЕЛАТЬ СНИМОК ДЛЯ АНАЛИЗА ИИ")

if cam:
    img_cam = cv2.imdecode(np.frombuffer(cam.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    
    # Запуск ИИ на снимке с камеры
    res_cam = model(img_cam)[0]
    final_img = res_cam.plot()
    count_cam = sum(1 for b in res_cam.boxes if int(b.cls) == 0)
    
    st.image(cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB), caption="Результат сканирования")
    st.success(f"Аббас, система обнаружила людей в кадре: {count_cam}")

st.markdown("<p style='text-align:center; opacity:0.3; margin-top:50px;'>AI SCANNER v4.0 | Created by Abbas</p>", unsafe_allow_html=True)
