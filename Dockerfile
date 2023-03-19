FROM python:3.8.0

WORKDIR  /aap

COPY . ./
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt 
EXPOSE 8501


ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]