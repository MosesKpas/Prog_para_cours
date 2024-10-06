import pika
from PIL import Image
import io

# Callback function pour traiter les messages reçus
def callback(ch, method, properties, body):
    # Convertir les bytes en image
    image = Image.open(io.BytesIO(body))

    # Traitement de l'image (exemple : affichage)
    image.show()

    # Accusé de réception de la réception du message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Paramètres de connexion à RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='image', durable=True, exchange_type='topic')

# Déclaration de la file d'attente
channel.queue_declare(queue='image_queue')

# Configuration de la qualité de service (QoS) pour garantir que RabbitMQ ne distribue qu'un message à la fois
channel.basic_qos(prefetch_count=1)

# Lier la file d'attente au consommateur avec la fonction de callback
channel.basic_consume(queue='image_queue', on_message_callback=callback)

print("Attente de messages. Pour arrêter le programme, appuyez sur CTRL+C")

# Commencer à consommer les messages de la file d'attente de façon infinie
channel.start_consuming()
