FROM python:3.9-slim
RUN pip install "paho-mqtt<2.0.0"
WORKDIR /app
COPY subscriber.py .
CMD ["python", "-u", "subscriber.py"]
