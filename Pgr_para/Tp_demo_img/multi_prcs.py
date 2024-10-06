from PIL import Image
import os
import multiprocessing as mp
import time

def traiter_image(dos_img,debut,fin):
    t0 = time.time()
    for fichier in os.listdir(dos_img)[debut:fin+1]:
    # Vérifier si le fichier est une image
        if fichier.endswith(".jpg") or fichier.endswith(".jpeg") or fichier.endswith(".png")or fichier.endswith(".bmp"):
            # Chemin complet de image
            chemin_image = os.path.join(dos_img, fichier)

            # Ouvrir l'image
            photo = Image.open(chemin_image)

            # Convertir l'image en noir et blanc
            photo = photo.convert("L")

            # Enregistrer l'image modifiée dans un nouveau dossier
            dossier_modifie = "cars_modif_parallele"
            if not os.path.exists(dossier_modifie):
                os.makedirs(dossier_modifie)
            chemin_image_modifiee = os.path.join(dossier_modifie, fichier)
            photo.save(chemin_image_modifiee)
        else:
            print("Erreur, Pas d'image disponible dans ce dossier")
    t1 =time.time()
    print(f'Temps d\'execution : {t1 - t0} s')

def main():
    #Ouvrir le dossier et compter le contenu
    dossier  ="cars"
    fichier =[fichier for fichier in os.listdir(dossier) if os.path.isfile(os.path.join(dossier,fichier))]
    nombre_fichier = len(fichier)
    print("\n\nCe dossier contient :",nombre_fichier,"images")
    #Definir le nombre des processus
    nbr_processus = 4
    taille_lot = nombre_fichier // nbr_processus
    #Decouper le par lot d'images
    debuts = [(i *taille_lot) for i in range(nbr_processus)]
    fins = [debut + taille_lot -1 for debut in debuts]
    fins[-1] = nombre_fichier

    print("Debut du traitement\nEn attente......")
    print("Division par lot d'image :",debuts,fins)
    #print("Fin :",fins)
    processus = []
    for debut, fin in zip(debuts,fins):
        processus.append(mp.Process(
            target=traiter_image,
            args=(dossier,debut,fin)
        ))
        processus[-1].start()
    for processus in processus:
        processus.join()
    print("Fin du traitement")
        
if __name__ == "__main__":
    main()
