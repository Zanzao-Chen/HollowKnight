class Player:
    def __init__(self, x, y, level=0): 
        self.x = x
        self.y = y
        self.level = level
        self.jumping = False
        self.falling = False
        self.positions = []
    def move(self, direction):
        self.x += direction

    def jump(self):
        self.jumping = True