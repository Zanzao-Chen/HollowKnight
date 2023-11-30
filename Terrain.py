class Terrain:
    def __init__(self, x, y, width, height, type, subtype, radius = None):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.type = type
        self.subtype = subtype
        self.radius = radius
    def __repr__(self):
        return f"{self.type} terrain, x: {self.x}, y:{self.y}"
    def getTerrainVertices(self):
        if self.type == 'Rectangle':
            self.leftX = self.x
            self.rightX = self.x + self.width
            self.topY = self.y
            self.bottomY = self.y + self.height
        elif self.type == 'outerOval' or self.type == 'innerOval':
            self.leftX = self.x - self.width/2
            self.rightX = self.x + self.width/2
            self.topY = self.y - self.height/2
            self.bottomY = self.y + self.height/2

    def getY(self, x):
        x0 = self.x
        y0 = self.y
        a = self.width/2
        b = self.height/2
        return -b*((1-((x-x0)/a)**2)**0.5) + y0
    
