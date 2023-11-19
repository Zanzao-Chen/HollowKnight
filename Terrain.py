class Terrain:
    def __init__(self, x, y, width, height, type, radius = None):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.type = type
        self.radius = radius
    def getTerrainVertices(self):
        self.leftX = self.x
        self.rightX = self.x + self.width
        self.topY = self.y
        self.bottomY = self.y + self.height
