from cmu_graphics import *

def onAppStart(app):
    app.x, app.y = 100, 100
    
def redrawAll(app):
    drawRect(app.x, app.y, 500, 500, fill = 'black')

def main():
    runApp()

main()