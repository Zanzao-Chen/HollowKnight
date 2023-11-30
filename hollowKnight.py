# Citations:
# Stack Overflow, How to detect when rotated rectangles are colliding each other
# https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other 
# I did not use any code from this source; I only used the visual pictures to understand the theory for the separating axis algorithm

# Sprites:
# Original Game Assets from the game Hollow Knight by Team Cherry: player and terrain sprites
# Background: https://pbs.twimg.com/media/Dv340GcWsAMt33a?format=jpg&name=4096x4096 


# How to run: use ctrl+b on this file, with the other .py files in the same folder

from cmu_graphics import *
from Player import *
from Terrain import *
from Enemy import *
from powerUp import *

from PIL import Image, ImageOps

def onAppStart(app):
    app.scrollX = 0
    app.scrollMargin = 400

    app.stepsPerSecond = 30
    app.generalAttackCounter = 0
    app.previousAttackTime = 0
    app.initialAttackCounter = 0
    app.generalCounter = 0
    app.generalFreezeCounter = 0
    app.initialFreezeCounter = 0
    app.generalInvincibleCounter = 0
    app.initialInvincibleCounter = 0
    app.generalFallingCounter = 0
    app.initialFallingCounter = 0
    app.generalDashingCounter = 0
    app.initialDashingCounter = 0

    app.spriteCounterDash = 0
    app.spriteCounterMove = 0 
    app.stepCounter = 0

    app.hazardLimit = 700
    
    
    createPlayerIdleSprites(app)
    createPlayerMovingSprites(app)
    createPlayerDashingSprites(app)
    createPlayerDashingSpritesFinal(app)
    createTerrainSprites(app)
    createBackgroundSprites(app)




player = Player(200, 0, 40, 50)
flat1 = Terrain(300, 480, 521, 50, 'Rectangle', 'Long') # width 521, height 50
flat2 = Terrain(800, 480, 521, 50, 'Rectangle', 'Long')
flat3 = Terrain(0, 450, 521, 50, 'Rectangle', 'Long')
flat4 = Terrain(1400, 430, 90, 90, 'Rectangle', 'Square') # width 90, height 90
flat5 = Terrain(1600, 460, 90, 90, 'Rectangle', 'Square') # width 90, height 90
oval1 = Terrain(1500, 450, 300, 150, 'outerOval', 'Oval')



powerUp1 = powerUp(500, 230, 50, 50, 'Rectangle', 1)
powerUp2 = powerUp(800, 230, 50, 50, 'Rectangle', 2)
powerUp3 = powerUp(1000, 230, 50, 50, 'Rectangle', 3)


groundEnemy1 = GroundEnemy(400, 100, 30, 30, 50, None)
groundEnemy2 = GroundEnemy(800, 100, 30, 30, 50, None)
groundEnemyVertical1 = GroundEnemyVertical(720, 100, 30, 30, 500, None)

terrainsList = [flat1, flat2, flat3, flat4, flat5, oval1]
enemyList = [groundEnemy1, groundEnemy2, groundEnemyVertical1]

powerUpList = [powerUp1, powerUp2, powerUp3]


def redrawAll(app):
    drawBackground(app)
    drawLabel('O is jump, J is attack, I is dash', 200, 100)
    drawLabel('Use AWDS to move and control attack direction', 200, 150)
    sideScroll(app)
    groundEnemyVertical1.getPlayerVertices()
    player.getPlayerVertices()
    drawTerrain(app)
    drawEnemies(app)
    drawTestVectors(app)
    drawHealth(app)
    drawPlayer(app)
    recordPreviousPositions(app)
    drawAttacks(app)
    drawTestVertices(app)
    drawLine(200-player.totalScrollX, 0, 200-player.totalScrollX, 1000)

def drawBackground(app):
    sprite = app.backgroundSprites[0]
    drawImage(sprite, 0, 0)

def sideScroll(app):
    if player.moving or player.dashing:
        for enemy in enemyList:
            enemy.x -= app.scrollX
        for terrain in terrainsList:
            terrain.x -= app.scrollX
        player.x -= app.scrollX
        player.totalScrollX += app.scrollX

def makePlayerVisible(app):
    player.getPlayerVertices()
    if (player.middleX < app.scrollX + app.scrollMargin):
        app.scrollX = player.middleX - app.scrollMargin
        return True
    elif (player.middleX > app.scrollX + app.width - app.scrollMargin):
        app.scrollX = player.middleX - (app.width - app.scrollMargin)
        return True
    else:
        app.scrollX = 0
        
    return False

def drawTestVertices(app):
    if player.test == True and player.isAttacking == True:
        for (x, y) in player.cornersAttack:
            drawCircle(x, y, 2)
        for (x, y) in player.cornersEnemy:
            drawCircle(x, y, 2)
        for (x, y) in player.fourPointsAttack1:
            drawCircle(x, y, 2, fill='white')
        for (x, y) in player.fourPointsAttack2:
            drawCircle(x, y, 2, fill='white')
        for (x, y) in player.fourPointsEnemy1:
            drawCircle(x, y, 2, fill = 'white')
        for (x, y) in player.fourPointsEnemy2:
            drawCircle(x, y, 2, fill = 'white')
        for (x, y) in player.twoPointsAttack1:
            drawCircle(x, y, 2, fill='yellow')
        for (x, y) in player.twoPointsAttack2:
            drawCircle(x, y, 2, fill='yellow')
        for (x, y) in player.twoPointsEnemy1:
            drawCircle(x, y, 2, fill = 'blue')
        for (x, y) in player.twoPointsEnemy2:
            drawCircle(x, y, 2, fill = 'blue')

def drawTestVectors(app):
    if player.test == True and player.isAttacking == True:
        for vector in [player.vectorAttackLeftX, 
                    player.vectorAttackRightX, 
                    player.vectorAttackRightY, 
                    player.vectorAttackLeftY,
                    player.vectorEnemyLeftX,
                    player.vectorEnemyRightX,
                    player.vectorEnemyLeftY,
                    player.vectorEnemyRightY]:
            (x, y, x1, y2) = vector.draw()
            drawLine(x, y, x1, y2)
        (x, y, x1, y2) = player.vectorAttackX.draw()
        drawLine(x, y, x1, y2, fill = 'red')
        (x, y, x1, y2) = player.vectorAttackY.draw()
        drawLine(x, y, x1, y2, fill = 'red')
        (x, y, x1, y2) = player.vectorEnemyX.draw()
        drawLine(x, y, x1, y2, fill = 'red')
        (x, y, x1, y2) = player.vectorEnemyY.draw()
        drawLine(x, y, x1, y2, fill = 'red')

def drawHealth(app):
    for i in range(len(player.healthList)):
        if player.healthList[i] == True:
            drawCircle(player.healthX+player.healthXInterval*i, player.healthY, player.healthRadius, fill=player.yesHealthColor)
        else:
            drawCircle(player.healthX+player.healthXInterval*i, player.healthY, player.healthRadius, fill=player.noHealthColor)

def drawPlayer(app):
    if player.dashing == True:
        player.dashingPositions.append((player.x, player.y, player.rotateAngle))
    elif player.dashing == False:
        player.dashingPositions = []
    # if player.dashing == False:
    #     if player.direction == 'left':
    #         sprite = app.idleSprites[1]
    #     elif player.direction == 'right':
    #         sprite = app.idleSprites[0]
    for (x, y, angle) in player.dashingPositions:
        if player.direction == 'left':
            sprite = app.dashSpritesFlipped[app.spriteCounterDash]
            drawImage(sprite, x-player.spriteX, -y+18, rotateAngle = angle, align = 'left', opacity = 20)
        elif player.direction == 'right':
            sprite = app.dashSprites[app.spriteCounterDash]
            drawImage(sprite, x-player.spriteX, -y+18, rotateAngle = angle, align = 'left', opacity = 20)
    # drawRect(player.x, -player.y, player.width, player.height, fill = 'black', rotateAngle = player.rotateAngle)
    # drawCircle(player.orientationX, player.orientationY, 3, fill='red')
    if player.dashing == True:
        if player.direction == 'right':
            sprite = app.dashSpritesFinal[1]
        elif player.direction == 'left':
            sprite = app.dashSpritesFinal[0]
        drawImage(sprite, player.x-player.spriteX, -player.y+18, align = 'left')
    if player.moving == False and player.dashing == False:
        if player.direction == 'left':
            sprite = app.idleSprites[1]
            drawImage(sprite, player.x-player.spriteX, -player.y+18, rotateAngle = player.rotateAngle, align = 'left')
        elif player.direction == 'right':
            sprite = app.idleSprites[0]
            drawImage(sprite, player.x-player.spriteX, -player.y+18, rotateAngle = player.rotateAngle, align = 'left')
    elif player.moving == True and player.dashing == False:
        if player.direction == 'right':
            sprite = app.moveSprites[app.spriteCounterMove]
            drawImage(sprite, player.x-player.spriteX, -player.y+18, rotateAngle = player.rotateAngle, align = 'left')
        elif player.direction == 'left':
            sprite = app.moveSpritesFlipped[app.spriteCounterMove]
            drawImage(sprite, player.x-player.spriteX, -player.y+18, rotateAngle = player.rotateAngle, align = 'left')


def createBackgroundSprites(app):
    spritestrip = Image.open('background.png')
    app.backgroundSprites = []
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width*0.8), int(height*0.8)))
    sprite = CMUImage(frame)
    app.backgroundSprites.append(sprite)
    

def createPlayerIdleSprites(app):
    app.idleSprites = []
    spritestrip = Image.open('playerSprites.png')
    i = 0
    frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
    app.spriteWidth, app.spriteHeight = frame.size
    sprite = CMUImage(frame)
    app.idleSprites.append(sprite)

    spritestrip = Image.open('playerSprites.png')
    i = 0
    frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
    frameFlipped = ImageOps.mirror(frame)
    sprite = CMUImage(frameFlipped)
    app.idleSprites.append(sprite)

def createPlayerMovingSprites(app):
    spritestrip = Image.open('playerSprites.png')
    app.moveSprites = []
    app.moveSpritesFlipped = []
    for i in range(1, 9):
        frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
        sprite = CMUImage(frame)
        app.moveSprites.append(sprite)
    for i in range(1, 9):
        frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
        frameFlipped = ImageOps.mirror(frame)
        sprite = CMUImage(frameFlipped)
        app.moveSpritesFlipped.append(sprite)

def createPlayerDashingSprites(app):
    spritestrip = Image.open('dashSprites.png')
    app.dashSprites = []
    for i in range(5):
        frame = spritestrip.crop((0+130*i, 520, 130+130*i, 640))
        frame = frame.resize((app.spriteWidth, app.spriteHeight))
        sprite = CMUImage(frame)
        app.dashSprites.append(sprite)
    app.dashSpritesFlipped = []
    for i in range(5):
        frame = spritestrip.crop((0+130*i, 520, 130+130*i, 640))
        frame = frame.resize((app.spriteWidth, app.spriteHeight))
        frameFlipped = ImageOps.mirror(frame)
        sprite = CMUImage(frameFlipped)
        app.dashSpritesFlipped.append(sprite)
def createPlayerDashingSpritesFinal(app):
    app.dashSpritesFinal = []

    spritestrip = Image.open('Knight.png')
    frame = spritestrip.crop((2624, 1550, 2624+164, 1664))
    width, height = frame.size
    factor = app.spriteHeight/height
    frame = frame.resize((int(width*factor), int(height*factor)))
    sprite = CMUImage(frame)
    app.dashSpritesFinal.append(sprite)

    frame = ImageOps.mirror(frame)
    sprite = CMUImage(frame)
    app.dashSpritesFinal.append(sprite)

def drawTerrain(app):
    for terrain in terrainsList:
        if terrain.type == 'Rectangle':
            if terrain.subtype == 'Long':
                sprite = app.terrainSprites[0]
                # drawRect(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')
                drawImage(sprite, terrain.x, terrain.y-2, align = 'top-left')
            elif terrain.subtype == 'Square':
                sprite = app.terrainSprites[1]
                # drawRect(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')
                drawImage(sprite, terrain.x, terrain.y-2, align = 'top-left')
        elif terrain.type == 'outerOval':
            sprite = app.terrainSprites[2]
            # drawOval(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')
            drawImage(sprite, terrain.x+20, terrain.y-2, align = 'center')

def createTerrainSprites(app):
    app.terrainSprites = []
    spritestrip = Image.open('ground1.png')
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width/3), int(height/3)))
    sprite = CMUImage(frame)
    app.terrainSprites.append(sprite)

    spritestrip = Image.open('squareGround.png')
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width/5), int(height/5)))
    sprite = CMUImage(frame)
    app.terrainSprites.append(sprite)

    spritestrip = Image.open('ovalGround2.png')
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width/6), int(height/6)))
    sprite = CMUImage(frame)
    app.terrainSprites.append(sprite)

def moveSprites(app):
    app.stepCounter += 1
    if app.stepCounter>= 5:
        app.spriteCounterMove = (1 + app.spriteCounterMove) % len(app.moveSprites)
        app.stepCounter = 0 
    if app.stepCounter>= 5:
        app.spriteCounterDash = (1 + app.spriteCounterDash) % len(app.dashSprites)
        app.stepCounter = 0 

def recordPreviousPositions(app):
    player.previousPositions.append((player.x, -player.y))
    if len(player.previousPositions) > 5:
        player.previousPositions = player.previousPositions[2:]
    for enemy in enemyList:
        enemy.previousPositions.append((enemy.x, -enemy.y))
        if len(enemy.previousPositions) > 5:
            enemy.previousPositions = enemy.previousPositions[2:]


def drawAttacks(app):
    if player.isAttacking == True or player.looksAttacking == True:
        drawRect(player.attackX, -player.attackY, player.attackWidth, player.attackHeight, fill='red', rotateAngle=player.rotateAngle)
        player.isAttacking = False

def drawEnemies(app):
    for enemy in enemyList:
        if enemy.isKilled == False:
            drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle, fill = 'white')
        else:
            enemyList.remove(enemy)

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
        if key == 'o' and (player.jumping == False and player.isPogoing == False and player.dashing == False):
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
            for enemy in enemyList:
                if player.isAttacking == True and player.checkAttackColliding(enemy) == True:
                    enemy.takeDamageEnemy(player.playerAttackDamage)
                    player.attackKnockBack(enemy)
        if key == 'i':
            player.dashing = True
        if key == 'p':
            app.stepsPerSecond = 0.01
        if key == 'space':
            player.test = True

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
        else:
            player.holdingUp = False
        if 's' in key:
            player.holdingDown = True
        else: 
            player.holdingDown = False
        if 'j' in key:
            if 'w' in key:
                player.attack(upwards=True) 
            elif 's' in key:
                player.attack(downwards=True)
            else:
                player.attack()
            for enemy in enemyList:
                if player.isAttacking == True and player.checkAttackColliding(enemy) == True:
                    enemy.takeDamageEnemy(player.playerAttackDamage)
                    player.attackKnockBack(enemy)

def onKeyRelease(app, key):
    if key == 'd' or key == 'a':
        player.moving = False
    if key == 'w':
        player.holdingUp = False
    elif key == 's':
        player.holdingDown = False

def onStep(app):
    makePlayerVisible(app)
    if -player.y >= app.hazardLimit-50:
        player.updateHealth(-1)
    if -player.y >= app.hazardLimit:
        app.respawnPoints = [(200-player.totalScrollX, -200),
                             (1200-player.totalScrollX, -200),
                             (1650-player.totalScrollX, -200)]
        respawnDistance = []
        for (x, y) in app.respawnPoints:
            respawnDistance.append(distance(x, y, player.x, player.y))
            
        minimumDistance = min(respawnDistance)
        index = respawnDistance.index(minimumDistance)
        player.x, player.y = app.respawnPoints[index]
        
    if player.freezeEverything == True:
        app.generalFreezeCounter += 1
        if app.generalFreezeCounter - app.initialFreezeCounter > player.freezeDuration:
            app.initialFreezeCounter = app.generalFreezeCounter
            player.freezeEverything = False
            player.stopFreeze = True
       
    
    elif player.freezeEverything == False:

        moveSprites(app)

        app.generalCounter += 1
        for enemy in enemyList:
            (isColliding, direction, reference) = player.isCollidingRect(enemy)
            if isColliding == True:
                player.updateHealth(-1)
                player.enemyCollisionDirection = direction
                player.collidedEnemy = enemy
                

        if player.stopFreeze == True:
            player.knockBack(player.enemyCollisionDirection)
            player.stopFreeze = False


        if player.falling == False:
            app.generalFallingCounter += 1
            if app.generalFallingCounter - app.initialFallingCounter > player.startFallDuration:
                app.initialFallingCounter = app.generalFallingCounter
                player.falling = True

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
        
        if player.dashing == True:
            app.generalDashingCounter+= 1
            if app.generalDashingCounter - app.initialDashingCounter > player.dashDuration:
                app.initialDashingCounter = app.generalDashingCounter
                player.dashing = False

        if player.dashing == True:
            player.dash()

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
        for enemy in enemyList:
            for terrain in terrainsList:
                implementLeftRightCollisions(enemy, terrain)

        if player.falling:
            player.timer += 1
            player.timerPogo += 1
            player.fall()
        if player.jumping:
            player.timer += 1
            player.jump()
        if player.isPogoing:
            player.timerPogo += 1
            player.pogoJump()
        if player.isPogoingWhileJumping:
            player.timerPogoJumping += 1
            player.pogoJumpWhileJumping()
        player.terrainCollisionsDict = dict()
        
        for terrain in terrainsList:
            isColliding = False
            (isColliding, direction, reference) = player.checkColliding(terrain)
            player.terrainCollisionsDict[terrain] = isColliding
            if not isColliding and terrain.type == 'outerOval':
                player.isCollidingWithOval = False
            elif isColliding and terrain.type == 'Rectangle':
                player.isCollidingWithRect = True
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
                    player.isPogoing = False
                    player.isPogoingOnGround = False
                    player.isPogoingWhileJumping = False
                    player.timerPogoJumping = 0
                    player.positions = []
                    player.timer = 0
                    player.timerPogo = 0
            elif isColliding and terrain.type == 'outerOval':
                player.isCollidingWithOval = True
                if direction == 'down':
                    player.getPlayerVertices()
                    getY = terrain.getY(player.orientationX)
                    realY = player.getMiddleXFromOrientation(getY)
                    player.y = -(realY - player.height)
                    player.jumping = False
                    player.isPogoing = False
                    player.isPogoingOnGround = False
                    player.positions = []
                    player.timer = 0
                    player.timerPogo = 0
                    player.isPogoingWhileJumping = False
                    player.timerPogoJumping = 0
    player.isCollidingWithAnything = False
    
    for key in player.terrainCollisionsDict:
        if player.terrainCollisionsDict[key] == True:
            player.isCollidingWithAnything = True



def implementLeftRightCollisions(object, terrain):
    (isColliding, direction, reference) = object.checkColliding(terrain)
    if isColliding == True and terrain.type == 'Rectangle':
        if direction == 'right':
            object.x = reference - object.width
        elif direction == 'left':
            object.x = reference
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


def main():
    runApp(width=1200, height=800)

main()