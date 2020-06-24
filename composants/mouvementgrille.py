class MouvementGrille:

    def __init__(self, coût):
        self.coût = coût
        self.sx = None
        self.sy = None
        self.cx = None
        self.cy = None
        self.vitesse = 1
        self.recharge = None
        self.recharge_dessin = None

    def arrête(self):
        self.sx = self.sy = self.cx = self.cy = None
        self.recharge = None