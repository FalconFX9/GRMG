import pygame
import constantes as C
from étatjeu import ÉtatJeu
from gétat import GÉtat
from gévènement import GÉvènement
from grendu import GRendu
from gfichiermonde import GFichierMonde
from gfichieritems import Gfichieritems
from mechaniquecombat import MécaniqueCombat
import copy
import pickle


class Jeu:

    def __init__(self):
        pygame.init()
        self.état = ÉtatJeu()
        self.état.ensemble_items = Gfichieritems.charge(C.DÉF_ITEMS_SOURCE)
        try:
            pickle_in = open('ressources\\save.chonker', 'rb')
            save_data = pickle.load(pickle_in)
            self.état.niveaux_init = save_data[3]
        except FileNotFoundError:
            self.état.niveaux_init = GFichierMonde.charge(C.DÉF_MONDE_SOURCE)
        self.état.niveaux = copy.deepcopy(self.état.niveaux_init)
        self.gévénement = GÉvènement(self.état)
        self.grendu = GRendu(C.TITRE, self.état)
        self.gétat = GÉtat(self.état)
        self.gévénement.gétat = self.gétat
        self.gétat.mécanique_combat = MécaniqueCombat(self.état)
        self.grendu.mécanique_combat = self.gétat.mécanique_combat
        self.état.usine_entité.mécanique_combat = self.gétat.mécanique_combat
        self.horloge = pygame.time.Clock()
        self.temps_accumulé = 0
        self.temps_écoulé = 0

    def exécute(self):
        self.état.état = C.ÉTAT_MENU
        pygame.mixer.music.load('ressources\\Musique\\Estavius.mp3')
        pygame.mixer.music.play(-1)
        while True:
            self.horloge.tick()

            self.temps_écoulé = self.horloge.get_time()

            self.temps_accumulé += self.temps_écoulé

            if not self.gévénement.traite():
                break

            no_actualisation = 0
            while (self.temps_accumulé >= self.état.dt and no_actualisation < 3):
                self.gétat.actualise()
                self.temps_accumulé -= self.état.dt
                no_actualisation += 1

            self.grendu.rend(self.temps_accumulé / self.état.dt)


if __name__ == '__main__':
    jeu = Jeu()
    jeu.exécute()
