import constantes as C
from tuiles.tuile import Tuile
from composants.joueur import Joueur


class TuileFeu(Tuile):
    def __init__(self):
        super().__init__()

    def peut_entrer(self, entité):
        return True

    def sur_entrer(self, état, entité):
        if entité.contient_composant(Joueur):
            état.état = C.ÉTAT_ÉCHEC
