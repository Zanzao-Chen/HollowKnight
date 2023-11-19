from cmu_graphics import *
from Player import *


player = Player(100, -200)

def onAppStart(app):
    app.stepsPerSecond = 30

def redrawAll(app):
    drawRect(player.x, -player.y, 20, 50, fill = 'black')
    print(player.y)

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
    
    
    

def main():
    runApp()

main()