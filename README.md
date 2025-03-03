# Reto2 Grupo3 - Desarrollo de aplicaciones IoT

# Proyecto: MQTT con Python seguro

Este proyecto implementa un sistema de publicación de artículos basado en MQTT utilizando Eclipse Mosquitto como 
broker, con clientes de publicación y suscripción escritos en Python. La infraestructura está orquestada mediante 
Docker Compose y utiliza certificados TLS para la seguridad en la comunicación. Se han definido configuraciones 
específicas en un archivo mosquitto.conf y se incluye un script para generar certificados de seguridad.

---

## Miembros del Equipo

- **Miembro 1:** Markel Aguirre
- **Miembro 2:** Garai Martínez de Santos
- **Miembro 3:** Pablo Ruiz de Azúa

---

## Explicación de los Pasos Seguidos  

1. **Configuración de Contenedores con Docker Compose

    - Se han definido varios contenedores en `docker-compose.yml` para orquestar la infraestructura del sistema.
    - Se incluye un contenedor para el broker **Mosquitto**, un contenedor para el **publicador** y otro para el **suscriptor**.
    - También se ha configurado un script para la generación de certificados **TLS**, con el fin de garantizar una comunicación segura.  


2. **Configuración del Broker MQTT (Mosquitto)**  
    - Se ha configurado **Mosquitto** como el broker MQTT principal.  
    - En el archivo `mosquitto.conf` se han definido los parámetros necesarios para su funcionamiento, incluyendo la autenticación y el uso de **certificados TLS**.  
    - Se ha creado una carpeta `certs/` donde se almacenan los certificados.  
    - Se utiliza una base de datos `mosquitto.db` para la **persistencia de mensajes**.  
    - Se genera un archivo de logs `mosquitto.log` para el **monitoreo del sistema**.  


3. **Desarrollo del Publicador MQTT**  
    - Se ha desarrollado un script en Python (`publisher.py`) utilizando la librería **paho-mqtt** para publicar artículos en un tópico MQTT.  
    - Este script se ejecuta dentro de un contenedor definido mediante un `Dockerfile`, lo que permite su despliegue en un entorno aislado.  
    - Se ha configurado para publicar artículos de manera **periódica** a un tópico específico en el broker.  


4. **Desarrollo del Suscriptor MQTT:**  
    - Se ha desarrollado un script en Python (`subscriber.py`) que se suscribe a un tópico MQTT y recibe los artículos publicados por el publicador.  
    - Al igual que el publicador, el suscriptor se ejecuta dentro de un contenedor definido en su propio `Dockerfile`.  
    - El script puede **procesar los mensajes recibidos** y realizar operaciones adicionales según sea necesario.  


5. **Implementación de Seguridad con Certificados TLS:**  
    - Se ha creado un script `generate_certs.sh` para **generar los certificados** necesarios para la comunicación segura entre los clientes y el broker.  
    - Estos certificados se almacenan en la carpeta `certs/` y su uso ha sido habilitado en la configuración de **Mosquitto**.  
    - Esto garantiza que **solo las conexiones autenticadas y encriptadas** puedan comunicarse con el broker.

6. **Verificación de la comunicación segura con certificados mediante comandos CLI:**
    - Se ha utilizado el comando mosquitto_pub y mosquitto_sub para probar la comunicación segura con certificados vía comandos.
    - Se ha conectado al contenedor del broker utilizando el comando docker exec para ejecutar los comandos de forma local dentro del contenedor.
    - Se ha utilizado el puerto 8883 para la conexión segura con certificados.
    - Se han especificado los archivos de certificado y clave necesarios para la conexión segura.
    - Se ha comprobado que los clientes no pueden ni enviar ni recibir mensajes sin el uso de certificados.

---

## Instrucciones de Uso  

1. **Requisitos Previos:**  
    - Tener instalado [Docker](https://www.docker.com/get-started) y [Docker Compose](https://docs.docker.com/compose/install/).  
    - Clonar el repositorio del proyecto.  


2. **Generación de Certificados TLS:**  
    - Antes de levantar los contenedores, ejecutar el siguiente comando en la terminal con sudo:  
      ```bash
      sudo ./generate_certs.sh
      ```  
    - Esto creará los certificados en la carpeta `mosquitto/certs/`, que serán usados por Mosquitto, el publicador y el suscriptor.  


3. **Levantar los Contenedores:**  
    - Ejecutar el siguiente comando:  
      ```bash
      docker compose up --build
      ```  
    - Esto iniciará los contenedores del **broker Mosquitto, el publicador y el suscriptor**, y se verán los logs de cada servicio.  


4. **Verificación del Funcionamiento:**  
    - Comprobar que el **broker Mosquitto** está en ejecución y escuchando en el puerto **8883**.  
    - Revisar los logs de los contenedores para asegurarse de que el publicador está enviando mensajes y el suscriptor los está recibiendo correctamente.

5. **Uso vía comandos:**
    - **Subscriber:**
    - Entra al contenedor del broker:
         ```bash
      docker exec -it mosquitto sh
      ```  
    - Introduce el siguiente comando:
         ```bash
       mosquitto_sub -h mosquitto -p 8883 --cafile ./mosquitto/certs/ca.crt --cert ./mosquitto/certs/subscriber.crt --key ./mosquitto/certs/subscriber.key -t "articulos/+/futbol"
      ```  
    - Esperar a recibir algún artículo de fútbol.
    - **Publisher:**
    - Entra al contenedor del broker o mantente en el si ya estás:
       ```bash
      docker exec -it mosquitto sh
      ```  
    - Introduce el siguiente comando:
         ```bash
      mosquitto_pub -h mosquitto -p 8883 --cafile /mosquitto/certs/ca.crt --cert /mosquitto/certs/publisher.crt --key /mosquitto/certs/publisher.key -t "articulos/eldiario/futbol" -m 'Título: El Alavés en descenso | Contenido: El Alavés pelea por no descender.' 
      ```
    - Verificar que se ha enviado correctamente.
    - **Se puede verificar que **no funciona sin certificados** probando los siguientes comandos dentro del broker:**
        ```bash
       mosquitto_sub -h mosquitto -p 8883 -t "articulos/+/futbol"
      ```  
        ```bash
      mosquitto_pub -h mosquitto -p 8883 -t "articulos/eldiario/futbol" -m 'Título: El Alavés en descenso | Contenido: El Alavés pelea por no descender.' 
      ```  
---

## Posibles Vías de Mejora  

- **Manejo Mejorado de Certificados TLS:**  
  - Automatizar la generación de certificados en el proceso de inicio de los contenedores para evitar ejecuciones manuales.  
  - Implementar un mecanismo de **renovación automática** de certificados antes de su expiración.  


- **Gestión de Errores:**  
  - Mejorar la captura y notificación de errores en la conexión MQTT, permitiendo reintentos automáticos en caso de fallos.  
  - Implementar logs detallados en el publicador y suscriptor para registrar intentos fallidos de conexión y mensajes no entregados.  


- **Monitorización y Logging:**  
  - Integrar herramientas como **Prometheus y Grafana** para obtener métricas en tiempo real del tráfico MQTT.  
  - Configurar un sistema de logging centralizado con **ELK Stack (Elasticsearch, Logstash, Kibana)** para facilitar la depuración.  


- **Escalabilidad:**  
  - Permitir la conexión de múltiples publicadores y suscriptores, balanceando la carga para mejorar el rendimiento.  


- **Documentación Ampliada:**  
  - Incluir diagramas de arquitectura para explicar el flujo de datos en el sistema.  

---

## Problemas / Retos Encontrados  

- **Manejo de Certificados TLS:**  
  - Se encontraron dificultades en la generación y configuración de los certificados TLS. Hubo problemas al asegurar que los certificados fueran correctamente reconocidos y utilizados por Mosquitto, el publicador y el suscriptor, lo que requirió ajustes en la configuración y permisos de archivos.  


- **Problemas con el broker MQTT (`mosquitto.conf`)**
  - Se presentaron inconvenientes en la configuración del archivo `mosquitto.conf`, lo que afectó la conexión de los clientes al broker.
---

## Alternativas Posibles  

- **Uso de Otros Brokers MQTT:**  
  - Evaluar alternativas como **RabbitMQ con MQTT plugin** o **EMQX** en lugar de Mosquitto, especialmente si se requiere escalabilidad y características avanzadas como clustering o autenticación extendida.  


- **Implementación de Seguridad Adicional:**  
  - Considerar el uso de **OAuth 2.0** o **JWT** para la autenticación y autorización de clientes en lugar de solo certificados TLS.  


- **Persistencia Avanzada de Mensajes:**  
  - Integrar una base de datos como **PostgreSQL o InfluxDB** para almacenar los mensajes recibidos y analizarlos posteriormente.  


- **Monitoreo y Logging Mejorado:**  
  - Utilizar herramientas como **Prometheus y Grafana** para visualizar métricas en tiempo real del broker, publicador y suscriptor.  
  - Configurar un sistema de logging centralizado con **ELK Stack (Elasticsearch, Logstash, Kibana)** o **Loki** para analizar logs de los contenedores.  

---