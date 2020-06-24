from tuiles.tuile import Tuile


class TuileLevier(Tuile):

    def __init__(self):
        super().__init__()
        self.cniveau = None
        self.cx = None
        self.cy = None
        self.tuile_alt = None

    def peut_entrer(self, entité):
        return True

    def sur_entrer(self, état, entité):
        carte = état.niveaux[self.cniveau].carte

        tuile_actuelle = carte[self.cx][self.cy]

        carte[self.cx] = list(carte[self.cx])

        carte[self.cx][self.cy] = self.tuile_alt

        self.tuile_alt = tuile_actuelle
