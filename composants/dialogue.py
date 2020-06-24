import constantes as C
from composants.orientable import Orientable


class Dialogue:
    def __init__(self, dialogue):
        self.dialogue = dialogue
        self.conteur = 0
        self.actif = False

    def sur_interaction(self, entité, joueur):
        self.actif = True
        orientation_joueur = joueur.obtient_composant(Orientable).orientation
        orientation = entité.obtient_composant(Orientable)
        if orientation_joueur == C.DIRECTION_N:
            orientation.orientation = C.DIRECTION_S
        elif orientation_joueur == C.DIRECTION_S:
            orientation.orientation = C.DIRECTION_N
        elif orientation_joueur == C.DIRECTION_E:
            orientation.orientation = C.DIRECTION_O
        elif orientation_joueur == C.DIRECTION_O:
            orientation.orientation = C.DIRECTION_E
        self.conteur += 1
