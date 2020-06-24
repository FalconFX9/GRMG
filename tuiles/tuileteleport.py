from tuiles.tuile import Tuile


class TuileTéléport(Tuile):
    def __init__(self):
        super().__init__()
        self.cx = 0
        self.cy = 0
        self.cniveau = 0

    def peut_entrer(self, entité):
        return True

    def sur_entrer(self, état, entité):
        état.déplace_entité(entité, état.niveaux[self.cniveau], self.cx, self.cy)
