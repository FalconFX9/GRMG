import constantes as C
from composants.controlable import Contrôlable
from composants.mouvementgrille import MouvementGrille
from composants.orientable import Orientable
from composants.position import Position
from composants.collisionneur import Collisionneur
from composants.joueur import Joueur
from composants.zombie import Zombie
from composants.boitealignee import BoîteAlignée
from composants.autonomiebouclee import AutonomieBouclée
from composants.autonomieciblee import AutonomieCiblée
from composants.inventaire import Inventaire
from composants.stats import Stats
from time import time
import random
import pickle


class GÉtat:
    __incoexistables = (
        lambda e1, e2: e1.contient_composant(
            Zombie) and e2.contient_composant(Zombie),
    )

    def __init__(self, état):
        self.mécanique_combat = None
        try:
            pickle_in = open('ressources\\save.chonker', 'rb')
            save_data = pickle.load(pickle_in)
        except FileNotFoundError:
            save_data = None
        self.état = état
        self.état.joueur = self.état.usine_entité.crée('joueur')
        if save_data:
            inventaire = self.état.joueur.obtient_composant(Inventaire)
            inventaire.inventaire = save_data[0]
            cx, cy = save_data[1]
            cx, cy = int(cx), int(cy)
            niveau_init = état.niveaux[save_data[2]]
        else:
            cx, cy = None, None
            niveau_init = None
            self.état.joueur.obtient_composant(Position).niveau = état.niveaux[(3, 3)]
        self.état.entités.append(self.état.joueur)
        self.état.joueur.obtient_composant(Inventaire).stats = self.état.joueur.obtient_composant(Stats)
        for niveau in self.état.niveaux.values():
            self.état.prépare_entités(niveau, True)
        if save_data:
            self.état.entités_détruites = save_data[4]
            for entité in self.état.entités:
                if entité.id in self.état.entités_détruites:
                    self.état.entités_à_détruire.add(entité)
            stats = self.état.joueur.obtient_composant(Stats)
            stats_sauvées = save_data[5]
            stats.lvl_up(stats_sauvées.niveau)
            inventaire.vérifie_stats()
            stats.XP = stats_sauvées.XP
            stats.HP = stats_sauvées.HP

        self.état.déplace_entité(self.état.joueur, niveau_init, cx, cy)
        self.temps = time()

    def __nettoie(self):
        while self.état.entités_à_détruire:
            entité = self.état.entités_à_détruire.pop()

            if entité.contient_composant(Joueur):
                self.état.état = C.ÉTAT_ÉCHEC

            else:
                if entité in self.état.entités:
                    self.état.entités.remove(entité)

    def __actualise_carré_débogage(self):
        if self.état.mode_débogage:
            self.état.carré_débogage_pos += 1

    def __actualise_mouvement_grille(self, entité):
        niveau = self.état.joueur.obtient_composant(Position).niveau
        position = entité.obtient_composant(Position)
        mouvement = entité.obtient_composant(MouvementGrille)

        # Le mouvement n'a pas de sense sans les composants position ou mouvement.
        if not position or not mouvement or position.niveau != niveau:
            return

        orientable = entité.obtient_composant(Orientable)
        contrôlable = entité.obtient_composant(Contrôlable)

        # Appliquer le mouvement si l'entité est en mouvement.
        if mouvement.recharge is not None:
            mouvement.recharge = mouvement.recharge - mouvement.vitesse
            if mouvement.recharge <= 0:
                self.état.déplace_entité(
                    entité, None, mouvement.cx, mouvement.cy)
            else:
                position.x, position.y = self.état.calcule_position(entité)
        elif orientable.recharge is not None:
            orientable.recharge = orientable.recharge - 1
            if orientable.recharge > 0:
                orientable.arrête()

        # Réinitialiser la vitesse de mouvement.
        mouvement.vitesse = 1
        if mouvement.recharge is None:
            self.__actualise_mvt_auto(entité)
        # Appliquer les mouvements à l'entité contrôlable qui n'est en mouvement.
        if contrôlable and contrôlable.force and not self.état.est_mouvement(entité):
            # Changer l'orientation de façon instantanée si le coût est 0 et l'orientation est incorrecte.
            if orientable and orientable.coût == 0 and contrôlable.force != orientable.orientation:
                orientable.orientation = contrôlable.force

            # Changer l'orientation si l'orientation est incorrecte.
            if orientable and contrôlable.force != orientable.orientation:
                orientable.orientation = contrôlable.force
                orientable.recharge = orientable.coût

            # Déplacer le joueur si l'orientation est correcte et si la tuile le permet.
            else:
                tuile = self.calcule_tuile_cible(entité, contrôlable.force)
                if tuile and self.__peut_entrer(position.niveau, tuile, entité):
                    mouvement.sx = position.x
                    mouvement.sy = position.y
                    mouvement.cx = tuile.x
                    mouvement.cy = tuile.y

                    mouvement.recharge = mouvement.coût

    def __peuvent_coexister(self, e1, e2):
        for fn in GÉtat.__incoexistables:
            if fn(e1, e2) or fn(e2, e1):
                return False
        # Putting false stops all entities from colliding
        return False

    def calcule_tuile_cible(self, entité, direction):
        position = entité.obtient_composant(Position)
        mouvement = entité.obtient_composant(MouvementGrille)

        # Une tuile cible n'a pas de sense s'il n'y a pas de position ou de mouvement.
        if not position or not mouvement:
            return None

        # Obtenir la position actuelle de l'entité.
        x = position.x
        y = position.y
        # Appliquer le mouvement dans la direction appropriée.
        if direction == C.DIRECTION_N:
            y -= 1
        elif direction == C.DIRECTION_O:
            x -= 1
        elif direction == C.DIRECTION_S:
            y += 1
        elif direction == C.DIRECTION_E:
            x += 1

        # Vérifier si le résultat est à l'intérieur de la carte.
        niveau = position.niveau
        if 0 <= x < niveau.l and 0 <= y < niveau.h:
            return niveau.carte[int(x)][int(y)]

        return None

    def __actualise_mvt_auto_bouclée(self, entité):
        ab = entité.obtient_composant(AutonomieBouclée)
        ctrl = entité.obtient_composant(Contrôlable)
        pos = entité.obtient_composant(Position)

        if not (ab and ctrl and pos):
            return

        cycle = ab.cycle
        x, y = cycle[0]

        if pos.x == x and pos.y == y:
            cycle.append(cycle.pop(0))
            x, y = cycle[0]

        if y < pos.y:
            ctrl.force = C.DIRECTION_N
        elif x < pos.x:
            ctrl.force = C.DIRECTION_O
        elif y > pos.y:
            ctrl.force = C.DIRECTION_S
        elif x > pos.x:
            ctrl.force = C.DIRECTION_E
        else:
            ctrl.force = None

    def __actualise_mvt_auto_ciblée(self, entité):
        ac = entité.obtient_composant(AutonomieCiblée)
        ctrl = entité.obtient_composant(Contrôlable)
        pos = entité.obtient_composant(Position)
        ori = entité.obtient_composant(Orientable)

        if not (ac and ctrl and pos):
            return

        pos_joueur = self.état.joueur.obtient_composant(Position)
        dir_joueur_x = C.DIRECTION_O if pos_joueur.x < pos.x else C.DIRECTION_E
        dir_joueur_y = C.DIRECTION_N if pos_joueur.y < pos.y else C.DIRECTION_S

        if pos_joueur.x == pos.x \
                and (not ori or ori.orientation == dir_joueur_y) \
                or pos_joueur.y == pos.y \
                and (not ori or ori.orientation == dir_joueur_x):

            if pos_joueur.x == pos.x and pos_joueur.y == pos.y:
                ctrl.force = None
            else:
                ctrl.force = ori.orientation

        else:
            dirs = [C.DIRECTION_N, C.DIRECTION_O, C.DIRECTION_S, C.DIRECTION_E]
            mode = random.random()

            if mode < 0.1:
                dirs.remove(ori.orientation)
                ctrl.force = random.choice(dirs)
            elif mode < 0.3:
                ctrl.force = ori.orientation if ori else random.choice(ori)
            else:
                ctrl.force = None

    def __actualise_mvt_auto(self, entité):
        if entité.obtient_composant(Position).niveau == self.état.joueur.obtient_composant(Position).niveau:
            self.__actualise_mvt_auto_bouclée(entité)
            self.__actualise_mvt_auto_ciblée(entité)

    def __actualise_carte(self):
        for colonne in self.état.joueur.niveau.carte:
            for tuile in colonne:
                tuile.actualise(self.état)

    def __actualise_tuiles(self):
        position = self.état.joueur.obtient_composant(Position)
        if not position:
            return

        for colonne in position.niveau.carte:
            for tuile in colonne:
                tuile.actualise(self.état)

    def __applique_effets_tuiles(self):
        for entité in list(self.état.entités):
            position = entité.obtient_composant(Position)
            if position:
                x, y = self.état.calcule_position(entité)
                tuile = position.niveau.carte[int(x)][int(y)]
                tuile.sur_marche(self.état, entité)

    def __peut_entrer(self, niveau, tuile, entité):
        # Vérifier si la tuile permet à l'entité d'entrer en premier.
        if not tuile.peut_entrer(entité):
            return False

        # Vérifier pour un entité dans la tuile cible qui n'accepte
        # pas que les deux entités coexistent dans la même tuile.
        # Seulement les entités avec des positions.
        for e in self.état.entités:
            # Exclure l'entité qui se déplace.
            if e == entité:
                continue

            # Exclure l'entité qui n'a pas de position ou qui n'est
            # pas dans le niveau de l'entité qui veut se déplacer.
            pn = e.obtient_composant(Position)
            if not pn or pn.niveau != niveau:
                continue

            # Une entité en mouvement occupe 2 tuiles: les tuiles source et cible.
            mvt = e.obtient_composant(MouvementGrille)
            if mvt:
                if mvt.recharge is not None:
                    if (mvt.sx == tuile.x and mvt.sy == tuile.y
                            or mvt.cx == tuile.x and mvt.cy == tuile.y) \
                            and not self.__peuvent_coexister(entité, e):
                        return False
                # Une entité fixe occupe une tuile.
                elif pn and pn.x == tuile.x and pn.y == tuile.y \
                        and not self.__peuvent_coexister(entité, e):
                    return False

        # Rien n'a empêché l'entré.
        return True

    def __actualise_physique(self):
        for entité in self.état.entités:
            self.__actualise_mouvement_grille(entité)

    def __applique_interactions_entités(self):
        # Travailler avec une copie de la liste au cas où des entités soient rajoutées.
        entités = list(self.état.entités)
        no_entités = len(entités)
        # Vérifier chaque entité.
        for i in range(no_entités):
            e1 = entités[i]
            collisionneur1 = e1.obtient_composant(Collisionneur)

            # Vérifier les entités après l'entité actuelle dans la liste.
            for j in range(i + 1, no_entités):
                e2 = entités[j]
                collisionneur2 = e2.obtient_composant(Collisionneur)

                # Si les deux entités n'ont pas de comportement lors d'une collision,
                # passe à la prochaine paire.
                if not collisionneur1 and not collisionneur2:
                    continue

                # Vérifier s'il y a une collision.
                if self.__en_collision(e1, e2):
                    # Appliquer le comportement de la première entité si elle a un comportement.
                    if collisionneur1:
                        collisionneur1.applique(self.état, e1, e2)

                    # Appliquer le comportement de la deuxième entité si elle a un comportement.
                    if collisionneur2:
                        collisionneur2.applique(self.état, e2, e1)

    def __en_collision(self, e1, e2):
        p1 = e1.obtient_composant(Position)
        p2 = e2.obtient_composant(Position)

        if p1.niveau.id == p2.niveau.id:

            # Utilise la boîte alignée. Si l'entitée n'a pas le
            # composant, la boîte mesure 0 unités.
            aabb1 = e1.obtient_composant(BoîteAlignée)
            if aabb1:
                minx1 = aabb1.minx
                miny1 = aabb1.miny
                maxx1 = aabb1.maxx
                maxy1 = aabb1.maxy
            else:
                minx1 = miny1 = maxx1 = maxy1 = 0

            # Utilise la boîte alignée. Si l'entitée n'a pas le
            # composant, la boîte mesure 0 unités.
            aabb2 = e2.obtient_composant(BoîteAlignée)
            if aabb2:
                minx2 = aabb2.minx
                miny2 = aabb2.miny
                maxx2 = aabb2.maxx
                maxy2 = aabb2.maxy
            else:
                minx2 = miny2 = maxx2 = maxy2 = 0

            # Vérifier l'intersection des boîtes.
            return p1.x + minx1 < p2.x + maxx2 \
                and p2.x + minx2 < p1.x + maxx1 \
                and p1.y + miny1 < p2.y + maxy2 \
                and p2.y + miny2 < p1.y + maxy1
        else:
            return False

    def __régen_lente(self):
        if self.temps + 1 <= time():
            stats = self.état.joueur.obtient_composant(Stats)
            if stats.HP < stats.HP_MAX:
                stats.HP += stats.HP_MAX * 0.01
                if stats.HP > stats.HP_MAX:
                    stats.HP = stats.HP_MAX
            self.temps = time()

    def __équipe_inventaire(self):
        liste_items = self.état.joueur.obtient_composant(Inventaire).inventaire
        liste_items.pop('argent')
        liste_items = list(liste_items)

    def actualise(self):
        if self.état.état == C.ÉTAT_NIVEAU:
            self.__régen_lente()
            self.__actualise_carré_débogage()
            self.__actualise_tuiles()
            self.__actualise_physique()
            self.__applique_effets_tuiles()
            self.__applique_interactions_entités()
            self.__nettoie()
        elif self.état.état == C.ÉTAT_COMBAT or self.état.état == C.ÉTAT_VICTOIRE:
            self.mécanique_combat.gestionnaire_tours()
            self.mécanique_combat.vérif_combat()
