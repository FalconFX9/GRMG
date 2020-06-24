class Boutton:
    def __init__(self, x, y, l , h, texte, c1, c2):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.texte = texte
        self.c1 = c1
        self.c2 = c2
        self.souris_dessus = False
        self.cliqué = False

    def obtiens_rect(self):
        return (self.x, self.y, self.l , self.h)
