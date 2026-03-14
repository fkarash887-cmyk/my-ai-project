import streamlit as st
import cv2
import numpy as np

# ------------------- КОНФИГУРАЦИЯ -------------------
st.set_page_config(
    page_title="Abbas Portfolio",
    layout="wide"
)

# ------------------- ДИЗАЙН (ЗЕЛЕНЫЙ ТЕРМИНАЛ) -------------------
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

.skill-tag {
    display: inline-block;
    border: 1px solid #00ff00;
    padding: 5px 15px;
    margin: 5px;
    background: rgba(0, 255, 0, 0.1);
    border-radius: 5px;
}

/* Кнопка связи */
.stButton>button {
    width: 100%;
    border: 1px solid #00ff00 !important;
    background-color: #051a05 !important;
    color: #00ff00 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------- ПЕРСОНАЛЬНЫЙ БЛОК АББАСА -------------------
st.markdown(f"""
<div class='abbas-card'>
    <h1>DEVELOPER: ABBAS</h1>
    <h3 style="letter-spacing: 2px;">+996 559 021 309</h3>
</div>
""", unsafe_allow_html=True)

# ------------------- ОСНОВНОЙ КОНТЕНТ -------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📷 ОБРАБОТКА ДАННЫХ")
    uploaded = st.file_uploader("Загрузить фото для анализа", type=["jpg", "jpeg", "png"])
    
    if uploaded:
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, caption="Объект загружен", use_container_width=True)
        st.success("Аббас, файл успешно считан.")

with col2:
    st.subheader("🛠 ТЕХНОЛОГИЧЕСКИЙ СТЕК")
    st.markdown("""
    <div style="margin-top:20px;">
        <div class="skill-tag">PYTHON 3.11</div>
        <div class="skill-tag">STREAMLIT</div>
        <div class="skill-tag">OPENCV</div>
        <div class="skill-tag">NUMPY</div>
        <div class="skill-tag">GITHUB</div>
        <div class="skill-tag">LINUX DEPLOY</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("💬 СВЯЗАТЬСЯ СО МНОЙ")
    # Кнопка для быстрого перехода в WhatsApp
    wa_link = "https://wa.me/996559021309"
    st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; cursor:pointer; padding:10px; border:1px solid #00ff00; background:#051a05; color:#00ff00;">НАПИСАТЬ В WHATSAPP</button></a>', unsafe_allow_html=True)

st.markdown("---")

# ------------------- КАМЕРА -------------------
st.subheader("📹 ТЕСТ СИСТЕМЫ ЗАХВАТА")
cam = st.camera_input("ПРОВЕРКА ВЕБ-КАМЕРЫ")

if cam:
    img_cam = cv2.imdecode(np.frombuffer(cam.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    st.image(cv2.cvtColor(img_cam, cv2.COLOR_BGR2RGB), caption="Снимок захвачен")
    st.info("Аббас, оборудование работает в штатном режиме.")

st.markdown("<p style='text-align:center; opacity:0.3; margin-top:50px;'>PORTFOLIO SYSTEM v3.0 | 2026</p>", unsafe_allow_html=True)
