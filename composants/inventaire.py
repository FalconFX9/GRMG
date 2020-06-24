class Inventaire:
    def __init__(self):
        self.inventaire = {}
        self.inventaire['argent'] = 0
        self.stats = None

    def ajoute_argent(self, argent):
        self.inventaire['argent'] += int(argent)

    def add_item(self, item):
        self.inventaire[item.id] = item
        self.stats.attaque += item.attaque
        self.stats.armure += item.armure

    def vérifie_stats(self):
        for item in self.inventaire.values():
            if type(item) is not int:
                self.stats.attaque += item.attaque
                self.stats.armure += item.armure

    def del_item(self, item):
        self.stats.attaque -= item.attaque
        self.stats.armure -= item.armure
        self.inventaire.pop(item.id)

    def print_items(self):
        print('\t'.join(['Name', 'Atk', 'Arm', 'Val']))
        for item in self.inventaire.values():
            print('\t'.join([str(x) for x in [item.name, item.attack, item.armor, item.price]]))
