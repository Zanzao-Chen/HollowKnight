from cmu_graphics import *
from Player import *


player = Player(50, 50)

def onAppStart(app):
    pass

def redrawAll(app):
    drawRect(player.x, player.y, 50, 50, fill = 'black')

def onKeyPress(app, key):
    if key == 'a':
        player.move(player.x, -1)
    elif key == 'd':
        player.move(player.x, +1)
    # if key == 'o' and player.jumping == False:
    #     player.jump(player.y)

def onKeyHold(app, key):
    if 'a' in key:
        player.move(player.x, -1)
    elif 'd' in key:
        player.move(player.x, +1)

def main():
    runApp()

main()