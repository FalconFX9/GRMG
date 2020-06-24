class Orientable:

    def __init__(self, orientation, coût):
        self.orientation = orientation
        self.coût = coût
        self.recharge = None

    def arrête(self):
        self.recharge = None
