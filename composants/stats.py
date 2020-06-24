import constantes as C


class Stats:
    def __init__(self, agilité, modificateur=(1, 1, 1, 1)):
        self.HP_MAX = None
        self.HP = None
        self.armure = None
        self.attaque = None
        self.XP = 0
        self.XP_MAX = None
        self.agilité = agilité
        self.niveau = 1
        self.stats_par_niveau = {}
        for niveau in range(1, len(C.STATS_PAR_NIVEAU) + 1):
            stats = []
            self.stats_par_niveau[niveau] = stats
            for x in range(4):
                stats.append(C.STATS_PAR_NIVEAU[niveau][x] * modificateur[x])
        self.lvl_up(self.niveau)
        self.HP = self.HP_MAX

    def vérifie_niveau(self):
        if self.XP >= self.XP_MAX:
            self.XP -= self.XP_MAX
            self.lvl_up(self.niveau + 1)
            return True
        else:
            return False

    def lvl_up(self, niveau):
        self.HP_MAX, self.armure, self.attaque, self.XP_MAX = self.stats_par_niveau[niveau]
        self.niveau = niveau

    def réinit_HP(self):
        self.HP = self.HP_MAX
