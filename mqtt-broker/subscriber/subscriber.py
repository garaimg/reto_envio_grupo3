import paho.mqtt.client as mqtt

# Definir la función de callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(f"📩 Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

# Crear un cliente MQTT
client = mqtt.Client(client_id="news-subscriber")

# Asignar el callback para manejar mensajes entrantes
client.on_message = on_message

# Conectar al broker
broker = "mosquitto"  # Nombre del servicio en docker-compose
port = 1883
client.connect(broker, port)

# Suscribirse a los topics deseados
topics = [
    ("articulos/+/futbol", 2),  # QoS 2 para el primer topic
    ("articulos/elmundo/#", 2)  # QoS 2 para el segundo topic
]
client.subscribe(topics)

# Iniciar el bucle para procesar mensajes
client.loop_start()

print("🔗 Conectado al broker MQTT.")
print(f"📩 Suscrito a los topics: {[topic[0] for topic in topics]}")

# Mantener el script corriendo para recibir mensajes
try:
    while True:
        pass  # Espera indefinidamente
except KeyboardInterrupt:
    print("🛑 Cerrando subscriber...")

client.loop_stop()
client.disconnect()
