from cmu_graphics import *

class Map:
    def __init__(self, points, cell, presetHitbox = None):
        self.points = points
        self.start = points[0]
        self.finish = points[-1]
        self.cell = cell
        self.getDistances()
        self.getHitbox()

        if presetHitbox:
            for i in presetHitbox:
                self.hitbox.append([j * self.cell for j in i])
    
    def getDistances(self):
        self.distances = []
        for i in range(0, len(self.points) - 1):
            x1 = self.points[i][0] * self.cell
            y1 = self.points[i][1] * self.cell
            x2 = self.points[i + 1][0] * self.cell
            y2 = self.points[i + 1][1] * self.cell
            delta = int(distance(x1, y1, x2, y2))
            angle = int(angleTo(x1, y1, x2, y2))
            self.distances.append([delta , angle])
    
    def getHitbox(self):
        self.hitbox = []
        
        for i in range(0, len(self.points) - 1):

            x = (min(self.points[i][0], self.points[i + 1][0]) - 0.5) * self.cell
            y = (min(self.points[i][1], self.points[i + 1][1]) - 0.5) * self.cell
            angle = self.distances[i][1]

            if angle in [90, 270]:    
                deltaX = self.distances[i][0] + self.cell
                deltaY = self.cell
            else:
                deltaX = self.cell
                deltaY = self.distances[i][0] + self.cell
            
            self.hitbox.append([x, y, deltaX, deltaY])

map1 = [
    (-0.5, 4.5),    
    (9, 4.5),     
    (9, 1.5),     
    (6, 1.5),     
    (6, 9.5),     
    (3, 9.5),     
    (3, 6.5),     
    (11.5, 6.5),    
    (11.5, 3.5),    
    (13.5, 3.5),    
    (13.5, 8.5),    
    (8, 8.5),     
    (8, 12.5)
]

map2 = [
    (2.5, -0.5),
    (2.5, 11),
    (7.3, 11),
    (7.3, 4.5),
    (10.5, 4.5),
    (10.5, 8.0),
    (15.5, 8.0),
    (15.5, -0.5)
]

map3 = [
    (-0.5, 6.0),
    (4.0, 6.0),
    (4.0, 3.5),
    (7.5, 3.5),
    (7.5, 6.0),
    (11.5, 6.0),
    (11.5, 8.5),
    (15.0, 8.5),
    (15.0, 6.0),
    (16.5, 6.0),
    (15.0, 6.0),
    (15.0, 8.5),
    (11.5, 8.5),
    (11.5, 6.0),
    (7.5, 6.0),
    (7.5, 3.5),
    (4.0, 3.5),
    (4.0, 6.0),
    (-0.5, 6.0)
]

# forbidden hitboxes
preset2 = [
    [0, 0, 18, 5],
    [0, 0, 7, 12],
    [0, 7, 18, 5],
    [10, 0, 8, 12]
]

preset3 = [
    [12, 5, 3, 4]
]