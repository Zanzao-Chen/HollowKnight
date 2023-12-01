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

class FlyEnemy(Entity):
    def __init__(self, x, y, width, height, health, type, level=0):
        super().__init__(x, y, width, height, level)
        self.initialX = x
        self.fireballX = x
        self.initialY = y
        self.initialHealth = health
        self.health = health
        self.type = type
        self.sightRadius = 500
        self.isMoving = True
        self.randomRadius = 200
        self.spawnDistance = 300
        self.teleportTimes = 0
        self.fireballSpeed = 0.03
        self.startShootFireball = False
        self.fireballRadius = 20

    def move(self, player):
        xDistance = self.x - player.x
        yDistance = self.y - player.y
        if xDistance < 10 and yDistance < 10:
            self.isMoving = False
        else:
            self.isMoving = True
        self.x -= xDistance/100
        self.y -= yDistance/100
    def moveRandom(self, x, y):
        xDistance = self.x - x
        yDistance = self.y - y
        self.x -= xDistance/100
        self.y -= yDistance/100
    def teleport(self, player):
        import random
        teleportX = random.randint(-self.randomRadius, self.randomRadius)
        teleportY = random.randint(100, 300)
        self.x = player.x + teleportX
        self.y = player.y + teleportY
    def shootFireball(self, x, y):
        self.isAttacking = True
        xDistance = self.x - x
        yDistance = self.y - y
        self.fireballX -= xDistance*self.fireballSpeed
        self.fireballY -= yDistance*self.fireballSpeed

    def fall(self):
        pass