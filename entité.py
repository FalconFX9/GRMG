import constantes as C


class Entité:

    def __init__(self, id=None):
        self.id = id
        self.composants = {}

    def __str__(self):
        nom_composants = ', '.join(map(lambda type_composant: type_composant.__name__, self.composants))
        return f'Entité(id={self.id}),composants=[{nom_composants}]'

    def ajoute_composant(self, *composant):
        for c in composant:
            self.composants[c.__class__] = c

        return self

    def contient_composant(self, type_composant):
        return type_composant in self.composants

    def obtient_composant(self, type_composant):
        if type_composant not in self.composants:
            return None

        return self.composants[type_composant]

    def retire_composant(self, type_composant):
        if type_composant in self.composants:
            del self.composants[type_composant]
