from tuiles.tuile import Tuile
from tuiles.tuiles import TuileTerrain, TuileFeu
import constantes as C
from composants.mouvementgrille import MouvementGrille


class TuileBascule(Tuile):

    def __init__(self):
        super().__init__()
        self.terrain = TuileTerrain()
        self.feu = TuileFeu()
        self.variante_tuile = self.terrain
        self.compteur = 90
        self.délai = 90

    def actualise(self, état):
        self.compteur -= 1

        if self.compteur <= 0:
            self.compteur = self.délai
            if self.variante == 'feu':
                self.variante = 'terrain'
                self.variante_tuile = self.terrain

            else:
                self.variante = 'feu'
                self.variante_tuile = self.feu

            mouvement = état.joueur.obtient_composant(MouvementGrille)
            if état.état != C.ÉTAT_ÉCHEC and mouvement.sx == mouvement.cx == self.x \
                    and mouvement.sy == mouvement.cy == self.y:

                self.sur_entrer(état, état.joueur)

        self.variante_tuile.actualise(état)

    def peut_entrer(self, caractère):
        return self.variante_tuile.peut_entrer(caractère)

    def sur_entrer(self, état, caractère):
        self.variante_tuile.sur_entrer(état, caractère)

    def sur_marche(self, état, caractère):
        self.variante_tuile.sur_marche(état, caractère)
