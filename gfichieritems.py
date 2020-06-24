import constantes as C
from composants.item import Item


class Gfichieritems:

    def __charge_fichier(fichier):
        with open(fichier, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def __analyse_item(lignes):
        données = {}

        ligne = lignes.pop(0)
        parties = ligne.split()

        données['nom'] = parties[1]

        while lignes:
            ligne = lignes.pop(0)
            parties = ligne.split()
            balise = parties[0]

            if balise == C.DÉF_BALISE_ITEM_ID:
                données['id'] = int(parties[1])
            elif balise == C.DÉF_BALISE_ITEM_ATTAQUE:
                données['attaque'] = int(parties[1])
            elif balise == C.DÉF_BALISE_ITEM_ARMURE:
                données['armure'] = int(parties[1])
            elif balise == C.DÉF_BALISE_ITEM_PRIX:
                données['prix'] = int(parties[1])
            elif balise == C.DÉF_BALISE_ITEM_TYPE:
                pass
                # données['type'] = int(parties[1])
            elif balise == C.DÉF_BALISE_ITEM_FIN:
                break
            else:
                raise ValueError(f'Balise inconnue: {balise}')

        return données

    @staticmethod
    def __trouve_items(lignes):
        items = {}

        while lignes:
            ligne = lignes[0]
            balise = ligne.split()[0]

            if balise == C.DÉF_BALISE_ITEM:
                item = Gfichieritems.__analyse_item(lignes)
                items[item['id']] = item
            else:
                raise ValueError(f'Balise inconue: {balise}')

        return items

    @staticmethod
    def charge(fichier):
        données = Gfichieritems.__charge_fichier(fichier)
        lignes = données.splitlines()
        lignes = list(filter(len, lignes))
        lignes = list(map(str.strip, lignes))
        items_texte = Gfichieritems.__trouve_items(lignes)
        items = {}
        for données in items_texte.values():
            item = Item()
            item.nom = données['nom']
            item.id = données['id']
            item.attaque = données['attaque']
            item.armure = données['armure']
            item.prix = données['prix']
            #item.type = données['type']
            items[item.id] = item
        return items
