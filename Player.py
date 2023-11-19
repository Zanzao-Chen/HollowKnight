class Player:
    def __init__(self, x, y, level=0): 
        self.x = x
        self.y = y
        self.level = level
        self.jumping = False
    def move(self, x, direction):
        self.x = x
        self.x += direction
    # def jump(self, y):
    #     self.jumping = True
    #     initialHeight = y
    #     while y < initialHeight + 10:
    #         self.y += 5
