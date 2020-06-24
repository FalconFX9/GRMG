TITRE = 'Mon jeu'
LARGEUR = 640
HAUTEUR = 580
HAUT_DPI = True
DESSIN_FOND = (0, 0, 0)
DT = (1000 / 180)
TUILE_TAILLE = 32
RESSOURCES = 'ressources/'
DÉF_MONDE_SOURCE = RESSOURCES + 'monde.megachonk'
DÉF_ITEMS_SOURCE = RESSOURCES + 'items.megachonk'
DÉF_SEP_B = ' '
DÉF_SEP_C = ';'
TUILE_TRANSPARENCE = (255, 127, 39)
JOUEUR_INIT_TUILES = 0
JOUEUR_INIT_RECTANGLE = 1
DÉF_BALISE_CARTE = 'carte'
DÉF_BALISE_CARTE_L2 = 'carte_l2'
DÉF_BALISE_CARTE_FIN = '/carte'
DÉF_BALISE_JOUEUR = 'joueur'
DÉF_BALISE_JOUEUR_TUILES = 'tuiles'
DÉF_BALISE_JOUEUR_RECTANGLE = 'rectangle'
DÉF_BALISE_NIVEAU = 'niveau'
DÉF_BALISE_NIVEAU_FIN = '/niveau'
TUILE_BORDURE = (255, 255, 255, 100)
DÉF_BALISE_ENTITÉ = 'entité'
DÉF_BALISE_ENTITÉ_FIN = '/entité'
DÉF_BALISE_POSITION = 'position'
DÉF_BALISE_AUTONOMIE_BOUCLÉE = 'autonomie_bouclée'
DÉF_BALISE_AUTONOMIE_CIBLÉE = 'autonomie_ciblée'
DÉF_BALISE_EPHEMERE = 'ephemere'
DÉF_BALISE_DIALOGUE = 'dialogue'
DÉF_BALISE_MARCHAND = 'marchand'
DÉF_BALISE_ITEM = 'item'
DÉF_BALISE_ITEM_ID = 'id'
DÉF_BALISE_ITEM_ATTAQUE = 'attaque'
DÉF_BALISE_ITEM_ARMURE = 'armure'
DÉF_BALISE_ITEM_PRIX = 'prix'
DÉF_BALISE_ITEM_TYPE = 'type'
DÉF_BALISE_ITEM_FIN = '/item'
DÉF_BALISE_COMBAT = 'combat'
JOUEUR_BORDURE = (255, 0, 0, 255)
DIRECTION_N, DIRECTION_E, DIRECTION_S, DIRECTION_O = 1, 2, 3, 4
JOUEUR_RECHARGE_DÉPLACEMENT = 36
RECHARGE_CLIC = 40
RECHARGE_ANIM = 150
RECHARGE_REGEN = 15000
ÉTAT_NIVEAU = 0
ÉTAT_ÉCHEC = 1
ÉTAT_PAUSE = 2
ÉTAT_COMBAT = 3
ÉTAT_VICTOIRE = 4
ÉTAT_MENU = 5
FIN_DU_JEU = 6
STATS_PAR_NIVEAU = {
    1: (500, 0, 20, 200),
    2: (600, 1, 25, 300),
    3: (700, 2, 30, 500),
    4: (700, 3, 40, 800),
    5: (900, 4, 50, 1100),
    6: (1000, 5, 60, 1400),
    7: (1100, 6, 80, 1700),
    8: (1200, 7, 100, 2000),
    9: (1300, 8, 120, 2400),
    10: (1400, 9, 140, 2800),
}
XP_PAR_ENNEMI = {
    'Chauve_Souris': 50,
    'FantomeNoir': 100,
    'SoldatSquel': 120,
    'OrbeBleue': 50,
    'SoldatSombre': 400,
    'Loup': 150,
    'Squelette': 90,
    'Diable': 150,
    'Boss': 1000,
}
