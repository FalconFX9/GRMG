from composants.inventaire import Inventaire


class Marchand:
    def __init__(self):
        self.items_demandés = {}
        self.items_donnés = {}
        self.items_manquants = []
        self.dialogue = None
        self.échange = False
        self.conteur = None

    def sur_échange(self, joueur):
        if not self.échange:
            inventaire = joueur.obtient_composant(Inventaire)
            for item in self.items_demandés.values():
                if item.id in inventaire.inventaire:
                    if item in self.items_manquants:
                        self.items_manquants.remove(item)
                elif item.id not in self.items_manquants:
                    self.dialogue = "L'item " + item.nom + " n'est pas dans votre inventaire"
                    if item not in self.items_manquants:
                        self.items_manquants.append(item)
                    break
            if len(self.items_manquants) == 0:
                for item in self.items_demandés.values():
                    inventaire.inventaire.pop(item.id)
                self.échange = True
                for item in self.items_donnés.values():
                    inventaire.add_item(item)
                self.items_manquants.append(None)
                self.dialogue = "Voici votre récompense : " + item.nom
