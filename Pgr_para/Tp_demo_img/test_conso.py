import pika
from PIL import Image
import io
import os

# Fonction pour convertir les images en noir et blanc
def convert_to_grayscale(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    grayscale_image = image.convert('L')  # Convertir en noir et blanc
    return grayscale_image

# Callback function pour traiter les messages reçus
def callback(ch, method, properties, body):
    # Convertir les bytes en image
    image = convert_to_grayscale(body)

    # Définir le chemin et le nom de fichier pour enregistrer l'image
    save_path = 'images_grayscale'
    os.makedirs(save_path, exist_ok=True)  # Créer le dossier s'il n'existe pas
    filename = os.path.join(save_path, f'image_{method.delivery_tag}.bmp')

    # Enregistrer l'image en noir et blanc
    image.save(filename)

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
