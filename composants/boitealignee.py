class BoîteAlignée:
    def __init__(self, x1, y1, x2, y2):
        self.minx = min(x1, x2)
        self.miny = min(y1, y2)
        self.maxx = max(x1, x2)
        self.maxy = max(y1, y2)
