import pika
import os
import queue
import threading

# Fonction pour convertir une image en bits
def img_bits(image_path):
    with open(image_path, 'rb') as f:
        return f.read()

# Fonction pour traiter les images d'un lot et les envoyer à une file d'attente spécifique
def traiter_images_lot(dossier, debut, fin, file_attente):
    images_paths = [os.path.join(dossier, fichier) for fichier in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, fichier))]
    for image_path in images_paths[debut:fin]:
        # Convertir l'image en bytes
        images = img_bits(image_path)
        # Mettre l'image dans la file d'attente spécifique
        file_attente.put((image_path, images))

# Paramètres de connexion à RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', virtual_host='/', credentials=credentials))
channel = connection.channel()

# Connection à l'exchange appelé "image"
channel.exchange_declare('image', durable=True, exchange_type='topic')

# Déclaration des files d'attente
channel.queue_declare(queue='image_queue_1')
channel.queue_declare(queue='image_queue_2')
channel.queue_declare(queue='image_queue_3')
channel.queue_declare(queue='image_queue_4')

# Chemin du dossier contenant les images
dossier_images = 'cars'

# Obtenir la liste des fichiers dans le dossier
fichiers_dossier = [fichier for fichier in os.listdir(dossier_images) if os.path.isfile(os.path.join(dossier_images, fichier))]
nombre_fichier = len(fichiers_dossier)
print("\n\nCe dossier contient :", nombre_fichier, "images")

# Définir le nombre de files d'attente (nombre de lots)
nbr_files_attente = 4

# Calculer la taille de chaque lot
taille_lot = nombre_fichier // nbr_files_attente

# Créer et démarrer les threads pour traiter les images dans chaque file d'attente
threads = []
for i in range(nbr_files_attente):
    debut = i * taille_lot
    fin = debut + taille_lot if i < nbr_files_attente - 1 else nombre_fichier
    file_attente = queue.Queue()
    thread = threading.Thread(target=traiter_images_lot, args=(dossier_images, debut, fin, file_attente))
    thread.start()
    threads.append((thread, file_attente))

# Attendre la fin de tous les threads
for thread, file_attente in threads:
    thread.join()

# Envoyer les images de chaque file d'attente à RabbitMQ
for i, (thread, file_attente) in enumerate(threads):
    while not file_attente.empty():
        image_path, img_bit = file_attente.get()
        channel.basic_publish(exchange='', routing_key=f'image_queue_{i+1}', body=img_bit)
        print(f"Image {image_path} envoyée à la file d'attente image_queue_{i+1}")

# Fermer la connexion à RabbitMQ
connection.close()
