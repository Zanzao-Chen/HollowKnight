class Player:
    def __init__(self, x, y, width, height, level=0): 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level = level
        self.jumping = False
        self.positions = []
        self.timer = 0
        self.maxJumpHeight = 10

    def move(self, direction):
        self.x += direction

    def jump(self):
        self.positions.append(self.y)
        if self.jumping == True and self.y >= self.positions[0]:
            self.positions.append(self.y)
            newPosition = -(self.timer - self.y - (self.maxJumpHeight)**0.5) + self.maxJumpHeight
            if newPosition < self.positions[0]:
                self.positions.pop()
                self.jumping = False
                self.y = self.positions[0]
                self.positions = []
                self.timer = 0
            else:
                self.y = newPosition

    def getPlayerVertices(self):
        self.leftX = self.x
        self.rightX = self.x + self.width
        self.topY = -self.y
        self.bottomY = -self.y + self.height

        # topLeft = (self.x, self.y)
        # topRight = (self.x + self.width, self.y)
        # bottomLeft = (self.x, self.y + self.height)
        # bottomRight = (self.x + self.width, self.y + self.height)
        # return topLeft, topRight, bottomLeft, bottomRight
