from cmu_graphics import *
from Player import *
from Terrain import *

def onAppStart(app):
    app.stepsPerSecond = 30

player = Player(400, -50, 20, 50)
flat1 = Terrain(0, 250, app.width, 50, 'Rectangle')
flat2 = Terrain(200, 230, app.width, 50, 'Rectangle')
flat3 = Terrain(0, 230, 50, 50, 'Rectangle')
oval1 = Terrain(650, 230, 100, 50, 'outerOval')
terrainsList = [flat1, flat2, flat3, oval1]

def redrawAll(app):
    drawRect(player.x, -player.y, player.width, player.height, fill = 'black')
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
        player.move(-1)
    elif key == 'd':
        player.move(+1)
    if key == 'o' and player.jumping == False:
        player.jumping = True
     

def onKeyHold(app, key):
    if 'a' in key:
        player.move(-1)
        for terrain in terrainsList:
            (isColliding, direction, reference) = checkColliding(terrain, player)
            if isColliding == True and terrain.type == 'Rectangle':
                if direction == 'right':
                    player.x = reference - player.width
                elif direction == 'left':
                    player.x = reference
    elif 'd' in key:
        player.move(+1)
        for terrain in terrainsList:
            (isColliding, direction, reference) = checkColliding(terrain, player)
            if isColliding == True and terrain.type == 'Rectangle':
                if direction == 'right':
                    player.x = reference - player.width
                elif direction == 'left':
                    player.x = reference
        

def onStep(app):
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
            if direction == 'right':
                player.getPlayerVertices()
                getY = terrain.getY(player.rightX)
                player.y = -(getY - player.height*2)
                player.x = terrain.getX(getY) - player.width*2

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
    player.getPlayerVertices()
    if ((player.rightX-terrain.x)/(terrain.width/2))**2 + ((player.bottomY-terrain.y)/(terrain.width/2))**2 <= 1:
        if player.rightX < terrain.x:
            return (True, 'right', terrain)
        elif player.leftX > terrain.x:
            return (True, 'left', terrain)
        elif player.x == terrain.x:
            return (True, 'above', terrain)
    return False, None, None


def main():
    runApp()

main()