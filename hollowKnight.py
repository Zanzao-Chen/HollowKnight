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
# Lecture demos 11/21 on sprite strips
# https://piazza.com/class/lkq6ivek5cg1bc/post/2231
# I created and animated all the sprites in my game using the code on sprite strips in the demos
# Things that I did myself: cropping sprites, using mirror, flip, and size methods in PIL, which I learned through the PIL official documentation

# [3]
# Sprites from the game Hollow Knight by Team Cherry, directly taken from Steam game files
# Includes: player sprites, terrain sprites, health bar sprites, upgrade area and instructions

# [4]
# Background Clouds from Twitter: https://pbs.twimg.com/media/Dv340GcWsAMt33a?format=jpg&name=4096x4096 

# [5]
# The Spriter's Resource
# Enemy sprite (crawlid): https://www.spriters-resource.com/pc_computer/hollowknight/sheet/131852/   
# Enemy sprite (charger): https://www.spriters-resource.com/pc_computer/hollowknight/sheet/131848
# Enemy sprite (flying): https://www.spriters-resource.com/pc_computer/hollowknight/sheet/133898/
# Enemy sprite (ghost and fireball): https://www.spriters-resource.com/pc_computer/hollowknight/sheet/133898/ 
# Attack sprites (fire): https://www.spriters-resource.com/pc_computer/rpgmakervxace/sheet/100134 
# How to run: use ctrl+b on this file, with the other .py files in the same folder

from random import *
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
    app.generalFireballCounter = 0
    app.initialFireballCounter = 0

    app.spriteCounterDash = 0
    app.spriteCounterMove = 0 
    app.spriteCounterEnemy = 0
    app.spriteCounterCharger = 0
    app.spriteCounterFly = 0
    app.spriteCounterFireball = 0
    
    app.stepCounter1 = 0
    app.stepCounter2 = 0
    app.stepCounter3 = 0
    app.stepCounter4 = 0
    app.stepCounter5 = 0
    app.stepCounter6 = 0
    app.stepCounter7 = 0

    
    app.hazardLimit = 700

    app.upgradePositions = [(1700, 300), (5000, 300)]
    app.upgradeStates = [True, True]
    app.powerUpRadius = 100
    app.gameStarted = False
    app.arrowsUp = True
    app.displayTutorial = False
    
    createPlayerIdleSprites(app)
    createPlayerMovingSprites(app)
    createPlayerDashingSprites(app)
    createPlayerDashingSpritesFinal(app)
    createTerrainSprites(app)
    createBackgroundSprites(app)
    createEnemySprites(app)
    createAttackSprites(app)
    createHealthSprites(app)
    createInstructionSprites(app)
    createUpgradeSprites(app)
    createMainMenuSprites(app)

player = Player(350, 0, 40, 50)
flat1 = Terrain(450, 480, 521, 50, 'Rectangle', 'Long') # width 521, height 50
flat2 = Terrain(0, 450, 521, 50, 'Rectangle', 'Long')
flat3 = Terrain(900, 450, 521, 50, 'Rectangle', 'Long')
flat4 = Terrain(1400, 450, 521, 50, 'Rectangle', 'Long')
flat4 = Terrain(1500, 450, 521, 50, 'Rectangle', 'Long')
flat5 = Terrain(2100, 430, 90, 90, 'Rectangle', 'Square') # width 90, height 90
flat6 = Terrain(2300, 460, 90, 90, 'Rectangle', 'Square') 
flat7 = Terrain(2500, 450, 90, 90, 'Rectangle', 'Square') 
flat8 = Terrain(2700, 420, 90, 90, 'Rectangle', 'Square') 
flat9 = Terrain(2900, 450, 521, 50, 'Rectangle', 'Long')
flat10 = Terrain(3300, 450, 521, 50, 'Rectangle', 'Long')
flat11 = Terrain(3700, 450, 521, 50, 'Rectangle', 'Long')
flat12 = Terrain(2900, 370, 90, 90, 'Rectangle', 'Square') 
flat13 = Terrain(4000, 370, 90, 90, 'Rectangle', 'Square')
flat14 = Terrain(4000, 450, 521, 50, 'Rectangle', 'Long')
flat15 = Terrain(4500, 450, 521, 50, 'Rectangle', 'Long')
flat16 = Terrain(5100, 430, 90, 90, 'Rectangle', 'Square') 
flat17 = Terrain(5300, 460, 90, 90, 'Rectangle', 'Square') 
flat18 = Terrain(5500, 450, 90, 90, 'Rectangle', 'Square') 
flat19 = Terrain(5700, 420, 90, 90, 'Rectangle', 'Square') 

oval1 = Terrain(1500, 500, 300, 150, 'outerOval', 'Oval')
oval2 = Terrain(1300, 550, 300, 150, 'outerOval', 'Oval')
oval3 = Terrain(1700, 550, 300, 150, 'outerOval', 'Oval')


crawlid1 = GroundEnemy(700, -300, 50, 30, 50, 'crawlid', None)
crawlid2 = GroundEnemy(800, -300, 50, 30, 50, 'crawlid', None)
charger1 = GroundEnemy(3500, 100, 60, 74, 50, 'charger', None)
fly1 = FlyEnemy(1000, -200, 50, 60, 50, 'fly', None)
fly2 = FlyEnemy(5500, -200, 50, 60, 50, 'fly', None)
fly3 = FlyEnemy(5700, -200, 50, 60, 50, 'fly', None)

ghost1 = FlyEnemy(4000, 200, 100, 100, 50, 'ghost', None)


terrainsList = [flat1, flat2, flat3, flat4, flat5, flat6, flat7, flat8, flat9, flat10, 
                flat11, flat12, flat13, flat14, flat15, flat16, flat17, flat18, flat19,
                oval2, oval3, oval1]
enemyList = [crawlid1, crawlid2, charger1, fly1, fly2, fly3, ghost1]


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
    drawUpgradeAreas(app)
    if app.gameStarted == False:
        drawMainMenu(app)

def drawMainMenu(app):
    sprite = app.mainMenuSprite[0]
    drawImage(sprite, 0, 0)
    if app.arrowsUp == True:
        drawPolygon(475, 380, 475, 400, 500, 390, fill = 'white')
        drawPolygon(750, 380, 750, 400, 725, 390, fill = 'white')
    if app.arrowsUp == False:
        drawPolygon(485, 420, 485, 440, 510, 430, fill = 'white')
        drawPolygon(740, 420, 740, 440, 715, 430, fill = 'white')
    if app.displayTutorial == True:
        sprite = app.mainMenuSprite[1]
        drawImage(sprite, 0, 0)
def drawInstructions(app):
    for i in range(len(app.upgradePositions)):
        x, y = app.upgradePositions[i]
        if app.upgradeStates[i] == False:
            drawStaticInstructions(x, y, app.instructionSprites[i+1])
    drawStaticInstructions(350-player.totalScrollX, 300, app.instructionSprites[0])

def drawStaticInstructions(x, y, sprite):
    opacityFirst = 100-abs((player.x-(x)))*0.2
    if opacityFirst > 100:
        opacityFirst = 100
    elif opacityFirst < 0:
        opacityFirst = 0
    drawImage(sprite, x, y, opacity = opacityFirst, align='center')


def drawBackground(app):
    sprite = app.backgroundSprites[0]
    drawImage(sprite, player.backgroundX, 0)

def sideScroll(app):
    if player.moving or player.dashing:
        for enemy in enemyList:
            enemy.x -= app.scrollX
        for terrain in terrainsList:
            terrain.x -= app.scrollX
        player.x -= app.scrollX
        player.totalScrollX += app.scrollX
        if player.totalScrollX > 0:
            player.backgroundX -= app.scrollX/5
        for i in range(len(app.upgradePositions)):
            x, y = app.upgradePositions[i]
            x -= app.scrollX
            app.upgradePositions[i] = x, y
        

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
            sprite = app.healthSprites[0]
            drawImage(sprite, player.healthX+player.healthXInterval*i, player.healthY)
            # drawCircle(player.healthX+player.healthXInterval*i, player.healthY, player.healthRadius, fill=player.yesHealthColor)
        else:
            sprite = app.healthSprites[1]
            drawImage(sprite, player.healthX+player.healthXInterval*i, player.healthY)
    
    
    
    if player.resource > 0:
        if player.resource >= 50:
            color1 = 'white'
        else:
            color1 = 'grey'
        drawRect(100, 170, int(159*(player.resource/50)), 20, fill=color1)
    if player.resource > 50:
        if player.resource == 100:
            color2 = 'white'
        else:
            color2 = 'grey'
        drawRect(259, 170, int(159*((player.resource-50)/50)), 20, fill=color2)
    drawRect(100, 170, 159, 20, fill=None, border='black')
    drawRect(259, 170, 159, 20, fill=None, border='black')


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

def createMainMenuSprites(app):
    spritestrip = Image.open('Images\\mainMenu.png')
    app.mainMenuSprite = []
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width*0.75), int(height*0.75)))
    sprite = CMUImage(frame)
    app.mainMenuSprite.append(sprite)

    spritestrip = Image.open('Images\\Tutorial.png')
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width*0.7), int(height*0.7)))
    sprite = CMUImage(frame)
    app.mainMenuSprite.append(sprite)


def drawUpgradeAreas(app):
    sprite =  app.upgradeSprites[0]
    for i in range(len(app.upgradePositions)):
        x, y = app.upgradePositions[i]
        if app.upgradeStates[i] == True:
            drawImage(sprite, x, y, align = 'center')
            # drawCircle(x, y, app.powerUpRadius, fill = 'red')

def createUpgradeSprites(app):
    spritestrip = Image.open('Images\\powerup.png')
    app.upgradeSprites = []
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width*0.8), int(height*0.8)))
    sprite = CMUImage(frame)
    app.upgradeSprites.append(sprite)

def createBackgroundSprites(app):
    spritestrip = Image.open('Images\\background.png')
    app.backgroundSprites = []
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width*0.8), int(height*0.8)))
    sprite = CMUImage(frame)
    app.backgroundSprites.append(sprite)

def createEnemySprites(app):
    app.enemySprites = []
    spritestrip = Image.open('Images\crawlid.png')
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

    spritestrip = Image.open('Images\charger.png')
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
    
    for i in range(4):
        frame = spritestrip.crop((i/3+2+82*i, 393, 81-i+82*i, 442))
        frameFlipped = ImageOps.mirror(frame)
        sprite = CMUImage(frameFlipped)
        app.chargingSprites.append(sprite)
    
    app.flySprites = []
    spritestrip = Image.open('Images\\fly.png')
    for i in range(5):
        frame = spritestrip.crop((5+168*i, 8, 168+168*i-5, 197))
        width, height = frame.size
        frame = frame.resize((int(width/3), int(height/3)))
        sprite = CMUImage(frame)
        app.flySprites.append(sprite)

    app.ghostSprites = []
    frame = Image.open('Images\ghost.png')
    width, height = frame.size
    frame = frame.resize((int(width/2), int(height/2)))
    sprite = CMUImage(frame)
    app.ghostSprites.append(sprite)

    spritestrip = Image.open('Images\enemyFireball.png')
    app.fireballSprites = [ ]
    for i in range(4):
        frame = spritestrip.crop((10+i+136*i, 6, 136+130*i, 125))
        width, height = frame.size
        frame = frame.resize((int(width/2), int(height/2)))     
        sprite = CMUImage(frame)
        app.fireballSprites.append(sprite)

def createAttackSprites(app):
    app.attackSprites = []
    spritestrip = Image.open('Images\playerAttacksLeftRight.png')
    for i in range(4):
        frame = spritestrip.crop((-300, 360*i, 1600, 360+360*i))
        width, height = frame.size
        frame = frame.resize((int(width/3), int(height/3)))
        sprite = CMUImage(frame)
        app.attackSprites.append(sprite)
    app.attackSprites.append(sprite)

    for i in range(4):
        frame = spritestrip.crop((-300, 360*i, 1600, 360+360*i))
        width, height = frame.size
        frame = frame.resize((int(width/3), int(height/3)))
        frameFlipped = ImageOps.mirror(frame)
        sprite = CMUImage(frameFlipped)
        app.attackSprites.append(sprite)
    app.attackSprites.append(sprite)

    app.attackUpDownSprites = []
    frame = Image.open('Images\playerAttackDownwards.png')
    app.sprites = [ ]
    width, height = frame.size
    frame = frame.resize((int(width/5), int(height/5)))
    sprite = CMUImage(frame)
    app.attackUpDownSprites.append(sprite)
    frameFlipped = ImageOps.flip(frame)
    sprite = CMUImage(frameFlipped)
    app.attackUpDownSprites.append(sprite)

def createPlayerIdleSprites(app):
    app.idleSprites = []
    spritestrip = Image.open('Images\playerSprites.png')
    i = 0
    frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
    app.spriteWidth, app.spriteHeight = frame.size
    sprite = CMUImage(frame)
    app.idleSprites.append(sprite)

    spritestrip = Image.open('Images\playerSprites.png')
    i = 0
    frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
    frameFlipped = ImageOps.mirror(frame)
    sprite = CMUImage(frameFlipped)
    app.idleSprites.append(sprite)

def createPlayerMovingSprites(app):
    spritestrip = Image.open('Images\playerSprites.png')
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
    spritestrip = Image.open('Images\dashSprites.png')
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

    spritestrip = Image.open('Images\Knight.png')
    frame = spritestrip.crop((2624, 1550, 2624+164, 1664))
    width, height = frame.size
    factor = app.spriteHeight/height
    frame = frame.resize((int(width*factor), int(height*factor)))
    sprite = CMUImage(frame)
    app.dashSpritesFinal.append(sprite)

    frame = ImageOps.mirror(frame)
    sprite = CMUImage(frame)
    app.dashSpritesFinal.append(sprite)

def createHealthSprites(app):
    app.healthSprites = []
    frame = Image.open('Images\health1.png')
    width, height = frame.size
    factor = 0.20
    frame = frame.resize((int(width*factor), int(height*factor)))
    sprite = CMUImage(frame)
    app.healthSprites.append(sprite)

    frame = Image.open('Images\health2.png')
    width, height = frame.size
    factor = 0.20
    frame = frame.resize((int(width*factor), int(height*factor)))
    sprite = CMUImage(frame)
    app.healthSprites.append(sprite)

def createInstructionSprites(app):
    app.instructionSprites = []
    frame = Image.open('Images\Instructions1.png')
    width, height = frame.size
    factor = 0.10
    frame = frame.resize((int(width*factor), int(height*factor)))
    sprite = CMUImage(frame)
    app.instructionSprites.append(sprite)

    frame = Image.open('Images\Instructions2.png')
    width, height = frame.size
    factor = 0.10
    frame = frame.resize((int(width*factor), int(height*factor)))
    sprite = CMUImage(frame)
    app.instructionSprites.append(sprite)

    frame = Image.open('Images\Instructions3.png')
    width, height = frame.size
    factor = 0.10
    frame = frame.resize((int(width*factor), int(height*factor)))
    sprite = CMUImage(frame)
    app.instructionSprites.append(sprite)

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
    spritestrip = Image.open('Images\ground1.png')
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width/3), int(height/3)))
    sprite = CMUImage(frame)
    app.terrainSprites.append(sprite)

    spritestrip = Image.open('Images\squareGround.png')
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width/5), int(height/5)))
    sprite = CMUImage(frame)
    app.terrainSprites.append(sprite)

    spritestrip = Image.open('Images\ovalGround2.png')
    width, height = spritestrip.size
    frame = spritestrip.resize((int(width/6), int(height/6)))
    sprite = CMUImage(frame)
    app.terrainSprites.append(sprite)

def moveSprites(app):
    app.stepCounter1 += 1
    app.stepCounter2 += 1
    app.stepCounter3 += 1
    app.stepCounter4 += 1
    app.stepCounter5 += 1
    app.stepCounter6 += 1
    app.stepCounter7 += 1
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
        app.spriteCounterCharger = (1 + app.spriteCounterCharger) % (len(app.chargingSprites)-4)
        app.stepCounter4 = 0
    if app.stepCounter5 >= 5:
        app.spriteCounterFly = (1 + app.spriteCounterFly) % (len(app.flySprites))
        app.stepCounter5 = 0
    if app.stepCounter7 >= 5:
        app.spriteCounterFireball = (1 + app.spriteCounterFireball) % (len( app.fireballSprites))
        app.stepCounter7 = 0 
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
        if player.attackDirection == 'right':
            if player.spriteCounterAttack < 4:
                # drawRect(player.attackX, -player.attackY, player.attackWidth, player.attackHeight, fill='red', rotateAngle=player.rotateAngle)
                sprite = app.attackSprites[player.spriteCounterAttack]
                drawImage(sprite, player.attackX-150, -player.attackY,rotateAngle=player.rotateAngle)
                player.spriteCounterAttack += 1
                player.isAttacking = False
            else:
                player.spriteCounterAttack = 0
                sprite = app.attackSprites[4]
                drawImage(sprite, player.attackX-150, -player.attackY,rotateAngle=player.rotateAngle)
                player.isAttacking = False
            
        elif player.attackDirection == 'left':
            if player.spriteCounterAttack < 4:
                sprite = app.attackSprites[player.spriteCounterAttack+5]
                drawImage(sprite, player.attackX-150, -player.attackY,rotateAngle=player.rotateAngle)
                player.spriteCounterAttack += 1
                player.isAttacking = False
            else:
                player.spriteCounterAttack = 0
                sprite = app.attackSprites[4+5]
                drawImage(sprite, player.attackX-150, -player.attackY,rotateAngle=player.rotateAngle)
                player.isAttacking = False
        elif player.attackDirection == 'up':
            sprite = app.attackUpDownSprites[1]
            drawImage(sprite, player.attackX, -player.attackY,rotateAngle=player.rotateAngle)
            player.isAttacking = False
        elif player.attackDirection == 'down':
            sprite = app.attackUpDownSprites[0]
            # drawRect(player.attackX, -player.attackY, player.attackWidth, player.attackHeight, fill='red', rotateAngle=player.rotateAngle)
            drawImage(sprite, player.attackX, -player.attackY,rotateAngle=player.rotateAngle)
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
            elif enemy.type == 'charger':
                if enemy.isCharging == True:
                    if enemy.direction == -1:
                        sprite = app.chargingSprites[app.spriteCounterCharger]
                        drawImage(sprite, enemy.x, -enemy.y+30, rotateAngle = enemy.rotateAngle)
                    elif enemy.direction == 1:
                        sprite = app.chargingSprites[app.spriteCounterCharger+4]
                        drawImage(sprite, enemy.x, -enemy.y+30, rotateAngle = enemy.rotateAngle)
                elif enemy.isCharging == False:
                    if enemy.direction == -1:
                        sprite = app.enemySprites[app.spriteCounterEnemy+3]
                        # drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle, fill = 'white')
                        drawImage(sprite, enemy.x, -enemy.y, rotateAngle = enemy.rotateAngle)
                    elif enemy.direction == 1:
                        sprite = app.enemySprites[app.spriteCounterEnemy+3+7]
                        # drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle, fill = 'white')
                        drawImage(sprite, enemy.x, -enemy.y, rotateAngle = enemy.rotateAngle)
            elif enemy.type == 'fly':
                sprite = app.flySprites[app.spriteCounterFly]
                # drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, fill='red')
                drawImage(sprite, enemy.x, -enemy.y)
            elif enemy.type == 'ghost':
                if enemy.startShootFireball == True:
                    drawCircle(enemy.fireballX, -enemy.fireballY, enemy.fireballRadius, fill='red')
                    drawLine(enemy.fireballX, -enemy.fireballY, enemy.finalFireballX, -enemy.finalFireballY)
                    sprite = app.fireballSprites[app.spriteCounterFireball]
                    drawImage(sprite, enemy.fireballX, -enemy.fireballY, align = 'center')
                sprite = app.ghostSprites[0]
                drawImage(sprite, enemy.x, -enemy.y)
        else:
            # enemyList.remove(enemy)
            enemy.direction = 0
            if enemy.type == 'crawlid':
                sprite = app.enemySprites[2]
                drawImage(sprite, enemy.x, -enemy.y-5, rotateAngle = enemy.rotateAngle) 
            

def onKeyPress(app, key):
    if app.displayTutorial == True and key == 'p':
        app.displayTutorial = False
        return
    if app.displayTutorial == False:
        if key == 'w':
            app.arrowsUp = True
        elif key == 's':
            app.arrowsUp = False
        if key == 'p' and app.arrowsUp == True:
            app.gameStarted = True
        if key == 'p' and app.arrowsUp == False:
            app.displayTutorial = True
    if app.gameStarted == True:
        if player.freezeEverything == False:
            if key == 'space':
                player.level = 3
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
                        if player.resource < 75:
                            player.resource += player.resourceGain
                        elif player.resource >= 75:
                            player.resource = 100
                        if enemy.type == 'charger':
                            attackDirection = None
                            if player.attackDirection == 'left':
                                attackDirection = -1
                            elif player.attackDirection == 'right':
                                attackDirection = +1
                            if attackDirection == enemy.direction:
                                enemy.direction *= -1
            if key == 'i' and player.dashesLeft > 0 and player.level > 0:
                player.dashing = True
            

            if key == 'k' and player.resource >= player.resourceCost:
                player.updateHealth(+1)
                player.resource -= player.resourceCost
            # if key == 'p':
            #     app.stepsPerSecond = 0.01
            # if key == 'space':
            #     player.test = True

def onKeyHold(app, key):
    if app.gameStarted == True:
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
    if app.gameStarted == True:
        if key == 'd' or key == 'a':
            player.moving = False
        if key == 'w':
            player.holdingUp = False
        elif key == 's':
            player.holdingDown = False

def onStep(app):
    if app.gameStarted:
        makePlayerVisible(app)
        if -player.y >= app.hazardLimit:
            app.respawnPoints = []
            player.updateHealth(-1)
            for terrain in terrainsList:
                if terrain.type == 'Rectangle':
                    terrain.getTerrainVertices()
                    x, y = (terrain.leftX + terrain.rightX)/2, terrain.topY
                    app.respawnPoints.append((x, -y+500))
            respawnDistance = []
            for (x, y) in app.respawnPoints:
                respawnDistance.append(distance(x, y, player.x, player.y))
                
            minimumDistance = min(respawnDistance)
            index = respawnDistance.index(minimumDistance)
            player.x, player.y = app.respawnPoints[index]

        for enemy in enemyList:
            if enemy.y >= app.hazardLimit:
                del enemy
        for enemy in enemyList:
            if enemy.type == 'ghost' and enemy.isAttacking:
                if distance(enemy.fireballX, enemy.fireballY, player.x, player.y) <= enemy.fireballRadius + 30:
                    player.updateHealth(-1)
            
        if player.freezeEverything == True:
            app.generalFreezeCounter += 1
            
            if app.generalFreezeCounter - app.initialFreezeCounter > player.freezeDuration:
                app.initialFreezeCounter = app.generalFreezeCounter
                player.freezeEverything = False
                player.stopFreeze = True
        
        
        elif player.freezeEverything == False:

            moveSprites(app)

            
            for i in range(len(app.upgradePositions)):
                if app.upgradeStates[i] == True:
                    x, y = app.upgradePositions[i]
                    if distance(player.x, -player.y, x, y) <= app.powerUpRadius+40: # compensates for player width
                        app.upgradeStates[i] = False
                        player.level += 1

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
            
            if enemy.startShootFireball == True:
                app.generalFireballCounter += 1
                if app.generalFireballCounter - app.initialFireballCounter > 90:
                    app.initialFireballCounter = app.generalFireballCounter
                    enemy.startShootFireball = False

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
                if enemy.type != 'fly' and enemy.type != 'ghost':
                    enemy.move()
                elif enemy.type == 'fly':
                    if distance(enemy.x, enemy.y, player.x, player.y) <= enemy.sightRadius:
                        enemy.move(player)
                    else:
                        x = enemy.initialX - player.totalScrollX
                        y = enemy.initialY
                        enemy.moveRandom(x, y)
                elif enemy.type == 'ghost':
                    if abs(enemy.x-player.x) <= enemy.spawnDistance:
                        if enemy.teleportTimes == 0:
                            enemy.teleport(player)
                            enemy.teleportTimes += 1
                        if enemy.health < enemy.initialHealth/2 and enemy.teleportTimes == 1:
                            enemy.teleport(player)
                            enemy.teleportTimes += 1
                    if enemy.startShootFireball == False and enemy.teleportTimes != 0:
                        enemy.fireballX, enemy.fireballY = enemy.x, enemy.y
                        enemy.finalFireballX, enemy.finalFireballY = player.x, player.y
                        enemy.startShootFireball = True
                        
                        

            for enemy in enemyList:
                if enemy.type == 'ghost' and enemy.startShootFireball == True:
                    enemy.shootFireball(enemy.finalFireballX, enemy.finalFireballY)


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
            if player.doubleJumping and player.level > 1:
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