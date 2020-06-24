import pygame
import constantes as C
from composants.controlable import Contrôlable
from composants.orientable import Orientable
from composants.position import Position
from composants.dialogue import Dialogue
from composants.marchand import Marchand
from composants.inventaire import Inventaire
from composants.stats import Stats
from composants.lancecombat import LanceCombat
import random
import pickle
import copy


class GÉvènement:

    def __init__(self, état):
        self.continue_jeu = True
        self.état = état
        self.gétat = None
        self.Joystick = None
        self.recharge = 0
        self.__vérifie_joystick()

    def __vérifie_joystick(self):
        pygame.joystick.init()
        if pygame.joystick.get_count() >= 1:
            self.Joystick = pygame.joystick.Joystick(0)
            self.Joystick.init()
        else:
            pygame.joystick.quit()

    def __traite_interaction(self):
        orientable = self.état.joueur.obtient_composant(Orientable)
        tuile = self.gétat.calcule_tuile_cible(self.état.joueur, orientable.orientation)
        for entité in self.état.entités:
            position = entité.obtient_composant(Position)
            dialogue = entité.obtient_composant(Dialogue)
            combat = entité.obtient_composant(LanceCombat)
            if position.x == tuile.x and position.y == tuile.y and position.niveau == self.état.joueur.obtient_composant(Position).niveau:
                if dialogue:
                    dialogue.sur_interaction(entité, self.état.joueur)
                    marchand = entité.obtient_composant(Marchand)
                    if dialogue.conteur >= len(dialogue.dialogue) + 1:
                        if marchand:
                            marchand.sur_échange(self.état.joueur)
                            if dialogue.conteur >= len(dialogue.dialogue) + len(marchand.items_manquants) + 1:
                                if None in marchand.items_manquants:
                                    marchand.items_manquants.remove(None)
                                dialogue.actif = False
                                dialogue.conteur = 0
                                marchand.dialogue = None
                            else:
                                dialogue.conteur += 1
                        else:
                            dialogue.conteur = 0
                            dialogue.actif = False
                elif combat:
                    self.état.entité_lance_combat = entité
                    combat.sur_interaction(self.état)
                    for entité in combat.entités_combat.values():
                        entité.obtient_composant(Stats).réinit_HP()
                    self.gétat.mécanique_combat.ennemis = copy.copy(combat.entités_combat)
                    pygame.mixer.music.stop()
                    musique = ['Acruta Lao D\'nor.mp3', 'Wings.mp3']
                    musique_choisie = random.choice(musique)
                    if self.gétat.mécanique_combat.ennemis[0].id == 'Boss':
                        self.gétat.mécanique_combat.ennemis[1] = self.gétat.mécanique_combat.ennemis.pop(0)
                        musique_choisie = 'demens.mp3'
                    pygame.mixer.music.load('ressources\\Musique\\' + musique_choisie)
                    pygame.mixer.music.play(-1)

        tuile.sur_interaction(self.état, self.état.joueur)

    def __traite_échec(self, événement):
        if événement.type == pygame.KEYDOWN and événement.key == pygame.K_RETURN:
            self.état.état = C.ÉTAT_NIVEAU
            stats = self.état.joueur.obtient_composant(Stats)
            stats.réinit_HP()
            position = self.état.joueur.obtient_composant(Position)
            if position.niveau.id == (3, 0):
                position.x -= 1
            self.état.joueur.obtient_composant(Contrôlable).force = 0
            pygame.mixer.music.stop()
            musique = ['Enter the Woods.mp3', 'Nebula.mp3']
            musique_choisie = random.choice(musique)
            pygame.mixer.music.load('ressources\\Musique\\' + musique_choisie)
            pygame.mixer.music.play(-1)
            self.état.déplace_entité(self.état.joueur, position.niveau, position.x, position.y)

    def __traite_niveau(self, événement):
        if événement.type == pygame.KEYDOWN:
            clé = événement.key
            if clé == pygame.K_ESCAPE:
                self.continue_jeu = False
            elif clé == pygame.K_m:
                self.état.mode_débogage = not self.état.mode_débogage
                print(self.état.joueur.obtient_composant(Stats).attaque)
            else:
                contrôlable = self.état.joueur.obtient_composant(Contrôlable)
                if contrôlable:
                    if (clé == pygame.K_w or clé == pygame.K_UP):
                        contrôlable.force = C.DIRECTION_N
                    elif (clé == pygame.K_d or clé == pygame.K_RIGHT):
                        contrôlable.force = C.DIRECTION_E
                    elif (clé == pygame.K_s or clé == pygame.K_DOWN):
                        contrôlable.force = C.DIRECTION_S
                    elif (clé == pygame.K_a or clé == pygame.K_LEFT):
                        contrôlable.force = C.DIRECTION_O
                    elif clé == pygame.K_SPACE and self.état.état != C.ÉTAT_PAUSE:
                        self.__traite_interaction()
                    elif clé == pygame.K_p:
                        if self.état.état == C.ÉTAT_NIVEAU:
                            self.état.état = C.ÉTAT_PAUSE
                        else:
                            self.état.état = C.ÉTAT_NIVEAU

        elif événement.type == pygame.KEYUP:
            clé = événement.key
            contrôlable = self.état.joueur.obtient_composant(Contrôlable)
            if contrôlable:
                force = contrôlable.force
                if clé == pygame.K_w and force == C.DIRECTION_N \
                        or clé == pygame.K_UP and force == C.DIRECTION_N \
                        or clé == pygame.K_d and force == C.DIRECTION_E \
                        or clé == pygame.K_RIGHT and force == C.DIRECTION_E \
                        or clé == pygame.K_s and force == C.DIRECTION_S \
                        or clé == pygame.K_DOWN and force == C.DIRECTION_S \
                        or clé == pygame.K_a and force == C.DIRECTION_O \
                        or clé == pygame.K_LEFT and force == C.DIRECTION_O:
                    contrôlable.force = 0

        if pygame.joystick.get_count() >= 1:
            contrôlable = self.état.joueur.obtient_composant(Contrôlable)
            if événement.type == pygame.JOYBUTTONDOWN:
                if self.Joystick.get_button(9) == 1:
                    self.état.mode_débogage = not self.état.mode_débogage
            if contrôlable:
                if événement.type == pygame.JOYAXISMOTION:
                    if self.Joystick.get_axis(1) < -0.5:
                        contrôlable.force = C.DIRECTION_N
                    elif self.Joystick.get_axis(1) > 0.5:
                        contrôlable.force = C.DIRECTION_S
                    elif self.Joystick.get_axis(0) > 0.5:
                        contrôlable.force = C.DIRECTION_E
                    elif self.Joystick.get_axis(0) < -0.5:
                        contrôlable.force = C.DIRECTION_O
                    else:
                        contrôlable.force = 0

    def __vérifie_boutton(self, rect):
        x, y, l, h = rect
        souris = pygame.mouse.get_pos()
        if x <= souris[0] + 32 <= x + l and y <= souris[1] + 32 <= y + h:
            return True
        else:
            return False

    def __traite_combat(self):
        clic = pygame.mouse.get_pressed()
        for boutton in self.état.bouttons.values():
            if boutton.texte:
                if not (boutton.texte == 'Fuir' and 'Boss' in self.état.entité_lance_combat.id):
                    if self.__vérifie_boutton(boutton.obtiens_rect()):
                        boutton.souris_dessus = True
                        if clic[0] and self.recharge <= 0:
                            if self.gétat.mécanique_combat.tour:
                                boutton.cliqué = True
                                self.recharge = C.RECHARGE_CLIC
                    else:
                        boutton.souris_dessus = False
        boutton = self.état.bouttons['Attaque']
        if boutton.cliqué:
            for x in range(len(self.état.bouttons_cible)):
                boutton = self.état.bouttons_cible[x]
                if x in self.gétat.mécanique_combat.ennemis.keys():
                    if self.__vérifie_boutton(boutton.obtiens_rect()):
                        boutton.souris_dessus = True
                        if clic[0] and self.recharge <= 0:
                            if self.gétat.mécanique_combat.tour:
                                boutton.cliqué = True
                                self.recharge = C.RECHARGE_CLIC
                    else:
                        boutton.souris_dessus = False
        self.recharge -= 1

    def __traite_victoire(self, événement):
        if événement.type == pygame.KEYDOWN and événement.key == pygame.K_RETURN:
            self.gétat.mécanique_combat.partir = True
            pygame.mixer.music.stop()
            musique = ['Enter the Woods.mp3', 'Nebula.mp3']
            musique_choisie = random.choice(musique)
            pygame.mixer.music.load('ressources\\Musique\\' + musique_choisie)
            pygame.mixer.music.play(-1)

    def __traite_menu(self):
        clic = pygame.mouse.get_pressed()
        boutton = self.état.bouttons['Jouer']
        if self.__vérifie_boutton(boutton.obtiens_rect()):
            boutton.souris_dessus = True
            if clic[0]:
                self.état.état = C.ÉTAT_NIVEAU
                pygame.mixer.music.stop()
                musique = ['Enter the Woods.mp3', 'Nebula.mp3']
                musique_choisie = random.choice(musique)
                pygame.mixer.music.load('ressources\\Musique\\' + musique_choisie)
                pygame.mixer.music.play(-1)
        else:
            boutton.souris_dessus = False

    def traite(self):
        if self.état.état == C.ÉTAT_COMBAT:
            self.__traite_combat()
        elif self.état.état == C.ÉTAT_MENU:
            self.__traite_menu()
        for événement in pygame.event.get():
            if événement.type == pygame.QUIT or événement.type == pygame.KEYDOWN and événement.key == pygame.K_ESCAPE:
                if self.état.état != C.ÉTAT_COMBAT:
                    position = self.état.joueur.obtient_composant(Position)
                    pickle_out = open("ressources\\save.chonker", 'wb')
                    pickle.dump((self.état.joueur.obtient_composant(Inventaire).inventaire, (position.x, position.y), position.niveau.id, self.état.niveaux, self.état.entités_détruites, self.état.joueur.obtient_composant(Stats)), pickle_out)
                    pickle_out.close()
                    self.continue_jeu = False
                    break
            elif self.état.état == C.ÉTAT_NIVEAU or self.état.état == C.ÉTAT_PAUSE:
                self.__traite_niveau(événement)
            elif self.état.état == C.ÉTAT_ÉCHEC:
                self.__traite_échec(événement)
            elif self.état.état == C.ÉTAT_VICTOIRE:
                self.__traite_victoire(événement)

        return self.continue_jeu
