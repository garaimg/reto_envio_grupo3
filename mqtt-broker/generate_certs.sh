#!/bin/bash

# Directorio donde se guardarán los certificados
CERTS_DIR="mosquitto/certs"
mkdir -p $CERTS_DIR
cd $CERTS_DIR

echo "🔹 Generando Autoridad Certificadora (CA)..."
openssl genpkey -algorithm RSA -out ca.key
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/C=ES/ST=Álava/L=Vitoria-Gasteiz/O=Deusto/OU=IoT/CN=Deusto CA"

echo "🔹 Generando clave y CSR para el broker (Mosquitto)..."
openssl genpkey -algorithm RSA -out broker.key
openssl req -new -key broker.key -out broker.csr -subj "/C=ES/ST=Álava/L=Vitoria-Gasteiz/O=Deusto/OU=IoT/CN=mosquitto"

echo "🔹 Firmando el certificado del broker con la CA..."
openssl x509 -req -in broker.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out broker.crt -days 365

echo "🔹 Generando clave y CSR para el publicador..."
openssl genpkey -algorithm RSA -out publisher.key
openssl req -new -key publisher.key -out publisher.csr -subj "/C=ES/ST=Álava/L=Vitoria-Gasteiz/O=Deusto/OU=IoT/CN=publisher"

echo "🔹 Firmando el certificado del publicador con la CA..."
openssl x509 -req -in publisher.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out publisher.crt -days 365

echo "🔹 Generando clave y CSR para el suscriptor..."
openssl genpkey -algorithm RSA -out subscriber.key
openssl req -new -key subscriber.key -out subscriber.csr -subj "/C=ES/ST=Álava/L=Vitoria-Gasteiz/O=Deusto/OU=IoT/CN=subscriber"

echo "🔹 Firmando el certificado del suscriptor con la CA..."
openssl x509 -req -in subscriber.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out subscriber.crt -days 365

echo "✅ Certificados generados en la carpeta $CERTS_DIR"
