"""
TODO: Finir ce nouveau type de tuile
"""
from tuiles.tuile import Tuile


class TuilePanneau(Tuile):
    def __init__(self):
        super().__init__()
        self.texte = None

    def sur_interaction(self):
        pass
