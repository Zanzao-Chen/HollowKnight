import math

class Vector:
    def __init__(self, x, y, angle):
        self.initialX = x
        self.initialY = y
        self.angleY = angle
        self.angleX = 90-self.angleY
        self.gradient = (math.tan(self.angleX*math.pi/180))
        self.intercept = self.initialY - self.initialX*self.gradient
    def __repr__(self):
        return f"Vector x: {self.initialX}, y:{self.initialY}, angle: {self.angleY}, gradient = {self.gradient}, intercept = {self.intercept}"
    def getX(self, y):
        return (y - self.intercept)/self.gradient
    def getY(self, x):
        return x*self.gradient + self.intercept
    def getDistancePoint(self, x, y):
        return abs(self.gradient*x-y+self.intercept)/(1+self.gradient**2)**0.5
    def getRelativePositionOfPoint(self, x, y):
        if self.getY(x) == y and self.getX(y) == x:
            return ('on', 'on')
        if self.getY(x) < y:
            vertical = 'down'
        elif self.getY(x) > y:
            vertical = 'up'
        if self.getX(y) > x:
            horizontal = 'left'
        elif self.getX(y) < x:
            horizontal = 'right'
        return (horizontal, vertical)
    def getProjection(self, x, y):
        distance = self.getDistancePoint(self, x, y)
        deltaX = math.sin(self.angleY-90)*distance
        deltaY = math.cos(self.angleY-90)*distance
        horizontal, vertical = self.getRelativePositionOfPoint(x, y)
        if horizontal == 'on':
            return (x, y)
        if horizontal == 'left':
            newX = x + deltaX
        elif horizontal == 'right':
            newX = x - deltaX
        if vertical == 'down':
            newY = y - deltaY
        elif vertical == 'up':
            newY = y + deltaY
        return(newX, newY)
    
    def getIntersection(self, other):
        x = (other.intercept+self.intercept)/(self.gradient - other.gradient)
        y = self.gradient*x + self.intercept
        return (x, y)

    def draw(self):
        return self.initialX-1000, self.initialY+(1000*self.gradient), self.initialX+1000, self.initialY-(1000*self.gradient)

# vectorTest = Vector(1, 1+3**0.5, 30)
# print(vectorTest.gradient, vectorTest.intercept) # sqrt3, 1
# print(vectorTest.getY(2)) # 4.46
# print(vectorTest.getX(1+2*3**0.5)) # 2
# print(vectorTest.getDistancePoint(1+3**0.5, 3**0.5)) # 2
# print(vectorTest.getRelativePositionOfPoint(1+3**0.5, 3**0.5)) # right, up (vertical is reversed in cmu graphics)