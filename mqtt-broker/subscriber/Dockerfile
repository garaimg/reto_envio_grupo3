FROM python:3.9-slim
RUN pip install paho-mqtt
WORKDIR /app
COPY subscriber.py .
CMD ["python", "-u", "subscriber.py"]
