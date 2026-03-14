import streamlit as st
import cv2
import numpy as np
import streamlit.components.v1 as components

# ------------------- КОНФИГУРАЦИЯ СТРАНИЦЫ -------------------
st.set_page_config(
    page_title="Abbas | Developer Portfolio",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------- ПЕРСОНАЛЬНЫЙ ДИЗАЙН (CSS) -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Черный фон и зеленый текст */
[data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
    background-color: #000000 !important;
}

* {
    color: #00ff00 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Заголовок с неоновым свечением */
h1 {
    text-align: center;
    text-shadow: 0 0 15px #00ff00;
    border-bottom: 2px solid #00ff00;
    padding-bottom: 10px;
}

/* Карточка Аббаса */
.abbas-card {
    border: 2px double #00ff00;
    padding: 25px;
    margin-bottom: 30px;
    text-align: center;
    background: rgba(0, 255, 0, 0.05);
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.2);
}

/* Рамки для медиа-элементов */
.stImage, iframe, .stCameraInput {
    border: 1px solid #00ff00 !important;
}

/* Кнопки */
button {
    border: 1px solid #00ff00 !important;
    background-color: #051a05 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------- ШАПКА И КОНТАКТЫ -------------------
st.markdown("<h1>SYSTEM ACCESS: AUTHORIZED</h1>", unsafe_allow_html=True)

st.markdown(f"""
<div class="abbas-card">
    <h2 style="margin:0; letter-spacing: 5px;">РАЗРАБОТЧИК: АББАС</h2>
    <p style="font-size: 24px; margin:15px 0; font-weight: bold;">+996 559 021 309</p>
    <p style="font-size: 12px; opacity: 0.6;">PROJECT: SECURE PORTFOLIO | LOCATION: BISHKEK</p>
</div>
""", unsafe_allow_html=True)

# ------------------- ОСНОВНОЙ ИНТЕРФЕЙС -------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📷 Обработка Изображений")
    uploaded = st.file_uploader("Загрузить файл в систему", type=["jpg", "png", "jpeg"])
    
    if uploaded:
        # Чтение изображения
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        
        # Конвертация для отображения
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        st.image(img_rgb, caption="Файл успешно загружен в базу данных", use_container_width=True)
        st.success("Аббас, изображение считано успешно.")

with col2:
    st.subheader("🌐 Внешний Модуль")
    # Здесь можно поставить любую ссылку, например на твой GitHub
    st.info("Отображение внешнего ресурса под управлением пользователя")
    components.iframe("https://www.wikipedia.org", height=500, scrolling=True)

st.markdown("---")

# ------------------- КАМЕРА -------------------
st.subheader("📹 Видео-захват")
cam_data = st.camera_input("Активировать камеру для снимка")

if cam_data:
    # Обработка снимка
    bytes_data = cam_data.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Показываем результат (можно добавить OpenCV фильтры)
    st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB), caption="Снимок захвачен")
    st.info("Система подтверждает: Камера работает стабильно.")

st.markdown("<p style='text-align:center; opacity:0.5; margin-top:50px;'>Terminal v2.6.0 | Created by Abbas</p>", unsafe_allow_html=True)
