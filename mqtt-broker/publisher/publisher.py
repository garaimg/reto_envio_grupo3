import time
import random
import paho.mqtt.client as mqtt

# Crear un cliente MQTT
client = mqtt.Client(client_id="news-publisher")

# Conectar al broker
broker = "mosquitto"  # Nombre del servicio en docker-compose
port = 1883
client.connect(broker, port)
print("🔗 Conectado al broker como publisher.")

# Iniciar el bucle para mantener la conexión
client.loop_start()

print("📢 Publicador de artículos activo. Enviando artículos cada 10 segundos...")

# Lista de artículos para publicar
articles = [
    {
        "newspaper": "marca",
        "category": "futbol",
        "title": "El triunfo del Deportivo Alavés",
        "content": "El Deportivo Alavés gana en un partido épico."
    },
    {
        "newspaper": "marca",
        "category": "baloncesto",
        "title": "Baloncesto en alza",
        "content": "El equipo local sorprende a todos en la cancha."
    },
    {
        "newspaper": "as",
        "category": "baloncesto",
        "title": "Baloncesto en decadencia",
        "content": "La audiencia del baloncesto baja en un 10%."
    },
    {
        "newspaper": "elmundo",
        "category": "futbol",
        "title": "Derbi de alto voltaje",
        "content": "Dos grandes rivales se enfrentan en un derbi inolvidable."
    },
    {
        "newspaper": "as",
        "category": "politica",
        "title": "Debate presidencial",
        "content": "El presidente anuncia nuevas medidas en el debate."
    },
    {
        "newspaper": "elmundo",
        "category": "politica",
        "title": "Debate presidencial parte 2",
        "content": "El presidente anuncia nuevas medidas en el debate (parte 2)."
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
        client.publish(topic, payload=message, qos=2)  # QoS 2 para la publicación
        time.sleep(10)
except KeyboardInterrupt:
    print("🛑 Cerrando publicador...")

client.loop_stop()
client.disconnect()
