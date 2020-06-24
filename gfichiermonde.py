import constantes as C
from tuiles.tuiles import *
from niveau import Niveau
import copy


class GFichierMonde:

    TUILES = {'0': TuileTerrain,
              '2': TuileMur,
              '3': TuileEau,
              '4': TuileFeu,
              '5': TuileSable,
              '6': TuileTéléport,
              '7': TuileGlace,
              '8': TuileLevier,
              '9': TuileRude,
              'b': TuileBascule,
              'c': TuileCoffre
              }

    @staticmethod
    def __charge_fichier(fichier):
        with open(fichier, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def __convertisseur(données_tuile):
        if données_tuile == 't':
            return '0'
        elif données_tuile == 'm':
            return '2'
        elif données_tuile == 'e':
            return '3'
        elif données_tuile == 'f':
            return '4'
        elif données_tuile == 's':
            return '5'
        elif données_tuile == 'T':
            return '6'
        elif données_tuile == 'g':
            return '7'
        elif données_tuile == 'l':
            return '8'
        elif données_tuile == 'r':
            return '9'
        else:
            return données_tuile

    @staticmethod
    def __analyse_position(lignes):
        ligne = lignes.pop(0)
        parties = ligne.split()

        if parties[1] == C.DÉF_BALISE_JOUEUR_TUILES:
            type = C.JOUEUR_INIT_TUILES
        elif parties[1] == C.DÉF_BALISE_JOUEUR_RECTANGLE:
            type = C.JOUEUR_INIT_RECTANGLE

        coordonnées = []

        for partie in parties[2:]:
            x, y = partie.split(C.DÉF_SEP_C)
            coordonnées.append((int(x), int(y)))

        return type, coordonnées

    @staticmethod
    def __analyse_autonomie_bouclée(lignes):
        ligne = lignes.pop(0)
        parties = ligne.split()

        # Lire une liste de coordonnées.
        coordonnées = []
        for partie in parties[1:]:
            x, y = partie.split(C.DÉF_SEP_C)
            coordonnées.append((int(x), int(y)))

        return coordonnées

    @staticmethod
    def __analyse_marchand(lignes):
        ligne = lignes.pop(0)
        parties = ligne.split()

        # Lire une liste de coordonnées.
        items_reception = []
        items = parties[1].split(C.DÉF_SEP_C)
        for item in items:
            items_reception.append(item)
        items_donation = []
        items = parties[2].split(C.DÉF_SEP_C)
        for item in items:
            items_donation.append(item)

        return items_reception, items_donation

    @staticmethod
    def __analyse_carte(lignes):
        carte = []
        lignes.pop(0)
        y = 0
        while True:
            ligne = lignes.pop(0)
            if ligne == C.DÉF_BALISE_CARTE_FIN:
                break

            rangée = []
            carte.append(rangée)

            ligne = ligne.split(C.DÉF_SEP_B)

            for x, données_tuile in enumerate(ligne):
                if '-1' not in données_tuile:
                    tuile = GFichierMonde.__analyse_tuile(
                        GFichierMonde.__convertisseur(données_tuile), x, y)

                    rangée.append(tuile)
                else:
                    rangée.append(None)

            y += 1

        carte = list(zip(*carte))
        return carte

    @staticmethod
    def __analyse_tuile(données, x, y):
        données = données.split(C.DÉF_SEP_C)
        tuile = GFichierMonde.TUILES[données[0]]()
        tuile.x = x
        tuile.y = y
        type_tuile = type(tuile)

        if type_tuile == TuileTéléport:
            x_niv = int(données[1])
            y_niv = int(données[2])
            tuile.cniveau = (x_niv, y_niv)
            tuile.cx = int(données[3])
            tuile.cy = int(données[4])
            tuile.couleur = (int(données[5]), int(données[6]), int(données[7]))
        elif type_tuile == TuileLevier:
            tuile.cniveau = int(données[1])
            tuile.cx = int(données[2])
            tuile.cy = int(données[3])

            données_tuile_alt = C.DÉF_SEP_C.join(données[4:])

            tuile.tuile_alt = GFichierMonde.__analyse_tuile(
                données_tuile_alt, tuile.cx, tuile.cy)
        elif type_tuile == TuileBascule:
            tuile.variante = 'terrain'
        elif type_tuile == TuileCoffre:
            tuile.variante = données[1]
            if len(données) >= 3:
                tuile.argent = données[2]
            if len(données) > 3:
                for x in range(3, len(données)):
                    tuile.items.append(données[x])
        else:
            tuile.variante = données[1]

        return tuile

    @staticmethod
    def __analyse_niveau(lignes):
        niveau = Niveau()
        niveau.entités_init = []
        lignes.pop(0)

        i = 0
        while lignes:
            ligne = lignes[0]
            balise = ligne.split()[0]

            if balise == C.DÉF_BALISE_CARTE:
                niveau.carte_l1 = GFichierMonde.__analyse_carte(lignes)
                niveau.l = len(niveau.carte_l1)
                niveau.h = len(niveau.carte_l1[0])
            elif balise == C.DÉF_BALISE_CARTE_L2:
                niveau.carte_l2 = GFichierMonde.__analyse_carte(lignes)
            elif balise == C.DÉF_BALISE_JOUEUR:
                niveau.joueur_init, niveau.joueur_init_coords = GFichierMonde.__analyse_joueur(
                    lignes)
            elif balise == C.DÉF_BALISE_NIVEAU_FIN:
                lignes.pop(0)
                break
            elif balise == C.DÉF_BALISE_ENTITÉ:
                entité = GFichierMonde.__analyse_entité(lignes)
                niveau.entités_init.append(entité)
            else:
                lignes.pop(i - 1)
            i += 1
        niveau.carte = list(niveau.carte_l1)
        for y in range(niveau.h):
            for x in range(niveau.l):
                if niveau.carte_l2[x][y]:
                    niveau.carte[x] = list(niveau.carte[x])
                    niveau.carte[x][y] = niveau.carte_l2[x][y]

        return niveau

    @staticmethod
    def __analyse_jeu(lignes):
        niveaux = {}

        while lignes:
            ligne = lignes[0]
            parties = ligne.split()
            balise = parties[0]

            if balise == C.DÉF_BALISE_NIVEAU:
                niveau = GFichierMonde.__analyse_niveau(lignes)
                niveau.id = int(parties[1]), int(parties[2])

                niveaux[niveau.id] = niveau

            else:
                raise ValueError(f'Balise inconue: {balise}')

        return niveaux

    @staticmethod
    def charge(fichier):
        données = GFichierMonde.__charge_fichier(fichier)
        lignes = données.splitlines()
        lignes = list(filter(len, lignes))
        lignes = list(map(str.strip, lignes))
        niveaux = GFichierMonde.__analyse_jeu(lignes)
        return niveaux

    @staticmethod
    def __analyse_joueur(lignes):
        return GFichierMonde.__analyse_position(lignes)

    @staticmethod
    def __analyse_combat(lignes, balise):
        ligne = lignes.pop(0)
        parties = ligne.split()
        parties.remove(balise)
        entités = []
        for partie in parties:
            entités.append(partie.split(C.DÉF_SEP_C))
        return entités

    @staticmethod
    def __analyse_entité(lignes):
        données = {}

        ligne = lignes.pop(0)
        parties = ligne.split()

        données['type'] = parties[1]

        while lignes:
            ligne = lignes[0]
            balise = ligne.split()[0]

            if balise == C.DÉF_BALISE_POSITION:
                données['position'], données['position_coords'] = GFichierMonde.__analyse_position(
                    lignes)
            elif balise == C.DÉF_BALISE_AUTONOMIE_BOUCLÉE:
                données['autonomie_bouclée'] = GFichierMonde.__analyse_autonomie_bouclée(
                    lignes)
            elif balise == C.DÉF_BALISE_AUTONOMIE_CIBLÉE:
                lignes.pop(0)
                données['autonomie_ciblée'] = True
            elif balise == C.DÉF_BALISE_EPHEMERE:
                ligne = lignes.pop(0)
                id = ligne.split()
                données['ephemere'] = id[1]
            elif balise == C.DÉF_BALISE_DIALOGUE:
                ligne = lignes.pop(0)
                dialogue = ligne.split(C.DÉF_SEP_C)
                dialogue.remove(balise + " ")
                données['dialogue'] = dialogue
            elif balise == C.DÉF_BALISE_MARCHAND:
                données['marchand'] = GFichierMonde.__analyse_marchand(lignes)
            elif balise == C.DÉF_BALISE_COMBAT:
                données['combat'] = GFichierMonde.__analyse_combat(lignes, balise)
            elif balise == C.DÉF_BALISE_ENTITÉ_FIN:
                lignes.pop(0)
                break
            else:
                raise ValueError(f'Balise inconnue: {balise}')

        return données
