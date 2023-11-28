# Citations:
# Stack Overflow, How to detect when rotated rectangles are colliding each other
# https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other 
# I did not use any code from this source; I only used the visual pictures to understand the theory for the separating axis algorithm

# How to run: use ctrl+b on this file, with the other .py files in the same folder

from cmu_graphics import *
from Player import *
from Terrain import *
from Enemy import *

from PIL import Image, ImageOps
import os, pathlib

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
    app.generalFallingCounter = 0
    app.initialFallingCounter = 0
    app.generalDashingCounter = 0
    app.initialDashingCounter = 0

    app.idleSprites = []
    createPlayerSprites(app)

player = Player(215, -100, 20, 50)
flat1 = Terrain(0, 250, app.width, 50, 'Rectangle')
flat2 = Terrain(200, 230, app.width*2, 50, 'Rectangle')
flat3 = Terrain(0, 230, 50, 50, 'Rectangle')
oval1 = Terrain(650, 230, 100, 50, 'outerOval')
oval2 = Terrain(650, 1000, 1000, 1600, 'outerOval')


groundEnemy1 = GroundEnemy(400, 100, 30, 30, 50, None)
groundEnemy2 = GroundEnemy(800, 100, 30, 30, 50, None)
groundEnemyVertical1 = GroundEnemyVertical(720, 100, 30, 30, 500, None)

terrainsList = [flat1, flat2, flat3, oval1, oval2]
enemyList = [groundEnemy1, groundEnemy2, groundEnemyVertical1]

def redrawAll(app):
    # drawRect(0, 0, 1000, 400, fill='grey') 
    drawLabel('O is jump, J is attack, I is dash', 200, 100)
    drawLabel('Use AWDS to move and control attack direction', 200, 150)
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
    for (x, y, angle) in player.dashingPositions:
        drawRect(x, -y, player.width, player.height, fill = 'black', rotateAngle = angle, opacity = 20)
    drawRect(player.x, -player.y, player.width, player.height, fill = 'black', rotateAngle = player.rotateAngle)
    drawCircle(player.orientationX, player.orientationY, 3, fill='red')
    
    if player.direction == 'left':
        sprite = app.idleSprites[1]
        drawImage(sprite, player.x, -player.y+18, rotateAngle = player.rotateAngle, align = 'center')
    elif player.direction == 'right':
        sprite = app.idleSprites[0]
        drawImage(sprite, player.x, -player.y+18, rotateAngle = player.rotateAngle, align = 'center')

def createPlayerSprites(app):
    spritestrip = Image.open('playerSprites.png')
    i = 0
    frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
    sprite = CMUImage(frame)
    app.idleSprites.append(sprite)

    spritestrip = Image.open('playerSprites.png')
    i = 0
    frame = spritestrip.crop((0+79*i, 2, 79+79*i, 79))
    frameFlipped = ImageOps.mirror(frame)
    sprite = CMUImage(frameFlipped)
    
    app.idleSprites.append(sprite)

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
        if enemy.isKilled == False:
            drawRect(enemy.x, -enemy.y, enemy.width, enemy.height, rotateAngle = enemy.rotateAngle)
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
        if 's' in key:
            player.holdingDown = True
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
    if key == 'w':
        player.holdingUp = False
    elif key == 's':
        player.holdingDown = False

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


def main():
    runApp(width=1000, height=400)

main()