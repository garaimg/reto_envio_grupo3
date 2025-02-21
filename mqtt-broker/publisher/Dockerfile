FROM python:3.9-slim
RUN pip install paho-mqtt
WORKDIR /app
COPY publisher.py .
CMD ["python", "-u", "publisher.py"]
