import pika
import os

# Fonction pour convertir une image en bytes
def image_to_bytes(image_path):
    with open(image_path, 'rb') as f:
        return f.read()

# Paramètres de connexion à RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', virtual_host='/', credentials=credentials))
channel = connection.channel()

# Connection à l'exchange appelé "image", qui est durable et de type "topic"
channel.exchange_declare('image', durable=True, exchange_type='topic')

# Déclaration de la file d'attente
channel.queue_declare(queue='image_queue')
channel.queue_bind(exchange='image', queue='image_queue', routing_key='A')

# Chemin du dossier contenant les images
dossier_images = 'cars'

# Lire tous les fichiers dans le dossier
fichiers_dossier = os.listdir(dossier_images)

# Filtrer les fichiers pour ne garder que les images
images_paths = [os.path.join(dossier_images, fichier) for fichier in fichiers_dossier if fichier.endswith(('.bmp', '.jpg', '.png'))]

# Envoyer chaque image à la file d'attente
for image_path in images_paths:
    # Convertir l'image en bytes
    image_bytes = image_to_bytes(image_path)
    # Envoyer l'image à la file d'attente
    channel.basic_publish(exchange='', routing_key='image_queue', body=image_bytes)
    print(f"Image {image_path} envoyée à la file d'attente")

# Fermer la connexion
connection.close()
