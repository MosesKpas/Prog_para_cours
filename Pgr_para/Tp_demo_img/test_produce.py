import pika
from PIL import Image
import io

# Fonction pour convertir une image en bytes
def image_to_bytes(image_path):
    with open(image_path, 'rb') as f:
        return f.read()

# Paramètres de connexion à RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', virtual_host='/', credentials=credentials))
channel = connection.channel()

# Connection a l'exchange appelé test, qui est durable et qui a le type topic
channel.exchange_declare('image', durable=True, exchange_type='topic')

# Déclaration de la file d'attente
channel.queue_declare(queue='image_queue')
channel.queue_bind(exchange='image', queue='image_queue', routing_key='A')

# Chemins des images à envoyer
image_paths = ['cars/carsgraz_001.bmp', 'cars/carsgraz_002.bmp', 'cars/carsgraz_003.bmp']

# Envoyer chaque image à la file d'attente
for image_path in image_paths:
    # Convertir l'image en bytes
    image_bytes = image_to_bytes(image_path)
    # Envoyer l'image à la file d'attente
    channel.basic_publish(exchange='', routing_key='image_queue', body=image_bytes)
    print(f"Image {image_path} envoyée à la file d'attente")

# Fermer la connexion
connection.close()
