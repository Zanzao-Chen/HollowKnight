class Player:
    def __init__(self, x, y, level=0): 
        self.x = x
        self.y = y
        self.level = level
        self.jumping = False
        self.positions = []
        self.timer = 0
        self.maxJumpHeight = 10
    def move(self, direction):
        self.x += direction

    def jump(self):
        if self.jumping == True:
            self.positions.append(self.y)
        if self.jumping == True and self.y >= self.positions[0]:
            self.y = -(self.timer - self.y - (self.maxJumpHeight)**0.5) + self.maxJumpHeight
        else:
            self.jumping = False
            self.positions = []
            self.timer = 0