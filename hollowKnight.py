# Citations:

# [1]
# Stack Overflow, How to detect when rotated rectangles are colliding each other
# https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other 
# I did not use any code from this source; I only used the visual pictures to understand the theory for the separating axis algorithm

# [2] 
# CS Academy Class Notes F22 Part 4, side scrolling
# https://www.cs.cmu.edu/~112-f22/notes/notes-animations-part4.html
# In my makePlayerVisible function, I directly used code with modifications from part 7, example sidescroller 2  

# [3]
# The game Hollow Knight by Team Cherry: I directly used their original player and terrain sprites

# [4]
# Background Clouds: https://pbs.twimg.com/media/Dv340GcWsAMt33a?format=jpg&name=4096x4096 

# [5]
# The Spriter's Resource
# Enemy sprite (crawlid): https://www.spriters-resource.com/pc_computer/hollowknight/sheet/131852/   
# Enemy sprite (charger): https://www.spriters-resource.com/pc_computer/hollowknight/sheet/131848

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
    app.spriteCounterEnemy = 0
    app.spriteCounterCharger = 0
    app.stepCounter1 = 0
    app.stepCounter2 = 0
    app.stepCounter3 = 0
    app.stepCounter4 = 0

    app.hazardLimit = 700
    
    
    createPlayerIdleSprites(app)
    createPlayerMovingSprites(app)
    createPlayerDashingSprites(app)
    createPlayerDashingSpritesFinal(app)
    createTerrainSprites(app)
    createBackgroundSprites(app)
    createEnemySprites(app)




player = Player(500, 0, 40, 50)
flat1 = Terrain(450, 480, 521, 50, 'Rectangle', 'Long') # width 521, height 50
flat2 = Terrain(0, 450, 521, 50, 'Rectangle', 'Long')
flat3 = Terrain(900, 450, 521, 50, 'Rectangle', 'Long')
flat4 = Terrain(1400, 450, 521, 50, 'Rectangle', 'Long')
flat5 = Terrain(2400, 430, 90, 90, 'Rectangle', 'Square') # width 90, height 90
flat6 = Terrain(2600, 460, 90, 90, 'Rectangle', 'Square') # width 90, height 90
oval1 = Terrain(1500, 500, 300, 150, 'outerOval', 'Oval')
oval2 = Terrain(1300, 550, 300, 150, 'outerOval', 'Oval')
oval3 = Terrain(1700, 550, 300, 150, 'outerOval', 'Oval')

powerUp1 = powerUp(500, 230, 50, 50, 'Rectangle', 1)
powerUp2 = powerUp(800, 230, 50, 50, 'Rectangle', 2)
powerUp3 = powerUp(1000, 230, 50, 50, 'Rectangle', 3)


crawlid1 = GroundEnemy(700, 100, 50, 30, 50, 'crawlid', None)
crawlid2 = GroundEnemy(800, 100, 50, 30, 50, 'crawlid', None)
charger1 = GroundEnemy(900, 100, 60, 74, 50, 'charger', None)

terrainsList = [flat1, flat2, flat3, flat4, flat5, flat6, oval2, oval3, oval1]
enemyList = [crawlid1, crawlid2, charger1]

powerUpList = [powerUp1, powerUp2, powerUp3]


def redrawAll(app):
    drawBackground(app)
    drawInstructions(app)
    sideScroll(app)
    player.getPlayerVertices()
    drawTerrain(app)
    drawEnemies(app)
    drawTestVectors(app)
    
    drawPlayer(app)
    recordPreviousPositions(app)
    drawAttacks(app)
    drawTestVertices(app)
    drawHealth(app)

def drawInstructions(app):
    opacityFirst = 100-abs((player.x-(400-player.totalScrollX)))*0.3
    if opacityFirst > 100:
        opacityFirst = 100
    elif opacityFirst < 0:
        opacityFirst = 0
    drawLabel('O is jump, J is attack', 400-player.totalScrollX, 250, size=20, fill='blue', opacity = opacityFirst)
    drawLabel('Use AWDS to move and control attack direction', 400-player.totalScrollX, 300, fill = 'blue', size=20, opacity=opacityFirst)

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

def createEnemySprites(app):
    app.enemySprites = []
    spritestrip = Image.open('crawlid.png')
    frame = spritestrip.crop((5, 24, 118, 106))
    width, height = frame.size
    frame = frame.resize((int(width*0.5), int(height*0.5)))
    sprite = CMUImage(frame)
    app.enemySprites.append(sprite)

    frame = spritestrip.crop((5, 24, 118, 106))
    width, height = frame.size
    frame = frame.resize((int(width*0.5), int(height*0.5)))
    frameFlipped = ImageOps.mirror(frame)
    sprite = CMUImage(frameFlipped)
    app.enemySprites.append(sprite)

    frame = spritestrip.crop((5, 376, 118, 465))
    width, height = frame.size
    frame = frame.resize((int(width*0.5), int(height*0.5)))
    sprite = CMUImage(frame)
    app.enemySprites.append(sprite)

    spritestrip = Image.open('charger.png')
    for i in range(7):
        frame = spritestrip.crop((2+i+63*i, 110, 63+63*i, 189))
        sprite = CMUImage(frame)
        app.enemySprites.append(sprite)
    for i in range(7):
        frame = spritestrip.crop((2+i+63*i, 110, 63+63*i, 189))
        frameFlipped = ImageOps.mirror(frame)
        sprite = CMUImage(frameFlipped)
        app.enemySprites.append(sprite)
    
    app.chargingSprites = []
    for i in range(4):
        frame = spritestrip.crop((i/3+2+82*i, 393, 81-i+82*i, 442))
        sprite = CMUImage(frame)
        app.chargingSprites.append(sprite)

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
    app.stepCounter1 += 1
    app.stepCounter2 += 1
    app.stepCounter3 += 1
    app.stepCounter4 += 1
    if app.stepCounter1>= 7:
        app.spriteCounterMove = (1 + app.spriteCounterMove) % len(app.moveSprites)
        app.stepCounter1 = 0 
    if app.stepCounter2>= 5:
        app.spriteCounterDash = (1 + app.spriteCounterDash) % len(app.dashSprites)
        app.stepCounter2 = 0 
    if app.stepCounter3 >= 5:
        app.spriteCounterEnemy = (1 + app.spriteCounterEnemy) % (len(app.enemySprites)-3-7) # 3 for crawlid, 7 for left direction
        app.stepCounter3 = 0
    if app.stepCounter4 >= 5:
        app.spriteCounterCharger = (1 + app.spriteCounterCharger) % (len(app.chargingSprites))
        app.stepCounter4 = 0

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
            if enemy.type == 'crawlid':
                if enemy.direction == -1:
                    # drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle, fill = 'white')
                    sprite = app.enemySprites[0]
                    drawImage(sprite, enemy.x, -enemy.y-5, rotateAngle = enemy.rotateAngle) 
                elif enemy.direction == 1:
                    sprite = app.enemySprites[1]
                    drawImage(sprite, enemy.x, -enemy.y-5, rotateAngle = enemy.rotateAngle)
            if enemy.type == 'charger':
                if enemy.isCharging == True:
                    sprite = app.chargingSprites[app.spriteCounterCharger]
                    drawImage(sprite, enemy.x, -enemy.y, rotateAngle = enemy.rotateAngle)
                elif enemy.isCharging == False:
                    if enemy.direction == -1:
                        sprite = app.enemySprites[app.spriteCounterEnemy+3]
                        # drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle, fill = 'white')
                        drawImage(sprite, enemy.x, -enemy.y, rotateAngle = enemy.rotateAngle)
                    elif enemy.direction == 1:
                        sprite = app.enemySprites[app.spriteCounterEnemy+3+7]
                        # drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle, fill = 'white')
                        drawImage(sprite, enemy.x, -enemy.y, rotateAngle = enemy.rotateAngle)
        else:
            # enemyList.remove(enemy)
            enemy.direction = 0
            if enemy.type == 'crawlid':
                sprite = app.enemySprites[2]
                drawImage(sprite, enemy.x, -enemy.y-5, rotateAngle = enemy.rotateAngle) 
            

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
        if key == 'o' and player.isCollidingWithAnything == False:
            player.doubleJumping = True
        if key == 'j' and player.dashing == False:
            if player.holdingUp == True:
                player.attack(upwards=True) 
                player.holdingUp = False
            elif player.holdingDown == True:
                player.attack(downwards=True) 
                player.holdingDown = False
            else:
                player.attack()
            for enemy in enemyList:
                if player.isAttacking == True and player.checkAttackColliding(enemy) == True and not enemy.isKilled:
                    enemy.takeDamageEnemy(player.playerAttackDamage)
                    player.attackKnockBack(enemy)
        if key == 'i' and player.dashesLeft > 0:
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
        if 'j' in key and player.dashing == False:
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

    for enemy in enemyList:
        if enemy.y >= app.hazardLimit:
            del enemy
        
    if player.freezeEverything == True:
        app.generalFreezeCounter += 1
        if app.generalFreezeCounter - app.initialFreezeCounter > player.freezeDuration:
            app.initialFreezeCounter = app.generalFreezeCounter
            player.freezeEverything = False
            player.stopFreeze = True
       
    
    elif player.freezeEverything == False:

        moveSprites(app)

        for enemy in enemyList:
            if enemy.type == 'charger':
                chargeLeft, chargeRight = False, False
                if enemy.direction == -1:
                    if enemy.x - player.x > 0 and enemy.x - player.x < enemy.sightRange:
                        enemy.charge()
                        chargeLeft = True
                elif enemy.direction == +1:
                    if player.x - enemy.x > 0  and player.x - enemy.x < enemy.sightRange:
                        enemy.charge()
                        chargeRight = True
                if chargeLeft == False and chargeRight == False:
                    enemy.isCharging = False


        app.generalCounter += 1
        for enemy in enemyList:
            (isColliding, direction, reference) = player.isCollidingRect(enemy)
            if isColliding == True and not enemy.isKilled:
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
        if player.doubleJumping:
            player.doubleTimer += 1
            player.doubleJump()
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
                    player.dashesLeft = 1
                    player.y = -(reference - player.height)
                    player.jumping = False
                    player.doubleJumping = False
                    player.doubleTimer = 0
                    player.isPogoing = False
                    player.isPogoingOnGround = False
                    player.isPogoingWhileJumping = False
                    player.timerPogoJumping = 0
                    player.positions = []
                    player.timer = 0
                    player.timerPogo = 0
                    player.isknockBack = True
            elif isColliding and terrain.type == 'outerOval':
                player.dashesLeft = 1
                player.isCollidingWithOval = True
                if direction == 'down':
                    player.getPlayerVertices()
                    getY = terrain.getY(player.orientationX)
                    realY = player.getMiddleXFromOrientation(getY)
                    player.y = -(realY - player.height)
                    player.jumping = False
                    player.doubleJumping = False
                    player.isPogoing = False
                    player.isPogoingOnGround = False
                    player.positions = []
                    player.timer = 0
                    player.timerPogo = 0
                    player.isPogoingWhileJumping = False
                    player.timerPogoJumping = 0
                    player.doubleTimer = 0
                    player.isknockBack = True
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