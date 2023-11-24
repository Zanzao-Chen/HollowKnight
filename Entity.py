import math
from cmu_graphics import *
from Vector import *


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
        self.attackWidth = self.width*5
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
        self.noHealthColor = 'white'
        self.holdingUp = False
        self.holdingDown = False
        self.isCollidingWithOval = False
        self.isKilled = False

        self.freezeDuration = 10
        self.freezeEverything = False
        self.stopFreeze = False
        self.isInvincible = False
        self.invincibleDuration = 60
        self.knockBackY = 50
        self.knockBackX = 100
        self.enemyCollisionDirection = None
        self.collidedEnemy = None
        self.startFallDuration = 3
        self.playerAttackDamage = 25

        self.dashing = False
        self.dashDuration = 5
        self.dashDistance = 100
        self.attackDirection = None

        self.dashingPositions = []
        self.test = False

        self.cornersAttack = []
        self.cornersEnemy = []
        self.projectedAttack = []
        self.projectedEnemy = []
        self.fourPointsAttack1 = []
        self.fourPointsAttack2 = []
        self.fourPointsEnemy1 = []
        self.fourPointsEnemy2 = []
        self.twoPointsAttack1 = []
        self.twoPointsAttack2 = []
        self.twoPointsEnemy1 = []
        self.twoPointsEnemy2 = []

        self.projectionCollisions = 0

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
        self.deltaX = (math.sin(theta))*self.longRadius
        self.deltaY = self.longRadius - (math.cos(theta))*self.longRadius
        self.orientationX = self.middleX - self.deltaX
        self.orientationY = self.bottomY - self.deltaY
        self.attackAppearDuration = 2
        self.timeBetweenAttacks = 20

    def getMiddleXFromOrientation(self, orientationY):
        self.longRadius = self.height/2
        theta =  (self.rotateAngle/180)*math.pi # math.sin and math.cos uses radians, not degrees
        self.deltaX = (math.sin(theta))*self.longRadius
        self.deltaY = self.longRadius - (math.cos(theta))*self.longRadius
        return orientationY + self.deltaY

    def resetAngle(self):
        if self.index >= abs(self.rotateAngle):
            self.rotateAngle = 0
            self.index = 1
        else:
            self.rotateAngle = self.rotateAngle/self.index
    
    def updateHealth(self, amount): # for player
        if self.currentHealth == -amount:
            self.isKilled = True
        elif self.currentHealth >= 1 and amount < 0 and self.isInvincible == False:
            self.currentHealth += amount
            self.damageTook = self.maxHealth - self.currentHealth
            self.healthList = [True]*self.currentHealth + [False]*self.damageTook
            self.isInvincible = True
            self.freezeEverything = True
        

    def knockBack(self, collisionDirection):
        self.y += self.knockBackY
        if collisionDirection == 'right':
            self.x -= self.knockBackX
        elif collisionDirection == 'left':
            self.x += self.knockBackX
        elif collisionDirection in ['up', 'down']:
            if self.x <= self.collidedEnemy.x:
                self.x -= self.knockBackX
            elif self.x > self.collidedEnemy.x:
                self.x += self.knockBackX
            


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

    def checkAttackColliding(self, enemy):
        self.cornersAttack = []
        self.cornersEnemy = []
        self.projectedEnemy = []
        self.projectedAttack = []
        self.fourPointsAttack1 = []
        self.fourPointsAttack2 = []
        self.fourPointsEnemy1 = []
        self.fourPointsEnemy2 = []

        topY = -self.attackY
        leftX = self.attackX
        bottomY = -(self.attackY - self.height)
        rightX = self.attackX + self.attackWidth
        middleX = (leftX + rightX)/2
        middleY = (topY + bottomY)/2
        attackAngle = self.rotateAngle
        self.vectorAttackX = Vector(middleX, middleY, attackAngle)
        self.vectorAttackY = Vector(middleX, middleY, attackAngle+90)
        
        shiftAttackX = (self.attackWidth/2)/(math.cos(attackAngle*math.pi/180)+0.00001)
        shiftAttackY = (self.attackHeight/2)/(math.sin(attackAngle*math.pi/180)+0.00001)
        self.vectorAttackRightX = Vector(middleX+shiftAttackX, middleY, attackAngle)
        self.vectorAttackLeftX = Vector(middleX-shiftAttackX, middleY, attackAngle)
        self.vectorAttackRightY = Vector(middleX+shiftAttackY, middleY, attackAngle+90)
        self.vectorAttackLeftY = Vector(middleX-shiftAttackY, middleY, attackAngle+90)

        self.cornersAttack = [
            (self.vectorAttackLeftX.getIntersection(self.vectorAttackRightY)),
            (self.vectorAttackLeftX.getIntersection(self.vectorAttackLeftY)),
            (self.vectorAttackRightX.getIntersection(self.vectorAttackRightY)),
            (self.vectorAttackRightX.getIntersection(self.vectorAttackLeftY))
        ]

        enemy.middleX = (enemy.leftX + enemy.rightX)/2
        enemy.middleY = (enemy.topY + enemy.bottomY)/2
        self.vectorEnemyX = Vector(enemy.middleX, enemy.middleY, enemy.rotateAngle)
        self.vectorEnemyY = Vector(enemy.middleX, enemy.middleY, enemy.rotateAngle+90)
        shiftEnemyX = (enemy.width/2) / (math.cos(enemy.rotateAngle*math.pi/180)+0.00001)
        shiftEnemyY = (enemy.height/2) / (math.sin(enemy.rotateAngle*math.pi/180)+0.00001)

        self.vectorEnemyRightX = Vector(enemy.middleX + shiftEnemyX, enemy.middleY, enemy.rotateAngle)
        self.vectorEnemyLeftX = Vector(enemy.middleX - shiftEnemyX, enemy.middleY, enemy.rotateAngle)
        self.vectorEnemyRightY = Vector(enemy.middleX + shiftEnemyY, enemy.middleY, enemy.rotateAngle + 90)
        self.vectorEnemyLeftY = Vector(enemy.middleX - shiftEnemyY, enemy.middleY, enemy.rotateAngle + 90)


        self.cornersEnemy = [
            self.vectorEnemyLeftX.getIntersection(self.vectorEnemyRightY),
            self.vectorEnemyLeftX.getIntersection(self.vectorEnemyLeftY),
            self.vectorEnemyRightX.getIntersection(self.vectorEnemyRightY),
            self.vectorEnemyRightX.getIntersection(self.vectorEnemyLeftY)
        ]

        for vector in [self.vectorEnemyX, 
                    self.vectorEnemyY]:
            for (x, y) in self.cornersAttack:
                self.projectedAttack.append(vector.getProjection(x, y))
        
        for vector in [self.vectorAttackX, 
                    self.vectorAttackY]:
            for (x, y) in self.cornersEnemy:
                self.projectedEnemy.append(vector.getProjection(x, y))

        self.fourPointsAttack1 = self.projectedAttack[:4]
        self.fourPointsAttack2 = self.projectedAttack[4:]
        self.fourPointsEnemy1 = self.projectedEnemy[:4]
        self.fourPointsEnemy2 = self.projectedEnemy[4:]

        self.twoPointsAttack1 = [max(self.fourPointsAttack1), min(self.fourPointsAttack1)]
        self.twoPointsAttack2 = [max(self.fourPointsAttack2), min(self.fourPointsAttack2)]
        self.twoPointsEnemy1 = [max(self.fourPointsEnemy1), min(self.fourPointsEnemy1)]
        self.twoPointsEnemy2 = [max(self.fourPointsEnemy2), min(self.fourPointsEnemy2)]

        # 0 top left, 1 bottom left, 2 top right, 3 bottom right
        (x0, y0) = self.cornersAttack[0]
        (x1, y1) = self.cornersAttack[1]
        (x2, y2) = self.cornersAttack[2]
        (x3, y3) = self.cornersAttack[3]
        referencePointAttack1X1 = ((x0+x2)/2, (y0+y2)/2)
        referencePointAttack1X2 = ((x1+x3)/2, (y1+y3)/2)
        referencePointAttack2X1 = ((x0+x1)/2, (y0+y1)/2)
        referencePointAttack2X2 = ((x2+x3)/2, (y2+y3)/2)

        (x0, y0) = self.cornersEnemy[0]
        (x1, y1) = self.cornersEnemy[1]
        (x2, y2) = self.cornersEnemy[2]
        (x3, y3) = self.cornersEnemy[3]
        referencePointEnemy1X1 = ((x0+x2)/2, (y0+y2)/2)
        referencePointEnemy1X2 = ((x1+x3)/2, (y1+y3)/2)
        referencePointEnemy2X1 = ((x0+x1)/2, (y0+y1)/2)
        referencePointEnemy2X2 = ((x2+x3)/2, (y2+y3)/2)
        
        
        [(endX1, endY1), (endX2, endY2)] = self.twoPointsEnemy1
        x0, y0 = referencePointAttack1X1[0], referencePointAttack1X1[1]
        x1, y1 = referencePointAttack1X2[0], referencePointAttack1X2[1]
        if ((x0 <= endX1 and x0 >= endX2) or (x0 >= endX1 and x0 <= endX2) or
            (x1 <= endX1 and x1 >= endX2) or (x1 >= endX1 and x1 <= endX2) or 
            (endX1 <= x0 and endX1 >= x1) or (endX1 >= x0 and endX1 <= x1) or
            (endX2 <= x0 and endX2 >= x1) or (endX2 >= x0 and endX2 <= x1)):
            self.projectionCollisions += 1

        [(endX1, endY1), (endX2, endY2)] = self.twoPointsEnemy2
        x0, y0 = referencePointAttack2X1[0], referencePointAttack2X1[1]
        x1, y1 = referencePointAttack2X2[0], referencePointAttack2X2[1]
        if ((x0 <= endX1 and x0 >= endX2) or (x0 >= endX1 and x0 <= endX2) or
            (x1 <= endX1 and x1 >= endX2) or (x1 >= endX1 and x1 <= endX2) or 
            (endX1 <= x0 and endX1 >= x1) or (endX1 >= x0 and endX1 <= x1) or
            (endX2 <= x0 and endX2 >= x1) or (endX2 >= x0 and endX2 <= x1)):
            self.projectionCollisions += 1
        
        
        [(endX1, endY1), (endX2, endY2)] = self.twoPointsAttack1
        x0, y0 = referencePointEnemy1X1[0], referencePointEnemy1X1[1]
        x1, y1 = referencePointEnemy1X2[0], referencePointEnemy1X2[1]
        if ((x0 <= endX1 and x0 >= endX2) or (x0 >= endX1 and x0 <= endX2) or
            (x1 <= endX1 and x1 >= endX2) or (x1 >= endX1 and x1 <= endX2) or 
            (endX1 <= x0 and endX1 >= x1) or (endX1 >= x0 and endX1 <= x1) or
            (endX2 <= x0 and endX2 >= x1) or (endX2 >= x0 and endX2 <= x1)):
            self.projectionCollisions += 1
        
        [(endX1, endY1), (endX2, endY2)] = self.twoPointsAttack2
        x0, y0 = referencePointEnemy2X1[0], referencePointEnemy2X1[1]
        x1, y1 = referencePointEnemy2X2[0], referencePointEnemy2X2[1]
        if ((x0 <= endX1 and x0 >= endX2) or (x0 >= endX1 and x0 <= endX2) or
            (x1 <= endX1 and x1 >= endX2) or (x1 >= endX1 and x1 <= endX2) or 
            (endX1 <= x0 and endX1 >= x1) or (endX1 >= x0 and endX1 <= x1) or
            (endX2 <= x0 and endX2 >= x1) or (endX2 >= x0 and endX2 <= x1)):
            self.projectionCollisions += 1

        if self.projectionCollisions == 4:
            self.projectionCollisions = 0
            return True
        else:
            self.projectionCollisions = 0
            return False
        


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
    
    def isCollidingRect(self, other):
        other.getPlayerVertices()
        if ((self.leftX >= other.leftX) and (self.leftX <= other.rightX) or
            (self.rightX >= other.leftX) and (self.rightX <= other.rightX)):
            if self.bottomY >= other.topY and self.bottomY <= other.bottomY:
                if len(self.previousPositions) <= 2:
                    return (True, 'down', other.topY)
                previousX, previousY = self.previousPositions[-2]
                if previousY + self.height <= other.topY:
                    return (True, 'down', other.topY)
        if ((self.bottomY >= other.topY and self.bottomY <= other.bottomY) or 
            (self.topY >= other.topY and self.topY <= other.bottomY)):
            if self.rightX >= other.leftX and self.rightX <= other.rightX:
                return (True, 'right', other.leftX) 
        if ((self.bottomY >= other.topY and self.bottomY <= other.bottomY) or 
            (self.topY >= other.topY and self.topY <= other.bottomY)):
            if self.leftX <= other.rightX and self.leftX >= other.leftX:
                return (True, 'left', other.rightX) 
        return False, None, None
    
    def takeDamageEnemy(self, damage):
        actualDamage = min(self.health, damage)
        self.health -= damage
        if self.health == 0:
            self.isKilled = True
                    
