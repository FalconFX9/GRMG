from composants.stats import Stats
from composants.combat import Combat
from composants.lancecombat import LanceCombat
from composants.inventaire import Inventaire
from composants.controlable import Contrôlable
import constantes as C
from random import randint, random, choice
import pygame


class MécaniqueCombat:
    def __init__(self, état):
        self.état = état
        self.ennemis = {}
        self.tour = True
        self.attaque_manquée = False
        self.entité_visée = None
        self.ennemis_vaincus = False
        self.recharge = C.RECHARGE_ANIM
        self.conteur = 0
        self.nmbr_ennemis = 0
        self.partir = False

    def effectue_tour(self):
        self.attaque_manquée = False
        self.entité_visée = None
        self.tour = not self.tour

    def attaque(self, entité_attaquante, entité_visée):
        stats_attaque = entité_attaquante.obtient_composant(Stats)
        stats_visée = entité_visée.obtient_composant(Stats)

        if randint(0, 100) >= stats_visée.agilité:
            multiplicateur = randint(-30, 30) / 100
            dégats = (stats_attaque.attaque * ((100 - stats_visée.armure) / 100)) * (1 + multiplicateur)
            if randint(0, 100) <= 10:
                dégats *= 2
        else:
            self.attaque_manquée = True
            dégats = 0

        stats_visée.HP -= dégats

        if stats_visée.HP <= 0:
            if entité_visée.contient_composant(Combat):
                for id, entité in self.ennemis.items():
                    if entité == entité_visée:
                        id_mort = id
                self.ennemis.pop(id_mort)

    def calcule_XP(self):
        XP_ajouté = 0
        for entité in self.état.entité_lance_combat.obtient_composant(LanceCombat).entités_combat.values():
            niveau = entité.obtient_composant(Stats).niveau
            XP_ajouté += C.XP_PAR_ENNEMI[entité.id] * (1 + (niveau / 5))
        return XP_ajouté

    def vérif_combat(self):
        if len(self.ennemis) == 0:
            self.ennemis_vaincus = True
            if not self.tour:
                pygame.mixer.music.stop()
                pygame.mixer.music.load('ressources\\Musique\\victory.mp3')
                pygame.mixer.music.play(-1)
            self.tour = True
            self.état.état = C.ÉTAT_VICTOIRE
            if self.partir:
                stats_joueur = self.état.joueur.obtient_composant(Stats)
                self.état.état = C.ÉTAT_NIVEAU
                stats_joueur.XP += self.calcule_XP()
                if stats_joueur.vérifie_niveau():
                    self.état.joueur.obtient_composant(Inventaire).vérifie_stats()
                self.état.entités_détruites.append(self.état.entité_lance_combat.id)
                if 'Boss' in self.état.entité_lance_combat.id:
                    self.état.état = C.FIN_DU_JEU
                self.état.entités.remove(self.état.entité_lance_combat)
                self.état.joueur.obtient_composant(Contrôlable).force = None
                self.partir = False
        elif self.état.bouttons['Fuir'].cliqué:
            pygame.mixer.music.stop()
            musique = ['Enter the Woods.mp3', 'Nebula.mp3']
            musique_choisie = choice(musique)
            pygame.mixer.music.load('ressources\\Musique\\' + musique_choisie)
            pygame.mixer.music.play(-1)
            self.état.bouttons['Fuir'].cliqué = False
            self.état.état = C.ÉTAT_NIVEAU
            self.tour = True
            self.entité_visée = None
            self.ennemis.clear()
        elif self.état.joueur.obtient_composant(Stats).HP <= 0:
            self.état.état = C.ÉTAT_ÉCHEC
            pygame.mixer.music.stop()
            pygame.mixer.music.load('ressources\\Musique\\Game Over.mp3')
            pygame.mixer.music.play(-1)
            self.ennemis.clear()
            self.entité_visée = None
            self.tour = True

    def tour_ennemi(self, id):
        if self.recharge == C.RECHARGE_ANIM:
            self.attaque(self.ennemis[id], self.état.joueur)
            self.recharge -= 1
        elif self.recharge <= 0:
            self.attaque_manquée = False
            self.recharge = C.RECHARGE_ANIM
            self.conteur += 1
        else:
            self.recharge -= 1

    def tour_joueur(self):
        if self.entité_visée:
            if self.recharge == C.RECHARGE_ANIM:
                self.attaque(self.état.joueur, self.entité_visée)
                self.recharge -= 1
            elif self.recharge <= 0:
                self.effectue_tour()
                self.recharge = C.RECHARGE_ANIM
            else:
                self.recharge -= 1
        elif self.état.bouttons['Guérir'].cliqué:
            if self.recharge == C.RECHARGE_ANIM:
                self.guérison()
                self.recharge -= 1
            elif self.recharge <= 0:
                self.état.bouttons['Guérir'].cliqué = False
                self.effectue_tour()
                self.recharge = C.RECHARGE_ANIM
            else:
                self.recharge -= 1

    def guérison(self):
        stats = self.état.joueur.obtient_composant(Stats)
        stats.HP += (stats.HP_MAX * 0.33) * (random() / 2 + 1)
        if stats.HP > stats.HP_MAX:
            stats.HP = stats.HP_MAX

    def gestionnaire_tours(self):
        if self.tour:
            self.vérifie_entitée_visée()
            self.tour_joueur()
        else:
            nmbr_ennemis = len(self.état.entité_lance_combat.obtient_composant(LanceCombat).entités_combat.values())
            if 'Boss' not in self.état.entité_lance_combat.id:
                if self.conteur in self.ennemis.keys():
                    self.tour_ennemi(self.conteur)
                else:
                    self.conteur += 1

                if self.conteur == nmbr_ennemis:
                    self.conteur = 0
                    self.effectue_tour()
            else:
                self.tour_ennemi(1)
                if self.conteur == nmbr_ennemis:
                    self.conteur = 0
                    self.effectue_tour()

    def vérifie_entitée_visée(self):
        conteur = 0
        for boutton in self.état.bouttons_cible:
            if boutton.cliqué and conteur in self.ennemis.keys():
                self.entité_visée = self.ennemis[conteur]
                boutton.cliqué = False
            conteur += 1
