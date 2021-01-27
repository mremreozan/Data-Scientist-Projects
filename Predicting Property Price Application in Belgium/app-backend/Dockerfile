FROM ubuntu:18.04
FROM python:3.8

RUN apt-get update -y 
RUN pip3 install -U scikit-learn

RUN mkdir /app 
COPY requirements.txt .
COPY app.py /app/app.py
COPY Datasets /app/Datasets
COPY model /app/model
COPY predict /app/predict
COPY preprocessing /app/preprocessing

RUN pip install -r requirements.txt

WORKDIR /app

CMD ["python", "app.py"]