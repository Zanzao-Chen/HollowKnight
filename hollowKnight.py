from cmu_graphics import *
from Player import *
from Terrain import *

def onAppStart(app):
    app.stepsPerSecond = 30

player = Player(100, -200, 20, 50)
flat1 = Terrain(0, 250, app.width, 50, 'Rectangle')
flat2 = Terrain(200, 230, app.width, 50, 'Rectangle')
flat3 = Terrain(0, 230, 50, 50, 'Rectangle')
terrainsList = [flat1, flat2, flat3]

def redrawAll(app):
    drawRect(player.x, -player.y, player.width, player.height, fill = 'black')
    for terrain in terrainsList:
        if terrain.type == 'Rectangle':
            drawRect(terrain.x, terrain.y, terrain.width, terrain.height, fill = 'green')

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
    elif 'd' in key:
        player.move(+1)

def onStep(app):
    
    if player.jumping == True:
        player.timer += 1
        player.jump()
    for terrain in terrainsList:
        (isColliding, direction, reference) = checkColliding(terrain, player)
        if isColliding == True:
            if direction == 'right':
                player.x = reference - player.width
            elif direction == 'left':
                player.x = reference
            elif direction == 'up':
                player.y = terrain.bottomY  
            elif direction == 'down':
                player.y = -(reference - player.height)

def checkColliding(terrain, player):
    player.getPlayerVertices()
    terrain.getTerrainVertices()
    if ((player.leftX > terrain.leftX) and (player.leftX < terrain.rightX) or
        (player.rightX > terrain.leftX) and (player.rightX < terrain.rightX)):
        if player.bottomY >= terrain.topY and player.bottomY <= terrain.bottomY:
            return (True, 'down', terrain.topY)
    if ((player.bottomY > terrain.topY and player.bottomY < terrain.bottomY) or 
        (player.topY > terrain.topY and player.topY < terrain.bottomY)):
        if player.rightX >= terrain.leftX and player.rightX <= terrain.rightX:
            print(player.bottomY, terrain.topY, terrain.bottomY)
            return (True, 'right', terrain.leftX) 
    if ((player.bottomY > terrain.topY and player.bottomY < terrain.bottomY) or 
        (player.topY > terrain.topY and player.topY < terrain.bottomY)):
        if player.leftX <= terrain.rightX and player.leftX >= terrain.leftX:
            return (True, 'left', terrain.rightX) 


    return False, None, None

def main():
    runApp()

main()