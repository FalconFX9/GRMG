from tuiles.tuile import Tuile
from composants.inventaire import Inventaire
from composants.position import Position


class TuileCoffre(Tuile):
    def __init__(self):
        super().__init__()
        self.argent = None
        self.items = []
        self.ouvert = False

    def peut_entrer(self, entité):
        return False

    def sur_interaction(self, état, entité):
        inventaire = entité.obtient_composant(Inventaire)
        if not self.ouvert:
            if self.argent:
                inventaire.ajoute_argent(self.argent)
            for id in self.items:
                inventaire.add_item(état.ensemble_items[int(id)])
            if état.niveaux[entité.obtient_composant(Position).niveau.id].carte_l1[self.x][self.y].variante == '1060':
                état.niveaux[entité.obtient_composant(Position).niveau.id].carte_l1[self.x][self.y].variante = '1062'
            else:
                état.niveaux[entité.obtient_composant(Position).niveau.id].carte_l2[self.x][self.y].variante = '1062'
            self.ouvert = True
