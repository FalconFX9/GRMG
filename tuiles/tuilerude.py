from tuiles.tuile import Tuile
from tuiles.tuiles import TuileFeu
from composants.position import Position


class TuileRude(Tuile):

    def __init__(self):
        super().__init__()
        self.cniveau = None

    def peut_entrer(self, entité):
        return True

    def sur_entrer(self, état, entité):
        tuile = TuileFeu()
        tuile.x = self.x
        tuile.y = self.y
        position = entité.obtient_composant(Position)
        carte = état.niveaux[position.niveau.id].carte

        carte[self.x] = list(carte[self.x])

        carte[self.x][self.y] = tuile

        tuile.sur_entrer(état, entité)
