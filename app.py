import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO

# ------------------- PAGE -------------------
st.set_page_config(
    page_title="People Counting System",
    layout="wide"
)

# ------------------- STYLE -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: black !important;
    color: #00ff00 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Фикс для текста и заголовков */
h1, h2, h3, p, span, label {
    color: #00ff00 !important;
}

h1 {
    text-align: center;
    text-shadow: 0 0 10px #00ff00;
}

.stButton>button {
    background-color: black !important;
    color: #00ff00 !important;
    border: 1px solid #00ff00 !important;
    width: 100%;
}

.stImage {
    border: 2px solid #00ff00;
}

hr {
    border: 1px solid #00ff00;
}
</style>
""", unsafe_allow_html=True)

# ------------------- TITLE -------------------
st.markdown("<h1>PEOPLE COUNTING SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("---")

# ------------------- MODEL -------------------
# Кэшируем модель, чтобы она не загружалась при каждом обновлении страницы
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model = load_model()

# ------------------- MAIN INTERFACE -------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📷 Загрузка изображения")
    uploaded = st.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])
    
    if uploaded:
        # Конвертация файла в формат OpenCV
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        results = model(img)[0]
        annotated = results.plot()
        people = sum(1 for b in results.boxes if int(b.cls) == 0)

        st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), caption="Результат детекции")
        st.success(f"Найдено людей: {people}")

with col2:
    st.subheader("🌐 Внешний проект / Сайт")
    # Тот самый функционал "подключения другого сайта", о котором вы просили
    st.info("Здесь можно отобразить ваш другой репозиторий или документацию")
    st.components.v1.iframe("https://docs.ultralytics.com/", height=500, scrolling=True)

st.markdown("---")

# ------------------- CAMERA NOTE -------------------
st.subheader("📹 Работа с камерой")
st.warning("Внимание: cv2.VideoCapture(0) работает только при запуске локально на Windows!")

# В облаке используем st.camera_input для захвата кадра от пользователя
img_file_buffer = st.camera_input("Сделать снимок с веб-камеры")

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    results = model(cv2_img)[0]
    annotated = results.plot()
    people = sum(1 for b in results.boxes if int(b.cls) == 0)
    
    st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
    st.metric("Людей в кадре", people)
