import constantes as C
from boutton import Boutton
from composants.controlable import Contrôlable
from composants.mouvementgrille import MouvementGrille
from composants.orientable import Orientable
from composants.position import Position
from composants.joueur import Joueur
from composants.autonomiebouclee import AutonomieBouclée
from composants.autonomieciblee import AutonomieCiblée
from composants.ephemere import Ephemere
from composants.dialogue import Dialogue
from composants.marchand import Marchand
from composants.lancecombat import LanceCombat
from composants.stats import Stats
import random
import copy


class ÉtatJeu:

    def __init__(self):
        self.dt = C.DT
        self.état = C.ÉTAT_NIVEAU
        self.usine_entité = None

        self.carré_débogage_pos = 0
        self.mode_débogage = False

        self.niveaux = None
        self.joueur = None
        self.ensemble_items = None
        self.entités = []
        self.entités_à_détruire = set()
        self.entités_détruites = []
        self.entité_lance_combat = None
        self.bouttons = {}
        self.bouttons_cible = []
        self.bouttons_inventaire = []

        self.cache_images = None

        self.niveaux_init = None
        self.crée_bouttons()

    def crée_bouttons(self):
        self.bouttons['Attaque'] = Boutton(34, 242, 106, 30, 'Attaque', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons['Guérir'] = Boutton(34, 272, 106, 30, 'Guérir', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons['Fuir'] = Boutton(34, 302, 106, 30, 'Fuir', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons['Jouer'] = Boutton(261, 394, 182, 126, 'Jouer', (255, 255, 255, 0), (255, 255, 255, 128))
        self.bouttons_cible.append(Boutton(486, 86, 48, 48, None, None, None))
        self.bouttons_cible.append(Boutton(496, 206, 48, 48, None, None, None))
        self.bouttons_cible.append(Boutton(506, 326, 48, 48, None, None, None))
        self.bouttons_cible.append(Boutton(516, 446, 48, 48, None, None, None))
        for x in range(10):
            self.bouttons_inventaire.append(Boutton((x * 20) + 32, 552, 16, 16, None, (255, 255, 255, 0), (255, 255, 255, 128)))

    def calcule_position_initiale(self, mode, coordonnées):
        # Définir la position.
        if mode == C.JOUEUR_INIT_RECTANGLE:
            x1, y1 = coordonnées[0]
            x2, y2 = coordonnées[1]
            x = random.randint(x1, x2)
            y = random.randint(y1, y2)
        elif mode == C.JOUEUR_INIT_TUILES:
            x, y = random.choice(coordonnées)

        return x, y

    def détruit_entité(self, entité):
        self.entités_à_détruire.add(entité)
        if entité.id is not None and entité.id not in self.entités_détruites:
            self.entités_détruites.append(entité.id)

    def calcule_position(self, entité, interpolation=0):
        position = entité.obtient_composant(Position)
        if not position:
            return None, None

        mouvement = entité.obtient_composant(MouvementGrille)
        if mouvement and mouvement.recharge is not None:
            interp_mvt = min(1 - (mouvement.recharge - mouvement.vitesse * interpolation) / mouvement.coût, 1)

            return (mouvement.sx * (1 - interp_mvt) + mouvement.cx * interp_mvt), \
                (mouvement.sy * (1 - interp_mvt) + mouvement.cy * interp_mvt)

        # À (x, y) si l'entité n'a pas de mouvement.
        return position.x, position.y

    def est_mouvement(self, entité):
        mouvement = entité.obtient_composant(MouvementGrille)
        if mouvement and mouvement.recharge is not None:
            return True

        orientable = entité.obtient_composant(Orientable)
        if orientable and orientable.recharge is not None:
            return True

        return False

    def prépare_entités(self, niveau, init=False):
        def enj_positionnées(entité):
            position = entité.obtient_composant(Position)

            return not position or not position.niveau or entité.contient_composant(Joueur) or entité.contient_composant(Ephemere)

        self.entités = list(filter(enj_positionnées, self.entités))

        for données in niveau.entités_init:
            if 'ephemere' not in données.keys() or ('ephemere' in données.keys() and init):
                type_entité = données['type']
                entité = self.usine_entité.crée(type_entité)
                self.entités.append(entité)
                x, y = None, None
                if 'position' in données:
                    x, y = self.calcule_position_initiale(données['position'], données['position_coords'])

                if 'ephemere' in données:
                    entité.ajoute_composant(Ephemere())
                    if entité.id:
                        entité.id = (entité.id, données['ephemere'])
                    else:
                        entité.id = données['ephemere']

                if 'dialogue' in données:
                    entité.ajoute_composant(Dialogue(données['dialogue']))

                if 'marchand' in données:
                    entité.ajoute_composant(Marchand())
                    marchand = entité.obtient_composant(Marchand)
                    for id in données['marchand'][0]:
                        item = self.ensemble_items[int(id)]
                        marchand.items_demandés[item.id] = item
                    for id in données['marchand'][1]:
                        item = self.ensemble_items[int(id)]
                        marchand.items_donnés[item.id] = item

                if 'combat' in données:
                    entité.ajoute_composant(LanceCombat())
                    combat = entité.obtient_composant(LanceCombat)
                    conteur = 0
                    for données_ennemi in données['combat']:
                        ennemi = self.usine_entité.crée(données_ennemi[0])
                        combat.entités_combat[conteur] = ennemi
                        stats = ennemi.obtient_composant(Stats)
                        stats.lvl_up(int(données_ennemi[1]))
                        conteur += 1

                if 'autonomie_bouclée' in données:
                    cycle = données['autonomie_bouclée']
                    x, y = cycle[0]
                    cycle.append(cycle.pop(0))
                    entité.ajoute_composant(
                        Contrôlable(),
                        AutonomieBouclée(cycle)
                    )

                elif 'autonomie_ciblée' in données:
                    entité.ajoute_composant(
                        Contrôlable(),
                        AutonomieCiblée()
                    )

                entité.obtient_composant(Position).niveau = niveau
                self.déplace_entité(entité, None, x, y)

    def déplace_entité(self, entité, niveau=None, cx=None, cy=None):
        position = entité.obtient_composant(Position)
        if not position:
            return

        if niveau is None:
            niveau = position.niveau

        # Lorsque les coordonnées cibles sont manquantes, c'est pour qu'un joueur reviennent à la zone initiale.
        if cx is None or cy is None:
            # Abandonne le déplacement si les coordonnées cibles sont manquantes et ce n'est pas le joueur.
            if entité != self.joueur:
                return

            # Efface une partie de la position du joueur pour assurer un rechargement du niveau.
            position.niveau = None

            # Réinitialiser l'orientation.
            orientable = entité.obtient_composant(Orientable)
            if orientable:
                orientable.orientation = C.DIRECTION_E

            # Réinitialiser la force.
            contrôlable = entité.obtient_composant(Contrôlable)
            if contrôlable:
                contrôlable.force = None

            # Calcule la tuile d'atterrissage.
            cx, cy = self.calcule_position_initiale(niveau.joueur_init, niveau.joueur_init_coords)

        mouvement = entité.obtient_composant(MouvementGrille)
        if mouvement:
            mouvement.arrête()

        orientable = entité.obtient_composant(Orientable)
        if orientable:
            orientable.arrête()

        if entité == self.joueur and niveau != position.niveau:
            self.prépare_entités(niveau)

        déplacement = niveau != position.niveau or position.x != cx or position.y != cy

        if entité.obtient_composant(Joueur) and position.niveau is not None:
            if position.niveau.id != niveau.id:
                # self.réinitialise_niveau(position.niveau.id)
                pass

        position.niveau = niveau
        position.x = cx
        position.y = cy
        if déplacement:
            tuile = niveau.carte[cx][cy]
            tuile.sur_entrer(self, entité)
            x_niv, y_niv = niveau.id
            if cx == 0:
                self.déplace_entité(entité, self.niveaux[(x_niv - 1, y_niv)], 20, cy)
            elif cx == 21:
                self.déplace_entité(entité, self.niveaux[(x_niv + 1, y_niv)], 1, cy)
            elif cy == 0:
                self.déplace_entité(entité, self.niveaux[(x_niv, y_niv - 1)], cx, 15)
            elif cy == 16:
                self.déplace_entité(entité, self.niveaux[(x_niv, y_niv + 1)], cx, 1)

    def réinitialise_niveau(self, id_niveau):
        self.niveaux[id_niveau] = copy.deepcopy(self.niveaux_init[id_niveau])
