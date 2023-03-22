FROM python:3.8.0

WORKDIR  /aap

COPY . ./
COPY requirements.txt ./requirements.txt
COPY yolov5 ./yolov5
COPY my_face_detection_model.pt ./my_face_detection_model.pt

RUN pip install -r requirements.txt 
EXPOSE 8501


ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]