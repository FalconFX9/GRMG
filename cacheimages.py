import pygame
import constantes as C


class CacheImagesIndividuelles:

    def __init__(self):
        self.images = {}

    def charge(self, id, nom_de_fichier):
        img = pygame.image.load(C.RESSOURCES + nom_de_fichier)
        img.set_colorkey(C.TUILE_TRANSPARENCE)
        img = img.convert_alpha()
        self.images[id] = img

    def transforme_taille(self, nom, x, y):
        self.images[nom] = pygame.transform.scale(self.images[nom], (x, y))

    def obtiens(self, id):
        return self.images[id]
