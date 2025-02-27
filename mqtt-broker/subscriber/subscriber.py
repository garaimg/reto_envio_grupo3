import ssl

import paho.mqtt.client as mqtt

def on_message(client, userdata, msg):
    print(f"📩 Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(client_id="news-subscriber")
client.tls_set(
    ca_certs="/mosquitto/certs/ca.crt",
    certfile="/mosquitto/certs/subscriber.crt",
    keyfile="/mosquitto/certs/subscriber.key",
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.tls_insecure_set(False)

client.on_message = on_message

broker = "mosquitto"
port = 8883
client.connect(broker, port)

# Ejemplo: suscribirse a dos topics
topics = [
    ("articulos/+/futbol", 2),
    ("articulos/eltiempo/politica", 2)
]
client.subscribe(topics)

client.loop_start()

print("🔗 Conectado al broker MQTT.")
print("📩 Suscrito a los siguientes topics:")
for t, _ in topics:
    print(f"  - {t}")

try:
    while True:
        pass
except KeyboardInterrupt:
    print("🛑 Cerrando subscriber...")

client.loop_stop()
client.disconnect()
