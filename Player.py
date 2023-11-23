import math
from cmu_graphics import *
from Entity import *

class Player(Entity):
    def attack(self, upwards=False):  
        self.getPlayerVertices()
        if app.generalCounter - self.previousAttackTime >= self.timeBetweenAttacks:
            self.previousAttackTime = app.generalCounter
            self.attackX = self.x + (self.width if self.direction == 'right' else -self.attackWidth)
            
            if upwards and self.isCollidingWithOval == False:
                self.attackY = self.y + self.height
                self.attackX = self.leftX
            elif upwards and self.isCollidingWithOval == True:
                self.attackY = self.y + self.height + self.deltaY
                self.attackX = self.leftX + self.deltaX*2 # times 2 because attack is based on self.leftX rather than self.middleX
                self.attackHeight = self.height + 5
            else:
                self.attackY = self.y 
            
            self.isAttacking = True
            self.looksAttacking = True