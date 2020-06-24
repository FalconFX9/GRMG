from tuiles.tuile import Tuile


class TuileTerrain(Tuile):
    def __init__(self):
        super().__init__()

    def peut_entrer(self, entité):
        return True
