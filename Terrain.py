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
    def getY(self, x):
        x += 10
        x0 = self.x
        y0 = self.y
        a = self.width/2
        b = self.height/2
        return -b*((1-((x-x0)/a)**2)**0.5) + y0