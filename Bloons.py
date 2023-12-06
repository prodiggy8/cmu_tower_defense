from cmu_graphics.shape_logic import loadImageFromStringReference
from cmu_graphics import *
from copy import copy, deepcopy

# class of towers
# finish buttons

class Bloon(object):
    radius = 15
    # do not calculate distance in every wave !!!!!
    def __init__(self, map, cell, x, y):
        self.x = x
        self.y = y
        self.hp = 1
        self.coins = 5
        self.speed = 1 / 40
        self.iceResistance = False
        self.dartResistance = False
        self.explosionResistance = False
        self.frozen = False
        self.glued = False
        self.cell = cell
        self.map = deepcopy(map)
        
        # account for position in the queue when spawning
        if x < 0:
            self.map[0][0] += abs(x) - (0.5 * self.cell)
        if y < 0:
            self.map[0][0] += abs(y) - (0.5 * self.cell)

        # todo: make this ugly ass transpose line prettier
        self.distanceLeft = sum(list(zip(*self.map))[0])

        # sprite
        self.image = loadImageFromStringReference('cmu_tower_defense\\images\\redbloon.png')
        self.width, self.height = getImageSize(self.image)

    def makeMove(self):
        currentSegment = self.map[0]
        distance = min(self.cell * self.speed, currentSegment[0])
        
        self.x, self.y = getPointInDir(self.x, self.y, currentSegment[1], distance)

        currentSegment[0] -= distance
        self.distanceLeft -= distance

        if currentSegment[0] <= 0:
            self.map.pop(0)
    
    def kill(self, app):
        app.bloons.remove(self)
        app.coins += self.coins

    def __repr__(self):
        return f'Bloon {self.x} {self.y}'    
    
class RedBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.color = 'red'
    
class BlueBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.image = loadImageFromStringReference( 'cmu_tower_defense\\images\\bluebloon.png')
        self.color = 'blue'
        self.hp = 2
        self.coins = 10
        self.speed = 1 / 30

    def kill(self, app):
        app.bloons.remove(self)
        app.bloons.append(RedBloon(self.map, self.cell, self.x, self.y))
        app.coins += self.coins
        
class GreenBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.image = loadImageFromStringReference( 'cmu_tower_defense\\images\\greenbloon.png')
        self.color = 'green'
        self.hp = 3
        self.coins = 15
        self.speed = 1 / 20

    def kill(self, app):
        app.bloons.remove(self)
        app.bloons.append(BlueBloon(self.map, self.cell, self.x, self.y))
        app.coins += self.coins


class YellowBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.image = loadImageFromStringReference( 'cmu_tower_defense\\images\\yellowbloon.png')
        self.color = 'yellow'
        self.hp = 4
        self.coins = 20
        self.speed = 1 / 15

    def kill(self, app):
        app.bloons.remove(self)
        app.bloons.append(GreenBloon(self.map, self.cell, self.x, self.y))
        app.coins += self.coins

class PinkBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.image = loadImageFromStringReference( 'cmu_tower_defense\\images\\pinkbloon.png')
        self.color = 'pink'
        self.hp = 5
        self.coins = 25
        self.speed = 1 / 10

    def kill(self, app):
        app.bloons.remove(self)
        app.bloons.append(YellowBloon(self.map, self.cell, self.x, self.y))
        app.coins += self.coins


class BlackBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.image = loadImageFromStringReference( 'cmu_tower_defense\\images\\blackbloon.png')
        self.color = 'black'
        self.hp = 6
        self.coins = 50
        self.speed = 1 / 8
        self.radius = 10
        self.explosionResistance = True

    def kill(self, app):
        app.bloons.remove(self)
        app.bloons.append(PinkBloon(self.map, self.cell, self.x, self.y))
        app.bloons.append(PinkBloon(self.map, self.cell, self.x, self.y))
        app.coins += self.coins

class WhiteBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.image = loadImageFromStringReference( 'cmu_tower_defense\\images\\whitebloon.png')
        self.color = 'white'
        self.hp = 6
        self.coins = 50
        self.speed = 1 / 9
        self.radius = 10
        self.iceResistance = True

    def kill(self, app):
        app.bloons.remove(self)
        app.bloons.append(PinkBloon(self.map, self.cell, self.x, self.y))
        app.bloons.append(PinkBloon(self.map, self.cell, self.x, self.y))
        app.coins += self.coins

class ReinforcedBloon(Bloon):
    def __init__(self, map, cell, x, y):
        super().__init__(map, cell, x, y)
        self.image = loadImageFromStringReference( 'cmu_tower_defense\\images\\reinforcedbloon.png')
        self.color = 'grey'
        self.hp = 7
        self.coins = 50
        self.speed = 1 / 15
        self.radius = 15
        self.dartResistance = True

    def kill(self, app):
        app.bloons.remove(self)
        app.bloons.append(BlackBloon(self.map, self.cell, self.x, self.y))
        app.bloons.append(BlackBloon(self.map, self.cell, self.x, self.y))
        app.coins += self.coins