import math
from cmu_graphics import *
from Entity import *

class Player(Entity):
    def attack(self):
        if app.generalCounter - self.previousAttackTime >= 20:
            print(self.previousAttackTime, app.generalCounter, app.generalCounter - self.previousAttackTime)
            self.previousAttackTime = app.generalCounter
            self.attackX = self.x + (self.width if self.direction == 'right' else -self.attackWidth)
            self.attackY = self.y
            self.isAttacking = True
            self.looksAttacking = True