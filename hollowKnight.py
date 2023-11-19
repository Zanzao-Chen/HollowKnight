from cmu_graphics import *
from Player import *


player = Player(100, 200)

def onAppStart(app):
    app.stepsPerSecond = 30

def redrawAll(app):
    drawRect(player.x, player.y, 20, 50, fill = 'black')

def onKeyPress(app, key):
    if key == 'a':
        player.move(-1)
    elif key == 'd':
        player.move(+1)
    if key == 'o':
        player.jump()

def onKeyHold(app, key):
    if 'a' in key:
        player.move(-1)
    elif 'd' in key:
        player.move(+1)

def onStep(app):
    if player.jumping == True:
        player.y -= 1.5
        player.positions.append(player.y)
        if player.y + 30 < player.positions[0]:
            player.jumping = False
            player.falling = True 
            player.positions = []
    if player.falling == True:
        player.y += 1.5
        player.positions.append(player.y)
        if player.y > 30 + player.positions[0]:
            player.jumping = False
            player.falling = False
            player.positions = []
    
    

def main():
    runApp()

main()