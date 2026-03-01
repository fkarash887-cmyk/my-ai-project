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

html, body, [class*="css"] {
    background-color: black !important;
    color: #00ff00 !important;
    font-family: 'Share Tech Mono', monospace !important;
}

h1 {
    text-align: center;
    text-shadow: 0 0 10px #00ff00;
}

.stButton>button, .stCheckbox>label {
    background-color: black !important;
    color: #00ff00 !important;
    border: 1px solid #00ff00 !important;
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
model = YOLO("yolov8n.pt")

# ------------------- IMAGE MODE -------------------
uploaded = st.file_uploader("Загрузить изображение", type=["jpg", "png", "jpeg"])

if uploaded:
    img = cv2.imdecode(np.frombuffer(uploaded.read(), np.uint8), cv2.IMREAD_COLOR)

    results = model(img)[0]
    annotated = results.plot()

    people = sum(1 for b in results.boxes if int(b.cls) == 0)

    st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
    st.markdown(f"**Людей на изображении:** {people}")

st.markdown("---")

# ------------------- CAMERA MODE -------------------
run = st.checkbox("Включить камеру")

if run:
    cap = cv2.VideoCapture(0)
    frame_box = st.image([])
    counter = st.empty()

    while run:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        annotated = results.plot()

        people = sum(1 for b in results.boxes if int(b.cls) == 0)

        frame_box.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
        counter.markdown(f"**Людей в кадре:** {people}")

    cap.release()
