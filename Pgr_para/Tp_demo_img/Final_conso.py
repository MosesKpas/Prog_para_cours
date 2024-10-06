import pika
from PIL import Image
import io
import os

# Fonction pour convertir les images en noir et blanc
def traiter_img_NB(img_bits):
    image = Image.open(io.BytesIO(img_bits))
    grayscale_image = image.convert('L')
    return grayscale_image

# Callback function pour traiter les messages reçus
def callback(ch, method, properties, body):
    # Convertir les bytes en image
    image = traiter_img_NB(body)

    # Définir le chemin et le nom de fichier pour enregistrer l'image
    dossier_img = 'cars_modif'
    os.makedirs(dossier_img, exist_ok=True)
    filename = os.path.join(dossier_img, f'image_{method.delivery_tag}.bmp')

    # Enregistrer l'image en noir et blanc
    image.save(filename)
    # Afficher le message de consommation
    print(f"Image traitée et enregistrée: {filename}")

    # Accusé de réception de la réception du message
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Paramètres de connexion à RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', virtual_host='/', credentials=credentials))
channel = connection.channel()

# Déclaration de l'exchange 'image'
channel.exchange_declare(exchange='image', durable=True, exchange_type='topic')

# Déclaration des files d'attente spécifiques
for i in range(1, 5):
    channel.queue_declare(queue=f'image_queue_{i}')

    # Lier chaque file d'attente à l'exchange avec la clé de routage spécifique
    channel.queue_bind(exchange='image', queue=f'image_queue_{i}', routing_key=f'image_queue_{i}')

# Configuration de la qualité de service, garantir que RabbitMQ ne distribue qu'un message à la fois
channel.basic_qos(prefetch_count=1)

# Lier chaque file d'attente au consommateur avec la fonction de callback
for i in range(1, 5):
    channel.basic_consume(queue=f'image_queue_{i}', on_message_callback=callback)

print("Attente de messages. Pour arrêter le programme, appuyez sur CTRL+C")
#commencer la consommation
channel.start_consuming()
