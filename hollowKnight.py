from cmu_graphics import *
from Player import *
from Terrain import *
from Enemy import *

def onAppStart(app):
    app.stepsPerSecond = 30
    app.generalAttackCounter = 0
    app.previousAttackTime = 0
    app.initialAttackCounter = 0
    app.generalCounter = 0
    app.generalFreezeCounter = 0
    app.initialFreezeCounter = 0
    app.generalInvincibleCounter = 0
    app.initialInvincibleCounter = 0

player = Player(215, -100, 20, 50)
flat1 = Terrain(0, 250, app.width, 50, 'Rectangle')
flat2 = Terrain(200, 230, app.width*2, 50, 'Rectangle')
flat3 = Terrain(0, 230, 50, 50, 'Rectangle')
oval1 = Terrain(650, 230, 100, 50, 'outerOval')
oval2 = Terrain(650, 1000, 1000, 1600, 'outerOval')
groundEnemy1 = GroundEnemy(400, 100, 30, 30, None)
groundEnemy2 = GroundEnemy(800, 100, 30, 30, None)

terrainsList = [flat1, flat2, flat3, oval1, oval2]
enemyList = [groundEnemy1, groundEnemy2]

def redrawAll(app):
    player.getPlayerVertices()
    drawEnemies(app)
    drawAttacks(app)
    drawHealth(app)
    drawPlayer(app)
    recordPreviousPositions(app)
    drawTerrain(app)

def drawHealth(app):
    for i in range(len(player.healthList)):
        if player.healthList[i] == True:
            drawCircle(player.healthX+player.healthXInterval*i, player.healthY, player.healthRadius, fill=player.yesHealthColor)
        else:
            drawCircle(player.healthX+player.healthXInterval*i, player.healthY, player.healthRadius, fill=player.noHealthColor)

def drawPlayer(app):
    drawRect(player.x, -player.y, player.width, player.height, fill = 'black', rotateAngle = player.rotateAngle)
    drawCircle(player.orientationX, player.orientationY, 3, fill='red')

def recordPreviousPositions(app):
    player.previousPositions.append((player.x, -player.y))
    if len(player.previousPositions) > 5:
        player.previousPositions = player.previousPositions[2:]
    for enemy in enemyList:
        enemy.previousPositions.append((enemy.x, -enemy.y))
        if len(enemy.previousPositions) > 5:
            enemy.previousPositions = enemy.previousPositions[2:]

def drawTerrain(app):
    for terrain in terrainsList:
        if terrain.type == 'Rectangle':
            drawRect(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')
        elif terrain.type == 'outerOval':
            drawOval(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')

def drawAttacks(app):
    if player.isAttacking == True or player.looksAttacking == True:
        drawRect(player.attackX, -player.attackY, player.attackWidth, player.attackHeight, fill='red', rotateAngle=player.rotateAngle)
        player.isAttacking = False

def drawEnemies(app):
    for enemy in enemyList:
        drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle)

def onKeyPress(app, key):
    if player.freezeEverything == False:
        if key == 'a':
            player.direction = 'left'
            player.move(-1)
            for terrain in terrainsList:
                implementLeftRightCollisions(player, terrain)
        elif key == 'd':
            player.direction = 'right'
            player.move(+1)
            for terrain in terrainsList:
                implementLeftRightCollisions(player, terrain)
        if key == 'o' and player.jumping == False:
            player.jumping = True
        if key == 'j':
            if player.holdingUp == True:
                player.attack(upwards=True) 
                player.holdingUp = False
            elif player.holdingDown == True:
                player.attack(downwards=True) 
                player.holdingDown = False
            else:
                player.attack()

def onKeyHold(app, key):
    if player.freezeEverything == False:
        if 'a' in key:
            player.move(-1)
            player.direction = 'left'
            for terrain in terrainsList:
                implementLeftRightCollisions(player, terrain)
        elif 'd' in key:
            player.direction = 'right'
            player.move(+1)
            for terrain in terrainsList:
                implementLeftRightCollisions(player, terrain)
        if 'w' in key:
            player.holdingUp = True
        if 's' in key:
            player.holdingDown = True
        if 'j' in key:
            if 'w' in key:
                player.attack(upwards=True) 
            elif 's' in key:
                player.attack(downwards=True)
            else:
                player.attack()

def onStep(app):
    if player.freezeEverything == True:
        app.generalFreezeCounter += 1
        if app.generalFreezeCounter - app.initialFreezeCounter > player.freezeDuration:
            app.initialFreezeCounter = app.generalFreezeCounter
            player.freezeEverything = False
            player.stopFreeze = True
       
    
    elif player.freezeEverything == False:
        app.generalCounter += 1
        for enemy in enemyList:
            (isColliding, direction, reference) = player.isCollidingRect(enemy)
            if isColliding == True:
                player.updateHealth(-1)
                player.enemyCollisionDirection = direction
                player.collidedEnemy = enemy

        if player.stopFreeze == True:
            player.knockBack(player.enemyCollisionDirection)
            print('yes')
            player.stopFreeze = False

        if player.isInvincible == True:
            app.generalInvincibleCounter += 1
            if app.generalInvincibleCounter - app.initialInvincibleCounter > player.invincibleDuration:
                app.initialInvincibleCounter = app.generalInvincibleCounter
                player.isInvincible = False

        if player.looksAttacking:
            app.generalAttackCounter += 1
            if app.generalAttackCounter - app.initialAttackCounter > player.attackAppearDuration:
                app.initialAttackCounter = app.generalAttackCounter
                player.looksAttacking = False

        for enemy in enemyList:
            if enemy.falling:
                enemy.timer += 1
                enemy.fall()

        for terrain in terrainsList:
            for enemy in enemyList:
                isColliding = False
                (isColliding, direction, reference) = enemy.checkColliding(terrain)
                if isColliding and terrain.type == 'Rectangle' and direction in ['left', 'right']:
                    enemy.direction *= -1
                if not isColliding and terrain.type == 'outerOval':
                    enemy.isCollidingWithOval = False
                if isColliding and terrain.type == 'Rectangle':
                    if enemy.rotateAngle != 0:
                        enemy.index += 0.05
                        enemy.resetAngle()
                    if direction == 'right':
                        enemy.x = reference - enemy.width
                    elif direction == 'left':
                        enemy.x = reference
                    elif direction == 'up':
                        enemy.y = terrain.bottomY
                    elif direction == 'down':
                        enemy.y = -(reference - enemy.height)
                        enemy.jumping = False
                        enemy.positions = []
                        enemy.timer = 0
                elif isColliding and terrain.type == 'outerOval':
                    enemy.isCollidingWithOval = True
                    if direction == 'down':
                        enemy.getPlayerVertices()
                        getY = terrain.getY(enemy.orientationX)
                        realY = enemy.getMiddleXFromOrientation(getY)
                        enemy.y = -(realY - enemy.height)
                        enemy.jumping = False
                        enemy.positions = []
                        enemy.timer = 0

        for enemy in enemyList:
            enemy.move()
        for terrain in terrainsList:
            implementLeftRightCollisions(enemy, terrain)

        if player.falling:
            player.timer += 1
            player.fall()
        if player.jumping:
            player.timer += 1
            player.jump()
        for terrain in terrainsList:
            isColliding = False
            (isColliding, direction, reference) = player.checkColliding(terrain)
            if not isColliding and terrain.type == 'outerOval':
                player.isCollidingWithOval = False
            elif isColliding and terrain.type == 'Rectangle':
                if player.rotateAngle != 0:
                    player.index += 0.05
                    player.resetAngle()
                if direction == 'right':
                    player.x = reference - player.width
                elif direction == 'left':
                    player.x = reference
                elif direction == 'up':
                    player.y = terrain.bottomY
                elif direction == 'down':
                    player.y = -(reference - player.height)
                    player.jumping = False
                    player.positions = []
                    player.timer = 0
            elif isColliding and terrain.type == 'outerOval':
                player.isCollidingWithOval = True
                if direction == 'down':
                    player.getPlayerVertices()
                    getY = terrain.getY(player.orientationX)
                    realY = player.getMiddleXFromOrientation(getY)
                    player.y = -(realY - player.height)
                    player.jumping = False
                    player.positions = []
                    player.timer = 0

def implementLeftRightCollisions(object, terrain):
    (isColliding, direction, reference) = object.checkColliding(terrain)
    if isColliding == True and terrain.type == 'Rectangle':
        if direction == 'right':
            object.x = reference - object.width
        elif direction == 'left':
            object.x = reference


def main():
    runApp(width=1000, height=400)

main()