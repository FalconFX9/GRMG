import pygame
import constantes as C


class CacheImages:
    def __init__(self):
        self.tuiles = []
        self.items = []
        self.images_entités = {}
        self.animations = {}

    def __charge(self, set_images, largeur, hauteur):
        image = pygame.image.load(C.RESSOURCES + set_images)
        image = image.convert_alpha()
        largeur_image, hauteur_image = image.get_size()
        images = []
        for image_y in range(0, int(hauteur_image / hauteur)):
            for image_x in range(0, int(largeur_image / largeur)):
                rect = (image_x * largeur, image_y * hauteur, largeur, hauteur)
                images.append(image.subsurface(rect))
        return images

    def __charge2d(self, set_images, largeur, hauteur):
        image = pygame.image.load(C.RESSOURCES + set_images)
        image = image.convert_alpha()
        largeur_image, hauteur_image = image.get_size()
        images = []
        for image_y in range(0, int(hauteur_image / hauteur)):
            index = []
            for image_x in range(0, int(largeur_image / largeur)):
                rect = (image_x * largeur, image_y * hauteur, largeur, hauteur)
                index.append(image.subsurface(rect))
            images.append(index)
        return images

    def charge_tuiles(self, tileset, largeur, hauteur):
        self.tuiles = self.__charge(tileset, largeur, hauteur)

    def charge_items(self, itemset, largeur, hauteur):
        self.items = self.__charge(itemset, largeur, hauteur)

    def charge_entités(self, nom, spritesheet, largeur, hauteur):
        self.images_entités[nom] = self.__charge2d(spritesheet, largeur, hauteur)

    def charge_animation(self, nom, setimages, largeur, hauteur):
        self.animations[nom] = self.__charge(setimages, largeur, hauteur)

    def obtiens_tuiles(self, id):
        return self.tuiles[id]

    def obtiens_sprite(self, nom, orientation):
        return self.images_entités[nom][orientation]

    def obtiens_items(self, id):
        return self.items[id]
    
    def obtiens_animation(self, nom):
        return self.animations[nom]
