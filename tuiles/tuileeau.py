from tuiles.tuile import Tuile
from composants.position import Position
from composants.mouvementgrille import MouvementGrille
from composants.inventaire import Inventaire


class TuileEau(Tuile):
    def __init__(self):
        super().__init__()

    def peut_entrer(self, entité):
        inventaire = entité.obtient_composant(Inventaire)
        if 132 in inventaire.inventaire.keys():
            return True
        else:
            return False

    def sur_entrer(self, état, entité):
        mouvement = entité.obtient_composant(MouvementGrille)
        if mouvement:
            mouvement.vitesse *= 0.8
        """
        position = entité.obtient_composant(Position)
        mouvement = entité.obtient_composant(MouvementGrille)
        if position and mouvement:
            mouvement.recharge = mouvement.coût
            mouvement.sx = mouvement.cx = position.x
            mouvement.sy = mouvement.cy = position.y
        """
