from tuiles.tuile import Tuile
from composants.mouvementgrille import MouvementGrille


class TuileSable(Tuile):
    def __init__(self):
        super().__init__()

    def peut_entrer(self, entité):
        return True

    def sur_marche(self, état, entité):
        mouvement = entité.obtient_composant(MouvementGrille)
        if mouvement:
            mouvement.vitesse *= 0.5
