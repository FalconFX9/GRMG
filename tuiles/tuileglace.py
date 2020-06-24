from tuiles.tuile import Tuile
from composants.mouvementgrille import MouvementGrille
from composants.orientable import Orientable
from composants.controlable import Contrôlable


class TuileGlace(Tuile):
    def __init__(self):
        super().__init__()

    def peut_entrer(self, entité):
        return True

    def sur_entrer(self, état, entité):
        orientable = entité.obtient_composant(Orientable)
        contrôlable = entité.obtient_composant(Contrôlable)
        if orientable and contrôlable:
            contrôlable.force = orientable.orientation

    def sur_marche(self, état, entité):
        mouvement = entité.obtient_composant(MouvementGrille)
        contrôlable = entité.obtient_composant(Contrôlable)
        if mouvement and contrôlable:
            mouvement.vitesse *= 1.5
            contrôlable.force = 0
