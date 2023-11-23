import math
from cmu_graphics import *

class Entity:
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
        
        self.maxHealth = 5
        self.currentHealth = 5
        self.damageTook = 0
        self.healthList = [True]*self.maxHealth

        self.healthX = 20 # center of left-most health circle
        self.healthXInterval = 30
        self.healthY = 20 
        self.healthRadius = 10
        self.yesHealthColor = 'black'
        self.noHealthColor = 'grey'

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
        theta =  (self.rotateAngle/180)*math.pi 
        deltaX = (math.sin(theta))*self.longRadius
        deltaY = self.longRadius - (math.cos(theta))*self.longRadius
        self.orientationX = self.middleX - deltaX
        self.orientationY = self.bottomY - deltaY
        self.attackAppearDuration = 5

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
    
    def updateHealth(self, amount):
        self.currentHealth += amount
        self.damageTook = self.maxHealth - self.currentHealth
        self.healthList = [True]*self.currentHealth + [False]*self.damageTook

    def checkColliding(self, terrain):
        self.getPlayerVertices()
        if terrain.type == 'Rectangle':
            return self.checkCollidingRect(terrain)
        elif terrain.type == 'outerOval':
            return self.checkCollidingOuterOval(terrain)

    def checkCollidingRect(self, terrain):
        terrain.getTerrainVertices()
        if ((self.leftX > terrain.leftX) and (self.leftX < terrain.rightX) or
            (self.rightX > terrain.leftX) and (self.rightX < terrain.rightX)):
            if self.bottomY >= terrain.topY and self.bottomY <= terrain.bottomY:
                if len(self.previousPositions) <= 2:
                    return (True, 'down', terrain.topY)
                previousX, previousY = self.previousPositions[-2]
                if previousY + self.height <= terrain.topY:
                    return (True, 'down', terrain.topY)
        if ((self.bottomY > terrain.topY and self.bottomY < terrain.bottomY) or 
            (self.topY > terrain.topY and self.topY < terrain.bottomY)):
            if self.rightX >= terrain.leftX and self.rightX <= terrain.rightX:
                return (True, 'right', terrain.leftX) 
        if ((self.bottomY > terrain.topY and self.bottomY < terrain.bottomY) or 
            (self.topY > terrain.topY and self.topY < terrain.bottomY)):
            if self.leftX <= terrain.rightX and self.leftX >= terrain.leftX:
                return (True, 'left', terrain.rightX) 
        return False, None, None

    def checkCollidingOuterOval(self, terrain):
        if self.jumping == True and self.reachFallPortion == False:
            return False, None, None
        else:
            self.getPlayerVertices()
            terrain.getTerrainVertices()
            if ((self.orientationX-terrain.x)/(terrain.width/2))**2 + ((self.orientationY-terrain.y)/(terrain.height/2))**2 < 1:
                self.setAngle(terrain)
                self.getPlayerVertices()
                if ((self.orientationX-terrain.x)/(terrain.width/2))**2 + ((self.orientationY-terrain.y)/(terrain.height/2))**2 < 1:
                    return (True, 'down', self.orientationX)    
                if ((self.middleX-terrain.x)/(terrain.width/2))**2 + ((self.bottomY-terrain.y)/(terrain.height/2))**2 < 1:
                    return (True, 'down', self.orientationX)    
            return False, None, None
            
    def setAngle(self, terrain):
        xPartialDerivative =  2*(self.middleX - terrain.x)/((terrain.width/2)**2)
        yPartialDerivative = 2*(self.bottomY-terrain.y)/((terrain.height/2)**2)
        if yPartialDerivative == 0:
            self.rotateAngle = 0
            return
        alpha = math.atan(xPartialDerivative/(yPartialDerivative))*180/math.pi
        if alpha < 45 and alpha >= 0:
            self.rotateAngle = -alpha
        elif alpha >= 45:
            self.rotateAngle = -(90-alpha)
        elif alpha <= -45:
            self.rotateAngle = (90+alpha)
        elif alpha < 0 and alpha > -45:
            self.rotateAngle = -alpha

                    
