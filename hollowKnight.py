from cmu_graphics import *
from Player import *
from Terrain import *

def onAppStart(app):
    app.stepsPerSecond = 30
    app.generalAttackCounter = 0
    app.previousAttackTime = 0
    app.initialAttackCounter = 0
    app.generalCounter = 0

player = Player(615, -100, 20, 50)
flat1 = Terrain(0, 250, app.width, 50, 'Rectangle')
flat2 = Terrain(200, 230, app.width*2, 50, 'Rectangle')
flat3 = Terrain(0, 230, 50, 50, 'Rectangle')
oval1 = Terrain(650, 230, 100, 50, 'outerOval')
oval2 = Terrain(650, 1000, 1000, 1600, 'outerOval')
terrainsList = [flat1, flat2, flat3, oval1, oval2]

def redrawAll(app):
    player.getPlayerVertices()
    if player.isAttacking == True or player.looksAttacking == True:
        drawRect(player.attackX, -player.attackY, player.attackWidth, player.attackHeight, fill='red', rotateAngle=player.rotateAngle)
        player.isAttacking = False

    for i in range(len(player.healthList)):
        if player.healthList[i] == True:
            drawCircle(player.healthX+player.healthXInterval*i, player.healthY, player.healthRadius, fill=player.yesHealthColor)
        else:
            drawCircle(player.healthX+player.healthXInterval*i, player.healthY, player.healthRadius, fill=player.noHealthColor)
    
    drawRect(player.x, -player.y, player.width, player.height, fill = 'black', rotateAngle = player.rotateAngle)
    drawCircle(player.orientationX, player.orientationY, 3, fill='red')
    player.previousPositions.append((player.x, -player.y))
    if len(player.previousPositions) > 5:
        player.previousPositions = player.previousPositions[2:]
    for terrain in terrainsList:
        if terrain.type == 'Rectangle':
            drawRect(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')
        elif terrain.type == 'outerOval':
            drawOval(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')

def onKeyPress(app, key):
    if key == 'a':
        player.direction = 'left'
        player.move(-1)
        for terrain in terrainsList:
            (isColliding, direction, reference) = checkColliding(terrain, player)
            if isColliding == True and terrain.type == 'Rectangle':
                if direction == 'right':
                    player.x = reference - player.width
                elif direction == 'left':
                    player.x = reference
    elif key == 'd':
        player.direction = 'right'
        player.move(+1)
        for terrain in terrainsList:
            (isColliding, direction, reference) = checkColliding(terrain, player)
            if isColliding == True and terrain.type == 'Rectangle':
                if direction == 'right':
                    player.x = reference - player.width
                elif direction == 'left':
                    player.x = reference
    if key == 'o' and player.jumping == False:
        player.jumping = True
    if key == 'j':
        player.attack()
    if key == 'p':
        player.updateHealth(-1)
     

def onKeyHold(app, key):
    if 'a' in key:
        player.move(-1)
        player.direction = 'left'
        for terrain in terrainsList:
            (isColliding, direction, reference) = checkColliding(terrain, player)
            if isColliding == True and terrain.type == 'Rectangle':
                if direction == 'right':
                    player.x = reference - player.width
                elif direction == 'left':
                    player.x = reference
    elif 'd' in key:
        player.direction = 'right'
        player.move(+1)
        for terrain in terrainsList:
            (isColliding, direction, reference) = checkColliding(terrain, player)
            if isColliding == True and terrain.type == 'Rectangle':
                if direction == 'right':
                    player.x = reference - player.width
                elif direction == 'left':
                    player.x = reference
    if 'j' in key:
        player.attack() 

def onStep(app):
    app.generalCounter += 1
    if player.looksAttacking == True:
        app.generalAttackCounter += 1
        if app.generalAttackCounter - app.initialAttackCounter > player.attackAppearDuration:
            app.initialAttackCounter = app.generalAttackCounter
            player.looksAttacking = False

    if player.falling == True:
        player.timer += 1
        player.fall()
    if player.jumping == True:
        player.timer += 1
        player.jump()
    for terrain in terrainsList:
        isColliding = False
        (isColliding, direction, reference) = checkColliding(terrain, player)
        if isColliding == True and terrain.type == 'Rectangle':
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
        elif isColliding == True and terrain.type == 'outerOval':
            if direction == 'down':
                player.getPlayerVertices()
                getY = terrain.getY(player.orientationX)
                realY = player.getMiddleXFromOrientation(getY)
                player.y = -(realY - player.height)
                player.jumping = False
                player.positions = []
                player.timer = 0
                

def checkColliding(terrain, player):
    player.getPlayerVertices()
    if terrain.type == 'Rectangle':
        return checkCollidingRect(terrain, player)
    elif terrain.type == 'outerOval':
        return checkCollidingOuterOval(terrain, player)

def checkCollidingRect(terrain, player):
    terrain.getTerrainVertices()
    if ((player.leftX > terrain.leftX) and (player.leftX < terrain.rightX) or
        (player.rightX > terrain.leftX) and (player.rightX < terrain.rightX)):
        if player.bottomY >= terrain.topY and player.bottomY <= terrain.bottomY:
            if len(player.previousPositions) <= 2:
                return (True, 'down', terrain.topY)
            previousX, previousY = player.previousPositions[-2]
            if previousY + player.height <= terrain.topY:
                return (True, 'down', terrain.topY)
    if ((player.bottomY > terrain.topY and player.bottomY < terrain.bottomY) or 
        (player.topY > terrain.topY and player.topY < terrain.bottomY)):
        if player.rightX >= terrain.leftX and player.rightX <= terrain.rightX:
            return (True, 'right', terrain.leftX) 
    if ((player.bottomY > terrain.topY and player.bottomY < terrain.bottomY) or 
        (player.topY > terrain.topY and player.topY < terrain.bottomY)):
        if player.leftX <= terrain.rightX and player.leftX >= terrain.leftX:
            return (True, 'left', terrain.rightX) 
    return False, None, None

def checkCollidingOuterOval(terrain, player):
    if player.jumping == True and player.reachFallPortion == False:
        return False, None, None
    else:
        player.getPlayerVertices()
        terrain.getTerrainVertices()
        if ((player.orientationX-terrain.x)/(terrain.width/2))**2 + ((player.orientationY-terrain.y)/(terrain.height/2))**2 < 1:
            setAngle(terrain, player)
            player.getPlayerVertices()
            if ((player.orientationX-terrain.x)/(terrain.width/2))**2 + ((player.orientationY-terrain.y)/(terrain.height/2))**2 < 1:
                return (True, 'down', player.orientationX)    
            if ((player.middleX-terrain.x)/(terrain.width/2))**2 + ((player.bottomY-terrain.y)/(terrain.height/2))**2 < 1:
                return (True, 'down', player.orientationX)    
        return False, None, None
        
def setAngle(terrain, player):
    xPartialDerivative =  2*(player.middleX - terrain.x)/((terrain.width/2)**2)
    yPartialDerivative = 2*(player.bottomY-terrain.y)/((terrain.height/2)**2)
    if yPartialDerivative == 0:
        player.rotateAngle = 0
        return
    alpha = math.atan(xPartialDerivative/(yPartialDerivative))*180/math.pi
    if alpha < 45 and alpha >= 0:
        player.rotateAngle = -alpha
    elif alpha >= 45:
        player.rotateAngle = -(90-alpha)
    elif alpha <= -45:
        player.rotateAngle = (90+alpha)
    elif alpha < 0 and alpha > -45:
        player.rotateAngle = -alpha

def main():
    runApp(width=1000, height=400)

main()