from Entity import *
from Player import *

class GroundEnemy(Entity):
    def __init__(self, x, y, width, height, health, type, level=0):
        super().__init__(x, y, width, height, level)
        self.health = health
        self.direction = -1 # left
        self.type = type
        self.sightRange = 500
        self.isCharging = False
    def move(self):
        self.x += self.direction*self.speed*0.5
    def __repr__(self):
        return 'groundEnemy'
    def charge(self):
        self.x += self.direction*self.speed*1
        self.isCharging = True