import math
from cmu_graphics import *
from Entity import *

class Player(Entity):
    def attack(self, upwards=False, downwards=False): 
        self.getPlayerVertices()
        if app.generalCounter - self.previousAttackTime >= self.timeBetweenAttacks:
            self.previousAttackTime = app.generalCounter
            self.attackX = self.x + (self.width if self.direction == 'right' else -self.attackWidth)
            if downwards == False and upwards == False:
                self.attackWidth = self.width*5
                self.attackHeight = self.height
                self.attackY = self.y 
                self.attackDirection = self.direction
                self.isAttacking = True
                self.looksAttacking = True
                return
            self.attackWidth = self.width*5
            self.attackHeight = self.height
            if upwards == True and self.isCollidingWithOval == False:
                self.attackWidth = self.width
                self.attackHeight = self.height*2
                self.attackY = self.y + self.attackHeight
                self.attackX = self.leftX - (self.attackWidth - self.width)/2
                self.attackDirection = 'up'
            elif upwards == True and self.isCollidingWithOval == True:
                self.attackY = self.y + self.height + self.deltaY
                self.attackX = self.leftX + self.deltaX*2 - (self.attackWidth - self.width)/2 # times 2 because attack is based on self.leftX rather than self.middleX
                self.attackHeight = self.height + 5
                self.attackDirection = 'up'
            elif downwards == True and self.isCollidingWithOval == False:
                self.attackWidth = self.width
                self.attackHeight = self.height*2
                self.attackY = self.y - self.height
                self.attackX = self.leftX - (self.attackWidth - self.width)/2
            elif downwards == True and self.isCollidingWithOval == True:
                self.attackWidth = self.width*5
                self.attackY = self.y - self.height + self.deltaY + 5
                self.attackX = self.leftX - self.deltaX*2 - (self.attackWidth - self.width)/2
                self.attackHeight = self.height + 5
                self.attackDirection = 'down'
            self.isAttacking = True
            self.looksAttacking = True

    def dash(self):
        if self.direction == 'left':
            self.x -= self.dashDistance/self.dashDuration
            self.falling = False
            self.jumping = False
            self.isPogoing = False
            self.dashing = True
        elif self.direction == 'right':
            self.x += self.dashDistance/self.dashDuration
            self.falling = False
            self.jumping = False
            self.isPogoing = False
            self.dashing = True

    def attackKnockBack(self, enemy):
        if self.attackDirection == 'left':
            self.x += self.playerAttackKnockBackDistanceHorizontal
            enemy.x -= enemy.enemyAttackKnockBackDistanceHorizontal
        elif self.attackDirection == 'right':
            self.x -= self.playerAttackKnockBackDistanceHorizontal
            enemy.x += enemy.enemyAttackKnockBackDistanceHorizontal
        elif self.attackDirection == 'up':
            enemy.y += enemy.enemyKnockBackDistanceVertical
        elif self.attackDirection == 'down':
            self.isPogoing = True