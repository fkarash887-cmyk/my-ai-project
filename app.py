import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import streamlit.components.v1 as components

# ------------------- КОНФИГУРАЦИЯ СТРАНИЦЫ -------------------
st.set_page_config(
    page_title="AI Academy | People Counter",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------- ХАКЕРСКИЙ ДИЗАЙН (CSS) -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* Основной фон и текст */
[data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
    background-color: #000000 !important;
}

* {
    color: #00ff00 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Заголовки */
h1 {
    text-align: center;
    text-shadow: 0 0 15px #00ff00;
    border-bottom: 2px solid #00ff00;
    padding-bottom: 10px;
}

/* Карточки и рамки */
.stImage, iframe, [data-testid="stMetricValue"] {
    border: 2px solid #00ff00 !important;
    box-shadow: 0 0 10px #00ff00;
}

/* Кнопки и инпуты */
button, .stFileUploader {
    border: 1px solid #00ff00 !important;
    background-color: #051a05 !important;
}

/* Стиль для метрик */
[data-testid="stMetricValue"] {
    background-color: #051a05;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ------------------- ЗАГРУЗКА МОДЕЛИ -------------------
@st.cache_resource
def load_yolo():
    # Загружаем легкую модель YOLOv8
    return YOLO("yolov8n.pt")

model = load_yolo()

# ------------------- ЗАГОЛОВОК -------------------
st.markdown("<h1>SYSTEM: PEOPLE COUNTING PORTFOLIO</h1>", unsafe_allow_html=True)

# ------------------- ОСНОВНОЙ ИНТЕРФЕЙС -------------------
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📡 AI SCANNER (Изображение)")
    uploaded = st.file_uploader("Загрузить объект для анализа", type=["jpg", "png", "jpeg"])
    
    if uploaded:
        # Чтение файла
        file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)

        # Детекция
        results = model(img)[0]
        annotated_img = results.plot()
        
        # Подсчет людей (ID класса 0 в YOLO - это person)
        people_count = sum(1 for b in results.boxes if int(b.cls) == 0)

        # Вывод
        st.image(cv2.cvtColor(annotated_img, cv2.COLOR_BGR2RGB), use_container_width=True)
        st.metric("ОБНАРУЖЕНО ОБЪЕКТОВ (HUMAN)", people_count)

with col2:
    st.subheader("🌐 CONNECTED PROJECT (Другой сайт)")
    
    # Выбор сайта для отображения
    site_option = st.selectbox("Выберите проект для просмотра:", 
                                ["Документация AI", "Мой GitHub", "Другой проект"])
    
    if site_option == "Документация AI":
        url = "https://docs.ultralytics.com/"
    elif site_option == "Мой GitHub":
        url = "https://github.com" # Замени на свою ссылку
    else:
        url = "https://www.wikipedia.org"

    # Вставка стороннего сайта
    components.iframe(url, height=550, scrolling=True)

st.markdown("---")

# ------------------- КАМЕРА (ДЛЯ ОБЛАКА) -------------------
st.subheader("📹 LIVE STREAM SCANNER")
st.info("Используйте этот блок для захвата кадра с вашей камеры в реальном времени.")

cam_input = st.camera_input("АКТИВИРОВАТЬ СКАНЕР")

if cam_input:
    # Обработка снимка с камеры
    bytes_data = cam_input.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Анализ
    res = model(cv2_img)[0]
    final_frame = res.plot()
    count = sum(1 for b in res.boxes if int(b.cls) == 0)
    
    st.image(cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB))
    st.success(f"Сканирование завершено. Найдено целей: {count}")

st.markdown("<p style='text-align:center'>Terminal v2.6.0 | AI Academy Projects</p>", unsafe_allow_html=True)
