import pygame
from entité import Entité
from composants.controlable import Contrôlable
from composants.mouvementgrille import MouvementGrille
from composants.orientable import Orientable
from composants.position import Position
from composants.sprite import Sprite
from composants.joueur import Joueur
from composants.boitealignee import BoîteAlignée
from composants.zombie import Zombie
from composants.enseignant import Enseignant
from composants.inventaire import Inventaire
from composants.stats import Stats
from composants.combat import Combat
from composants.lancecombat import LanceCombat
from composants.collisionneur import Collisionneur
import constantes as C
import copy


class UsineEntité:

    def __init__(self, état, cache_images, cache_images_combat):
        self.cache_images = cache_images
        self.cache_images_combat = cache_images_combat
        self.état = état
        self.mécanique_combat = None

    def crée_joueur(self):
        return Entité().ajoute_composant(
            Stats(5),
            Inventaire(),
            Contrôlable(),
            MouvementGrille(
                C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(
                C.DIRECTION_O, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('Joueur', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('Joueur', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('Joueur', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('Joueur', 2)):
                lambda e: True}),
            Joueur()
        )

    def crée_npc_dialogue2(self):
        return Entité().ajoute_composant(
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_O, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('Mr Chad', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('Mr Chad', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('Mr Chad', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('Mr Chad', 2)):
                lambda e: True})
        )

    def crée_npc_dialogue(self):
        return Entité().ajoute_composant(
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_O, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('NPC Intro', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('NPC Intro', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('NPC Intro', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('NPC Intro', 2)):
                lambda e: True})
        )

    def crée_chauve_souris(self):
        return Entité('Chauve_Souris').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('Chauve_Souris')),
            Stats(15, (0.1, 0, 1, 1)),
        )

    def crée_fantome_noir(self):
        return Entité('FantomeNoir').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('FantomeNoir')),
            Stats(20, (0.05, 7, 3, 1)),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_O, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('FantomeNoir', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('FantomeNoir', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('FantomeNoir', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('FantomeNoir', 2)):
                lambda e: True})
        )

    def crée_soldat_squelette(self):
        return Entité('SoldatSquel').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('SoldatSquel')),
            Stats(5, (0.8, 4, 0.2, 1)),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_E, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('SoldatSquel', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('SoldatSquel', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('SoldatSquel', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('SoldatSquel', 2)):
                lambda e: True})
        )

    def crée_soldat_sombre(self):
        return Entité('SoldatSombre').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('SoldatSombre')),
            Stats(0, (0.4, 8, 5, 1)),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_E, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('SoldatSombre', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('SoldatSombre', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('SoldatSombre', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('SoldatSombre', 2)):
                lambda e: True})
        )

    def crée_orbe_bleue(self):
        return Entité('OrbeBleue').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('OrbeBleue')),
            Stats(50, (0.2, 0, 0.5, 1)),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_E, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('OrbeBleue', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('OrbeBleue', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('OrbeBleue', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('OrbeBleue', 2)):
                lambda e: True})
        )

    def crée_squelette(self):
        return Entité('Squelette').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('Squelette')),
            Stats(8, (0.5, 5, 0.8, 1)),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_E, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('Squelette', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('Squelette', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('Squelette', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('Squelette', 2)):
                lambda e: True})
        )

    def crée_loup(self):
        return Entité('Loup').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('Loup')),
            Stats(30, (0.2, 0, 3, 1)),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_E, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('Loup', 3)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('Loup', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('Loup', 0)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('Loup', 2)):
                lambda e: True})
        )

    def crée_diable(self):
        return Entité('Diable').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('Diable')),
            Stats(20, (0.2, 0, 2, 1)),
            Position(None, None, None),
            BoîteAlignée(-0.5, -0.5, 0.5, 0.5),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_E, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                pygame.transform.scale(self.cache_images_combat.obtiens('Diable'), (32, 32)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                pygame.transform.scale(self.cache_images_combat.obtiens('Diable'), (32, 32)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                pygame.transform.scale(self.cache_images_combat.obtiens('Diable'), (32, 32)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                pygame.transform.scale(self.cache_images_combat.obtiens('Diable'), (32, 32)):
                lambda e: True})
        )

    def crée_boss(self):
        def en_collision(état, e1, e2):
            if e2.contient_composant(Joueur):
                combat = e1.obtient_composant(LanceCombat)
                self.état.entité_lance_combat = e1
                combat.sur_interaction(self.état)
                self.mécanique_combat.ennemis[1] = copy.copy(e1.obtient_composant(LanceCombat).entités_combat[0])
                self.mécanique_combat.ennemis[1].obtient_composant(Stats).réinit_HP()
                pygame.mixer.music.stop()
                musique_choisie = 'demens.mp3'
                pygame.mixer.music.load('ressources\\Musique\\' + musique_choisie)
                pygame.mixer.music.play(-1)

        return Entité('Boss').ajoute_composant(
            Combat(self.cache_images_combat.obtiens('Boss')),
            Stats(10, (4, 8, 3, 1)),
            Position(None, None, None),
            BoîteAlignée(-4.5, -4.5, 4.5, 4.5),
            Collisionneur(en_collision),
            MouvementGrille(C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Orientable(C.DIRECTION_E, C.JOUEUR_RECHARGE_DÉPLACEMENT),
            Sprite({
                tuple(self.cache_images.obtiens_sprite('Boss', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_N,
                tuple(self.cache_images.obtiens_sprite('Boss', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_O,
                tuple(self.cache_images.obtiens_sprite('Boss', 1)):
                lambda e: e.obtient_composant(
                    Orientable).orientation == C.DIRECTION_S,
                tuple(self.cache_images.obtiens_sprite('Boss', 1)):
                lambda e: True})
        )

    def crée(self, nom):
        return getattr(self, 'crée_' + nom)()
