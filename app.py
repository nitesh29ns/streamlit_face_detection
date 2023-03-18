import cv2
import streamlit as st
import torch
import numpy as np

st.title("Webcam Live Feed")
run = st.button('Run')
FRAME_WINDOW = st.image([])
model = torch.hub.load('./yolov5/', 'custom', path='my_face_detection_model.pt', source='local') 

camera = cv2.VideoCapture(0)
while run:
    _, frame = camera.read()
    result = model(frame)
    ret,buffer=cv2.imencode('.jpg',  np.squeeze(result.render()))
    image = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)


if st.button("stop camera"):
    camera.release()
