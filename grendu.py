import pygame
import pygame.gfxdraw
import ctypes
import pygame.freetype
import constantes as C
from cachesetimages import CacheImages
from cacheimages import CacheImagesIndividuelles
from tuiles.tuiles import *
from composants.position import Position
from composants.sprite import Sprite
from composants.boitealignee import BoîteAlignée
from composants.inventaire import Inventaire
from composants.mouvementgrille import MouvementGrille
from composants.dialogue import Dialogue
from composants.marchand import Marchand
from composants.stats import Stats
from composants.lancecombat import LanceCombat
from composants.combat import Combat
from usineentité import UsineEntité
from math import sin


class GRendu:

    def __init__(self, titre, état):
        self.titre = titre
        self.état = état
        self.fenêtre = None
        self.surface = None
        self.police = []
        self.prev_coords = {}
        self.cache_images = None
        self.mécanique_combat = None
        self.__initialise_système_graphique()
        self.__crée_fenêtre()
        self.__charge_images()
        self.__charge_police()

    def __initialise_système_graphique(self):
        pygame.init()

        # Paramètre les écrans à haut DPI.
        if C.HAUT_DPI:
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()

    def __crée_fenêtre(self):
        # Crée l'écran et obtiens la surface de dessin.
        self.fenêtre = pygame.display.set_mode((C.LARGEUR, C.HAUTEUR))
        x, y = self.fenêtre.get_size()
        self.surface = pygame.Surface(
            (x + C.TUILE_TAILLE, y + C.TUILE_TAILLE), pygame.SRCALPHA | pygame.HWSURFACE)
        self.inventaire = pygame.Surface((x, 100), pygame.SRCALPHA | pygame.HWSURFACE)

        # Détermine le titre de la fenêtre.
        pygame.display.set_caption(self.titre)

    def __charge_images(self):
        self.état.cache_images = CacheImagesIndividuelles()
        self.état.cache_images.charge('Mort', 'Fonds\\game_over_tr.png')
        self.état.cache_images.charge('Victoire', 'Fonds\\victoire.jpg')
        self.état.cache_images.charge('Fond_Menu', 'Fonds\\GenericRPG.png')
        self.état.cache_images.charge('Fond_Combat', 'Fonds\\fond_plage.jpg')
        self.état.cache_images.charge('Cible', 'Interface Graphique\\Crosshair.png')
        self.état.cache_images.charge('CibleTr', 'Interface Graphique\\CrosshairTransparency.png')
        self.état.cache_images.charge('Menu1', 'Interface Graphique\\AttackMenu.png')
        self.état.cache_images.charge('Dialogue', 'Interface Graphique\\DialogueEtendu.png')
        self.état.cache_images.charge('Joueur_Combat', 'Entités\\BigSoldier.png')
        self.état.cache_images.charge('Joueur_Attaqué', 'Entités\\BigSoldierDmg.png')
        self.état.cache_images.charge('Chauve_Souris', 'Entités\\pipo-enemy001.png')
        self.état.cache_images.charge('FantomeNoir', 'Entités\\pipo-enemy010b.png')
        self.état.cache_images.charge('SoldatSquel', 'Entités\\pipo-enemy026.png')
        self.état.cache_images.charge('OrbeBleue', 'Entités\\pipo-enemy012a.png')
        self.état.cache_images.charge('SoldatSombre', 'Entités\\pipo-enemy018b.png')
        self.état.cache_images.charge('Squelette', 'Entités\\pipo-enemy039.png')
        self.état.cache_images.charge('Diable', 'Entités\\pipo-enemy040.png')
        self.état.cache_images.charge('Loup', 'Entités\\pipo-enemy002a.png')
        self.état.cache_images.charge('Boss', 'Entités\\pipo-boss002.png')

        self.état.cache_images.transforme_taille('Fond_Menu', 640, 580)
        self.état.cache_images.transforme_taille('Cible', 48, 48)
        self.état.cache_images.transforme_taille('CibleTr', 48, 48)
        self.état.cache_images.transforme_taille('Joueur_Combat', 92, 128)
        self.état.cache_images.transforme_taille('Joueur_Attaqué', 92, 128)
        self.état.cache_images.transforme_taille('Chauve_Souris', 320, 320)
        self.état.cache_images.transforme_taille('FantomeNoir', 260, 260)
        self.état.cache_images.transforme_taille('SoldatSquel', 160, 160)
        self.état.cache_images.transforme_taille('OrbeBleue', 280, 280)
        self.état.cache_images.transforme_taille('SoldatSombre', 160, 160)
        self.état.cache_images.transforme_taille('Squelette', 160, 160)
        self.état.cache_images.transforme_taille('Diable', 200, 200)
        self.état.cache_images.transforme_taille('Loup', 180, 180)
        self.état.cache_images.transforme_taille('Boss', 426, 200)

        cache_images = CacheImages()
        cache_images.charge_entités('Joueur', 'Entités\\Soldier 01-1.png', 32, 32)
        cache_images.charge_entités('Mr Chad', 'Entités\\Male 01-1.png', 32, 32)
        cache_images.charge_entités('NPC Intro', 'Entités\\Male 04-1.png', 32, 32)
        cache_images.charge_entités('FantomeNoir', 'Entités\\Enemy 15-1.png', 32, 32)
        cache_images.charge_entités('SoldatSquel', 'Entités\\Enemy 04-1.png', 32, 32)
        cache_images.charge_entités('OrbeBleue', 'Entités\\Enemy 16-5.png', 32, 32)
        cache_images.charge_entités('SoldatSombre', 'Entités\\Enemy 05-1.png', 32, 32)
        cache_images.charge_entités('Squelette', 'Entités\\Enemy 06-1.png', 32, 32)
        cache_images.charge_entités('Loup', 'Entités\\Dog 01-3.png', 32, 32)
        cache_images.charge_entités('Boss', 'Entités\\Boss 01.png', 288, 288)
        self.état.usine_entité = UsineEntité(self.état, cache_images, self.état.cache_images)

        self.cache_images = CacheImages()
        self.cache_images.charge_tuiles('tileset.png', C.TUILE_TAILLE, C.TUILE_TAILLE)
        self.cache_images.charge_items('roguelikeitems.png', 16, 16)
        self.cache_images.charge_animation('Guérir', 'heal_003.png', 192, 192)

    def __charge_police(self):
        self.police.append(pygame.freetype.Font(C.RESSOURCES + "Polices\\After_Shok.ttf", 26))
        self.police.append(pygame.freetype.SysFont('comicsansms', 18))
        self.police.append(pygame.freetype.SysFont('comicsansms', 12))

    def __dessine_échec(self):
        self.surface.fill((0, 0, 0))
        img = self.état.cache_images.obtiens('Mort')
        largeur, hauteur = img.get_size()
        pos = ((C.LARGEUR - largeur) // 2) + 32, ((C.HAUTEUR - hauteur) // 2) + 32
        self.surface.blit(img, pos)
        taille = self.police[0].get_rect("Es tu perdu?")
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 32)
        self.police[0].render_to(self.surface, pos, None, (255, 0, 0))

    def __dessine_victoire(self):
        self.surface.fill((0, 0, 0))
        img = self.état.cache_images.obtiens('Victoire')
        largeur, hauteur = img.get_size()
        pos = ((C.LARGEUR - largeur) // 2) + 32, ((C.HAUTEUR - hauteur) // 2) + 32
        self.surface.blit(img, pos)
        taille = self.police[1].get_rect('+' + str(self.mécanique_combat.calcule_XP()) + 'XP !')
        pos = ((C.LARGEUR - taille[2]) // 2) + 32, 340
        self.police[1].render_to(self.surface, pos, None, (0, 255, 0))
        taille = self.police[1].get_rect('Apppuyez sur ENTER pour continuer')
        pos = ((C.LARGEUR - taille[2]) // 2) + 32, 420
        self.police[1].render_to(self.surface, pos, None, (255, 255, 255))

    def __dessine_menu(self):
        self.surface.fill((255, 0, 0))
        img = self.état.cache_images.obtiens('Fond_Menu')
        self.surface.blit(img, (32, 32))
        boutton = self.état.bouttons['Jouer']
        s = pygame.Surface((boutton.l, boutton.h), pygame.SRCALPHA)
        if boutton.souris_dessus:
            s.fill(boutton.c2)
        else:
            s.fill(boutton.c1)
        self.surface.blit(s, (boutton.x, boutton.y))
        rect = self.police[1].get_rect(boutton.texte)
        pos = ((boutton.x + (boutton.l - rect[0]) // 2) - 32, (boutton.y + boutton.h // 2) - rect[1] // 2)
        self.police[1].render_to(self.surface, pos, None, (255, 255, 255))

    def __dessine_dialogue(self):
        for entité in self.état.entités:
            dialogue = entité.obtient_composant(Dialogue)
            marchand = entité.obtient_composant(Marchand)
            if dialogue:
                if dialogue.actif:
                    img = self.état.cache_images.obtiens('Dialogue')
                    pos = (32, 434)
                    self.surface.blit(img, pos)
                    if marchand:
                        self.police[1].get_rect(marchand.dialogue)
                    try:
                        self.police[1].get_rect(dialogue.dialogue[dialogue.conteur - 1])
                    except IndexError:
                        pass
                    pos = (40, 444)
                    self.police[1].render_to(self.surface, pos, None, (255, 255, 255))

    def __colorie_image(self, image, couleur):
        couleur_remplacement = (255, 255, 255)
        coloriée = image.copy()
        pygame.transform.threshold(coloriée, coloriée, couleur_remplacement, set_color=couleur, inverse_set=True)
        # pygame.transform.threshold(coloriée, coloriée, (251, 252, 252), set_color=couleur, inverse_set=True)
        return coloriée

    def __dessine_entités(self, interpolation):
        niveau = self.état.joueur.obtient_composant(Position).niveau

        for entité in self.état.entités:
            position = entité.obtient_composant(Position)
            sprite = entité.obtient_composant(Sprite)
            mouvement = entité.obtient_composant(MouvementGrille)

            # Seulement dessiner les entités avec un position et un sprite.
            if not position or not sprite or position.niveau != niveau:
                continue

            # Obtiens l'image appropriée.
            for image, condition in sprite.images.items():
                if condition(entité):
                    if mouvement.recharge:
                        if 36 >= mouvement.recharge >= 24:
                            id = 2
                        elif 24 > mouvement.recharge >= 16:
                            id = 1
                        elif 16 > mouvement.recharge >= 8:
                            id = 0
                        elif 8 > mouvement.recharge >= 0:
                            id = 1
                    else:
                        id = 1
                    if type(image) is tuple:
                        img = image[id]
                    else:
                        img = image
                    break

            # Saute l'entité si aucune condition a été remplie.
            else:
                continue

            # Détermine la position en pixels.
            if self.état.état != C.ÉTAT_PAUSE:
                x, y = self.état.calcule_position(entité, interpolation)
            else:
                x, y = self.prev_coords[entité]
            boîte = entité.obtient_composant(BoîteAlignée)
            if boîte:
                pos = (
                    int((x + boîte.minx + 0.5) * C.TUILE_TAILLE),
                    int((y + boîte.miny + 0.5) * C.TUILE_TAILLE)
                )
            else:
                l, h = img.get_size()
                pos = (
                    int((x + 0.5) * C.TUILE_TAILLE - 0.5 * l),
                    int((y + 0.5) * C.TUILE_TAILLE - 0.5 * h)
                )

            # Dessine l'image.
            self.surface.blit(img, pos)

            # En mode débogage, dessine un rectangle autour de l'entité.
            if self.état.mode_débogage:
                bordure = pygame.Surface((C.TUILE_TAILLE, C.TUILE_TAILLE), pygame.SRCALPHA)
                pygame.draw.rect(bordure, C.JOUEUR_BORDURE, (0, 0, C.TUILE_TAILLE, C.TUILE_TAILLE), 3)
                self.surface.blit(bordure, pos)
            self.prev_coords[entité] = x, y

    def __dessine_carte(self):
        if self.état.mode_débogage:
            bordure = pygame.Surface(
                (C.TUILE_TAILLE, C.TUILE_TAILLE), pygame.SRCALPHA)
            pygame.draw.rect(bordure, C.TUILE_BORDURE,
                             (0, 0, C.TUILE_TAILLE, C.TUILE_TAILLE), 1)

        position = self.état.joueur.obtient_composant(Position)
        if not position:
            return

        for y in range(position.niveau.h - 1):
            for x in range(position.niveau.l):
                tuile = position.niveau.carte_l1[x][y]
                img = self.cache_images.obtiens_tuiles(int(tuile.variante))
                if tuile.couleur:
                    img = self.__colorie_image(img, tuile.couleur)
                pos = (tuile.x * C.TUILE_TAILLE, tuile.y * C.TUILE_TAILLE)
                self.surface.blit(img, pos)
                tuile = position.niveau.carte_l2[x][y]
                if tuile:
                    img = self.cache_images.obtiens_tuiles(int(tuile.variante))
                    if tuile.couleur:
                        img = self.__colorie_image(img, tuile.couleur)
                    pos = (tuile.x * C.TUILE_TAILLE, tuile.y * C.TUILE_TAILLE)
                    self.surface.blit(img, pos)
                if self.état.mode_débogage:
                    self.surface.blit(bordure, pos)

    def __dessine_débogage(self, interpolation):
        pos_interpolée = int(self.état.carré_débogage_pos + 1 * interpolation)
        pygame.draw.rect(self.surface, (0, 0, 0),
                         (pos_interpolée % (C.LARGEUR - 10), 10, 10, 10))

    def __dessine_inventaire(self):
        inventaire = self.état.joueur.obtient_composant(Inventaire)
        stats = self.état.joueur.obtient_composant(Stats)
        x = 0
        self.police[1].get_rect("Inventaire")
        self.police[1].render_to(self.surface, (32, 512), None, (255, 255, 255))
        self.police[1].get_rect("HP")
        self.police[1].render_to(self.surface, (560, 512), None, (255, 255, 255))
        self.police[1].get_rect(str(int(stats.HP)) + '/' + str(stats.HP_MAX))
        self.police[1].render_to(self.surface, (560, 532), None, (255, 255, 255))
        self.police[1].get_rect("XP")
        self.police[1].render_to(self.surface, (560, 562), None, (255, 255, 255))
        self.police[1].get_rect(str(int(stats.XP)) + '/' + str(stats.XP_MAX))
        self.police[1].render_to(self.surface, (560, 582), None, (255, 255, 255))
        for item in inventaire.inventaire.values():
            if type(item) is not int:
                self.surface.blit(self.cache_images.obtiens_items(item.id), ((x * 20) + 32, 552))
                x += 1
            else:
                self.police[1].get_rect('$' + str(item))
                pos = (35, 532)
                self.police[1].render_to(self.surface, pos, None, (255, 0, 0))

    def __dessine_combat(self):
        fond = self.état.cache_images.obtiens('Fond_Combat')
        self.surface.blit(fond, (0, 0))
        if self.mécanique_combat.attaque_manquée or self.mécanique_combat.tour:
            joueur_img = self.état.cache_images.obtiens('Joueur_Combat')
        else:
            joueur_img = self.état.cache_images.obtiens('Joueur_Combat')
            if self.mécanique_combat.recharge > 50:
                if sin(self.mécanique_combat.recharge / 4) > 0:
                    self.mécanique_combat.recharge -= 2
                    joueur_img = self.état.cache_images.obtiens('Joueur_Attaqué')

        if self.état.bouttons['Guérir'].cliqué:
            img_liste = self.cache_images.obtiens_animation('Guérir')
            img = img_liste[int(19 - (self.mécanique_combat.recharge // (150 / 19)))]
            self.surface.blit(img, (0, 55))
        self.surface.blit(joueur_img, (52, 100))
        menu_attaque = self.état.cache_images.obtiens('Menu1')
        self.surface.blit(menu_attaque, (32, 240))
        conteur = 0
        self.__dessine_HP()

        for boutton in self.état.bouttons.values():
            if boutton.texte and boutton.texte != 'Jouer':
                if not (boutton.texte == 'Fuir' and 'Boss' in self.état.entité_lance_combat.id):
                    s = pygame.Surface((boutton.l, boutton.h), pygame.SRCALPHA)
                    if boutton.souris_dessus:
                        s.fill(boutton.c2)
                    else:
                        s.fill(boutton.c1)
                    self.surface.blit(s, (boutton.x, boutton.y))
                    rect = self.police[1].get_rect(boutton.texte)
                    pos = ((boutton.x + (boutton.l - rect[0]) // 2) - 32, (boutton.y + boutton.h // 2) - rect[1] // 2)
                    self.police[1].render_to(self.surface, pos, None, (255, 255, 255))

        for id, entité in self.mécanique_combat.ennemis.items():
            combat = entité.obtient_composant(Combat)
            img = combat.img
            pos = (350 + 10 * id, -50 + 120 * id)
            if entité == self.mécanique_combat.entité_visée:
                if not self.mécanique_combat.attaque_manquée:
                    pos = (pos[0] + (sin(self.mécanique_combat.recharge / 4) * 4), pos[1])
                else:
                    pos = (pos[0], pos[1] + (self.mécanique_combat.recharge / 2 - 37.5))
                    self.mécanique_combat.recharge -= 1
            taille = img.get_size()
            taille_manquante = (320 - taille[0]) / 2, (320 - taille[1]) / 2
            pos = pos[0] + taille_manquante[0], pos[1] + taille_manquante[1]
            self.surface.blit(img, pos)
            largeur, hauteur = img.get_size()
            pos = ((pos[0] + largeur // 2) - 24, (pos[1] + hauteur // 2) - 24)
            boutton = self.état.bouttons_cible[id]
            if boutton.souris_dessus:
                img = self.état.cache_images.obtiens('Cible')
            else:
                img = self.état.cache_images.obtiens('CibleTr')
            self.surface.blit(img, pos)
            conteur += 1

    def __dessine_HP(self):
        stats_joueur = self.état.joueur.obtient_composant(Stats)
        self.__dessine_slider((32, 530), stats_joueur.HP, stats_joueur.HP_MAX, (0, 0, 255))
        self.police[2].get_rect(str(int(stats_joueur.HP)) + '/' + str(int(stats_joueur.HP_MAX)) + 'HP')
        self.police[2].render_to(self.surface, (185, 528), None, (255, 255, 255))
        for id, entité in self.mécanique_combat.ennemis.items():
            pos = (520, 530 + 15 * id)
            stats = entité.obtient_composant(Stats)
            self.__dessine_slider(pos, stats.HP, stats.HP_MAX, (255, 0, 0))
            taille = self.police[2].get_rect(str(int(stats.HP)) + '/' + str(int(stats.HP_MAX)) + 'HP')
            self.police[2].render_to(self.surface, (520 - taille[2], 528 + 15 * id), None, (255, 0, 0))

    def __dessine_slider(self, pos, v_actuelle, v_max, couleur):
        pygame.draw.rect(self.surface, (couleur), (pos[0], pos[1], 152, 8), 1)
        pygame.draw.rect(self.surface, (couleur), (pos[0] + 1, pos[1] + 1, (v_actuelle / v_max) * 150, 6))

    def __dessine_fin(self):
        self.surface.fill((0, 0, 0))
        taille = self.police[1].get_rect('Merci d\'avoir joué à la démo de GRMG!')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2))
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('Le jeu n\'est définitevement pas fini')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 22)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('et il y a encore beaucoup de bugs et d\'éléments manquants')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 42)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('Crédits:')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 64)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('Pipoya: Sprites du Joueur et des monstres')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 96)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('Charles Gabriel: Fond d\'interface de combat')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 128)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('Phyrnna: Musique')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 160)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('Et finalement, merci à Mr. Ouimet')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 192)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))
        taille = self.police[1].get_rect('et à Antoine pour avoir rendu ce projet possible')
        pos = (((C.LARGEUR - taille.w) // 2) + 32, ((C.HAUTEUR - taille.h) // 2) + 212)
        self.police[1].render_to(self.surface, pos, None, (255, 0, 0))

    def rend(self, interpolation):
        self.surface.fill(C.DESSIN_FOND)
        if self.état.état == C.ÉTAT_NIVEAU or self.état.état == C.ÉTAT_PAUSE:
            self.__dessine_carte()
            self.__dessine_inventaire()
            self.__dessine_entités(interpolation)
            self.__dessine_dialogue()
            if self.état.mode_débogage:
                self.__dessine_débogage(interpolation)
        elif self.état.état == C.ÉTAT_ÉCHEC:
            self.__dessine_échec()
        elif self.état.état == C.ÉTAT_COMBAT:
            self.__dessine_combat()
        elif self.état.état == C.ÉTAT_VICTOIRE:
            self.__dessine_victoire()
        elif self.état.état == C.ÉTAT_MENU:
            self.__dessine_menu()
        elif self.état.état == C.FIN_DU_JEU:
            self.__dessine_fin()
        self.__actualise_fenêtre()

    def __actualise_fenêtre(self):
        # Dessine l'image sur la fenêtre.
        self.fenêtre.blit(self.surface, (-C.TUILE_TAILLE, -C.TUILE_TAILLE))
        pygame.display.flip()
