from Entity import *

class GroundEnemy(Entity):
    def __init__(self, x, y, width, height, level=0):
        super().__init__(x, y, width, height, level)
        self.direction = -1
    def move(self):
        self.x += self.direction*self.speed
    def __repr__(self):
        return 'groundEnemy'

class GroundEnemyVertical(Entity):
    def __init__(self, x, y, width, height, level=0):
        super().__init__(x, y, width, height, level)
        self.direction = 0
    def move(self):
        self.x += self.direction*self.speed
    def __repr__(self):
        return 'groundEnemyVertical'