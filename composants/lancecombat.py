import constantes as C


class LanceCombat:
    def __init__(self):
        self.entités_combat = {}

    def sur_interaction(self, état):
        état.état = C.ÉTAT_COMBAT
