import math
from cmu_graphics import *

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
        self.speed = 3
        self.reachFallPortion = False
        self.gravity = 1.3
        self.rotateAngle = 0
        self.index = 1
        self.direction = 'right'
        self.attackWidth = 50
        self.isAttacking = False
        self.looksAttacking = False
        self.previousAttackTime = 0
        self.attackWidth = self.width
        self.attackHeight = self.height
        

    def move(self, direction):
        self.x += direction*self.speed

    def jump(self):
        self.positions.append(self.y)
        if self.jumping == True and self.y >= self.positions[0]:
            if self.reachMax():
                self.reachFallPortion = True
            else:
                self.reachFallPortion = False
            self.positions.append(self.y)
            newPosition = -(self.timer - self.y - (self.maxJumpHeight)**0.5) + self.maxJumpHeight
            self.y = newPosition
    def fall(self):
        if self.falling == True and self.jumping == False:
            self.y += -self.timer*self.gravity
        elif self.falling == True and self.jumping == True:
            self.y += -self.timer*self.gravity/2
        

    def reachMax(self):
        if self.timer*(1+self.gravity) >= (self.maxJumpHeight)**0.5 + self.maxJumpHeight:
            return True
        return False

    def getPlayerVertices(self):
        self.leftX = self.x
        self.rightX = self.x + self.width
        self.topY = -self.y
        self.bottomY = -self.y + self.height
        self.middleX = (self.rightX + self.leftX)/2
        self.middleY = (self.topY + self.bottomY)/2
        self.longRadius = self.height/2
        theta =  (self.rotateAngle/180)*math.pi # math.sin and math.cos uses radians, not degrees
        deltaX = (math.sin(theta))*self.longRadius
        deltaY = self.longRadius - (math.cos(theta))*self.longRadius
        self.orientationX = self.middleX - deltaX
        self.orientationY = self.bottomY - deltaY

    def getMiddleXFromOrientation(self, orientationY):
        self.longRadius = self.height/2
        theta =  (self.rotateAngle/180)*math.pi # math.sin and math.cos uses radians, not degrees
        deltaX = (math.sin(theta))*self.longRadius
        deltaY = self.longRadius - (math.cos(theta))*self.longRadius
        return orientationY + deltaY

    def resetAngle(self):
        if self.index >= abs(self.rotateAngle):
            self.rotateAngle = 0
            self.index = 1
        else:
            self.rotateAngle = self.rotateAngle/self.index
    def attack(self):
        if app.generalCounter - self.previousAttackTime >= 20:
            print(self.previousAttackTime, app.generalCounter, app.generalCounter - self.previousAttackTime)
            self.previousAttackTime = app.generalCounter
            self.attackX = self.x + (self.width if self.direction == 'right' else -self.attackWidth)
            self.attackY = self.y
            self.isAttacking = True
            self.looksAttacking = True
        

                
