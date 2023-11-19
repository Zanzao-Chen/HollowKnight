from cmu_graphics import *
from Player import *
from Terrain import *

def onAppStart(app):
    app.stepsPerSecond = 30

player = Player(100, -200, 20, 50)
flat1 = Terrain(0, 250, app.width, 50, 'Rectangle')
flat2 = Terrain(200, 230, app.width, 50, 'Rectangle')
terrainsList = [flat1, flat2]

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
        (isColliding, direction) = checkColliding(terrain, player)
        if isColliding == True:
            if direction == 'right':
                player.x = terrain.leftX - player.width

def checkColliding(terrain, player):
    player.getPlayerVertices()
    terrain.getTerrainVertices()
    if ((player.bottomY > terrain.topY and player.bottomY <= terrain.bottomY) or 
        (player.topY > terrain.topY and player.topY <= terrain.bottomY)):
        if player.rightX >= terrain.leftX:
            return (True, 'right') # direction is relative to the player
    return False, None

def main():
    runApp()

main()