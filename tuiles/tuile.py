from abc import ABC, abstractmethod


class Tuile(ABC):

    def __init__(self):
        self.x = None
        self.y = None
        self.couleur = None
        self.variante = None

    def actualise(self, état):
        pass

    @abstractmethod
    def peut_entrer(self, caractère):
        pass

    def sur_entrer(self, état, entité):
        pass

    def sur_marche(self, état, entité):
        pass

    def sur_interaction(self, état, entité):
        pass
