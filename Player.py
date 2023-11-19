class Player:
    def __init__(self, x, y, width, height, level=0): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.jumping = False
        self.falling = True
        self.positions = []
        self.previousPositions = []
        self.timer = 0
        self.maxJumpHeight = 20
        self.speed = 2

    def move(self, direction):
        self.x += direction*self.speed

    def jump(self):
        self.positions.append(self.y)
        if self.jumping == True and self.y >= self.positions[0]:
            self.positions.append(self.y)
            newPosition = -(self.timer - self.y - (self.maxJumpHeight)**0.5) + self.maxJumpHeight
            self.y = newPosition
    def fall(self):
        if self.falling == True:
            self.y += -self.timer**0.5

    def getPlayerVertices(self):
        self.leftX = self.x
        self.rightX = self.x + self.width
        self.topY = -self.y
        self.bottomY = -self.y + self.height
