import math
from cmu_graphics import *
from Entity import *
from Vector import *

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
                if self.isCollidingWithOval == True:
                    self.alignAttacks()
                return
            self.attackWidth = self.width*3
            self.attackHeight = self.height*1.2
            if upwards == True and self.isCollidingWithOval == False:
                self.attackY = self.y + self.attackHeight
                self.attackX = self.leftX - (self.attackWidth - self.width)/2
                self.attackDirection = 'up'
            elif upwards == True and self.isCollidingWithOval == True:
                self.attackY = self.y + self.height + self.deltaY
                self.attackX = self.leftX + self.deltaX*2 - (self.attackWidth - self.width)/2 # times 2 because attack is based on self.leftX rather than self.middleX
                self.attackHeight = self.height 
                self.attackDirection = 'up'
            elif downwards == True and self.isCollidingWithOval == False:
                self.attackY = self.y - self.height
                self.attackX = self.leftX - (self.attackWidth - self.width)/2
                self.attackDirection = 'down'
            elif downwards == True and self.isCollidingWithOval == True:
                self.attackY = self.y - self.height + self.deltaY
                self.attackX = self.leftX - self.deltaX*2 - (self.attackWidth - self.width)/2
                self.attackHeight = self.height 
                self.attackDirection = 'down'
            self.isAttacking = True
            self.looksAttacking = True

    def dash(self):
        if self.direction == 'left':
            self.x -= self.dashDistance/self.dashDuration
            self.falling = False
            self.jumping = False
            self.isPogoing = False
            self.isPogoingWhileJumping = False
            self.dashing = True
        elif self.direction == 'right':
            self.x += self.dashDistance/self.dashDuration
            self.falling = False
            self.jumping = False
            self.isPogoing = False
            self.isPogoingWhileJumping = False
            self.dashing = True

    def attackKnockBack(self, enemy):
        if self.attackDirection == 'left':
            self.x += self.playerAttackKnockBackDistanceHorizontal
            enemy.x -= enemy.enemyAttackKnockBackDistanceHorizontal
        elif self.attackDirection == 'right':
            self.x -= self.playerAttackKnockBackDistanceHorizontal
            enemy.x += enemy.enemyAttackKnockBackDistanceHorizontal
        elif self.attackDirection == 'down':
            self.isPogoing = True
    def alignAttacks(self):
        self.previousAttackTime = app.generalCounter
        self.attackX = self.x + (self.width if self.direction == 'right' else -self.attackWidth)
        self.attackY = self.y
        self.getPlayerVertices()
        self.cornersRotated = []
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

        if self.rotateAngle == 0:
            shiftAttackX = self.attackWidth/2
            shiftAttackY = self.attackHeight/2
            self.vectorAttackRightX = Vector(middleX+shiftAttackX, middleY, attackAngle)
            self.vectorAttackLeftX = Vector(middleX-shiftAttackX, middleY, attackAngle)
            self.vectorAttackRightY = Vector(middleX+shiftAttackY, middleY, attackAngle+90)
            self.vectorAttackLeftY = Vector(middleX-shiftAttackY, middleY, attackAngle+90)
            self.cornersAttack=[(self.x, -self.y),
                                (self.attackX, -self.attackY+self.attackHeight),
                                (self.attackX+self.attackWidth, -self.attackY),
                                (self.attackX+self.attackWidth, -self.attackY+self.attackHeight)]
        else:
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
        middleX = self.middleX
        middleY = self.middleY

        if self.rotateAngle == 0:
            pass
        else:
            shiftX = (self.width/2)/(math.cos(self.rotateAngle*math.pi/180)+0.00001)
            shiftY = (self.height/2)/(math.sin(self.rotateAngle*math.pi/180)+0.00001)
            self.vectorRightX = Vector(middleX+shiftX, middleY, self.rotateAngle)
            self.vectorLeftX = Vector(middleX-shiftX, middleY, self.rotateAngle)
            self.vectorRightY = Vector(middleX+shiftY, middleY, self.rotateAngle+90)
            self.vectorLeftY = Vector(middleX-shiftY, middleY, self.rotateAngle+90)

            self.cornersRotated = [
                (self.vectorLeftX.getIntersection(self.vectorRightY)),
                (self.vectorLeftX.getIntersection(self.vectorLeftY)),
                (self.vectorRightX.getIntersection(self.vectorRightY)),
                (self.vectorRightX.getIntersection(self.vectorLeftY))
            ]

            if self.attackDirection == 'right':
                self.attackPointOfInterest = self.cornersAttack[0]
                self.originalPointOfInterest = self.cornersRotated[2]
                (x1, y1) = self.attackPointOfInterest
                (x2, y2) = self.originalPointOfInterest
                distance = self.distance(x1, y1, x2, y2)
                deltaX = math.sin(-self.rotateAngle*math.pi/180)*distance
                deltaY = math.cos(-self.rotateAngle*math.pi/180)*distance
                if self.rotateAngle > 0:
                    self.alignAttackX = deltaX
                    self.alignAttackY = -deltaY
                elif self.rotateAngle < 0:
                    self.alignAttackX = -deltaX
                    self.alignAttackY = deltaY
            elif self.attackDirection == 'left':
                self.attackPointOfInterest = self.cornersAttack[2]
                self.originalPointOfInterest = self.cornersRotated[0]
                (x1, y1) = self.attackPointOfInterest
                (x2, y2) = self.originalPointOfInterest
                distance = self.distance(x1, y1, x2, y2)
                deltaX = math.sin(-self.rotateAngle*math.pi/180)*distance
                deltaY = math.cos(-self.rotateAngle*math.pi/180)*distance
                if self.rotateAngle > 0:
                    self.alignAttackX = -deltaX
                    self.alignAttackY = deltaY
                elif self.rotateAngle < 0:
                    self.alignAttackX = deltaX
                    self.alignAttackY = -deltaY
            self.attackX += self.alignAttackX
            self.attackY += self.alignAttackY
                        
