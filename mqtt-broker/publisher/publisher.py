import time
import random
import ssl
import paho.mqtt.client as mqtt

# Crear el cliente MQTT
client = mqtt.Client(client_id="news-publisher")

# Configurar TLS usando los certificados del publisher
client.tls_set(
    ca_certs="/mosquitto/certs/ca.crt",
    certfile="/mosquitto/certs/publisher.crt",
    keyfile="/mosquitto/certs/publisher.key",
    tls_version=ssl.PROTOCOL_TLSv1_2
)
client.tls_insecure_set(False)

broker = "mosquitto"  # En la red de Docker, el broker se llama "mosquitto"
port = 8883
client.connect(broker, port)
client.loop_start()

print("📢 Publicador de artículos activo. Enviando artículos cada 10 segundos...")

articles = [
    {
        "newspaper": "marca",
        "category": "futbol",
        "title": "El triunfo de Deusto FC",
        "content": "El Deusto FC gana en un partido épico."
    },
    {
        "newspaper": "marca",
        "category": "baloncesto",
        "title": "Baloncesto en alza",
        "content": "El equipo local sorprende a todos en la cancha."
    },
    {
        "newspaper": "eldiario",
        "category": "futbol",
        "title": "Derbi de alto voltaje",
        "content": "Dos grandes rivales se enfrentan en un derbi inolvidable."
    },
    {
        "newspaper": "eldiario",
        "category": "baloncesto",
        "title": "El Baloncesto baja en audiencias en 2025",
        "content": "El baloncesto en 2025 se ve un 5% menos que en 2024."
    },
    {
        "newspaper": "elpais",
        "category": "politica",
        "title": "Debate presidencial",
        "content": "El presidente anuncia nuevas medidas en el debate."
    },
    {
        "newspaper": "as",
        "category": "futbol",
        "title": "Lucha por la clasificación",
        "content": "Los equipos se esfuerzan por obtener un puesto en Champions League."
    },
]

try:
    while True:
        article = random.choice(articles)
        topic = f"articulos/{article['newspaper']}/{article['category']}"
        message = f"Título: {article['title']} | Contenido: {article['content']}"
        print(f"📰 Publicando en {topic}: {message}")
        client.publish(topic, payload=message, qos=2)
        time.sleep(10)
except KeyboardInterrupt:
    print("🛑 Cerrando publicador...")

client.loop_stop()
client.disconnect()
