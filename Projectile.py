from cmu_graphics.shape_logic import loadImageFromStringReference
from cmu_graphics import *
import math

# projectile velocity is constant at 15 m/s

class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = target.cell //  4  # arbitrary constant
        self.type = 'dart'
        self.sprite = loadImageFromStringReference('cmu_tower_defense\\images\\dart.png')
        self.width, self.height = getImageSize(self.sprite)

        # displacement for the time the bullet takes to arrive
        self.starting = distance(self.x, self.y, self.target.x, self.target.y)
        self.displacement = (self.starting / self.speed) * (self.target.speed * self.target.cell)

        # account for change of direction
        if self.target.map[0][0] < self.displacement:
            x, y = getPointInDir(self.target.x, self.target.y, self.target.map[0][1], self.target.map[0][0])
            angle = self.target.map[1][1]
            delta = self.displacement - self.target.map[0][0]
        else:
            x, y = self.target.x, self.target.y
            angle = self.target.map[0][1]
            delta = self.displacement

        # create path
        self.targetX, self.targetY = getPointInDir(x, y, angle, delta)  
        self.angle = angleTo(self.x, self.y, self.targetX, self.targetY)    
        self.distance = distance(self.x, self.y, self.targetX, self.targetY)

    def update(self, app):
        self.distance -= self.speed
        self.x, self.y = getPointInDir(self.x, self.y, self.angle, self.speed)
    
        if self.distance <= 0:
            app.targets.remove(self.target)
            app.bullets.remove(self)
            
            if not self.target.dartResistance:
                self.target.kill(app)

class Dart(Projectile):
    def __init__(self, x, y, target):
        super().__init__(x, y, target)

class Ball(Projectile):
    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        self.sprite = loadImageFromStringReference('cmu_tower_defense\\images\\ball.png')
        self.width, self.height = getImageSize(self.sprite)

class Shuriken(Projectile):
    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        self.sprite = loadImageFromStringReference('cmu_tower_defense\\images\\shuriken.png')
        self.width, self.height = getImageSize(self.sprite)

        # shuriken stops after two bloons or 300 meters
        self.distance = 300
        self.killed = 0
    
    # shuriken intersecting bloon, not the other way around
    def isIntersecting(self, x, y, height):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2) <= height

    def update(self, app):
        self.distance -= self.speed
        self.x, self.y = getPointInDir(self.x, self.y, self.angle, self.speed)

        for i in app.bloons:
            if self.isIntersecting(i.x, i.y, i.height) and (i == self.target or i not in app.targets):
                self.killed += 1
                
                i.kill(app)
            
            if self.killed >= 2:
                app.targets.remove(self.target)
                app.bullets.remove(self)
                break

        if self.distance <= 0 or self.x < 0:
            app.targets.remove(self.target)
            app.bullets.remove(self)        

class Boomerang(Projectile):
    def __init__(self, x, y, target):
        super().__init__(x, y, target)

        self.sprite = loadImageFromStringReference('cmu_tower_defense\\images\\boomerang.png')
        self.width, self.height = getImageSize(self.sprite)
        
        self.radius = self.distance // 2
        self.cx, self.cy = getPointInDir(self.x, self.y, self.angle, self.radius)
        self.circunference = 2 * math.pi * self.radius 
        self.fangle = 0 #angleTo(self.cx, self.cy, self.x, self.y)
        self.remaining = 360
        self.speed = 10 # arbitrary constraint
        self.killed = 0
        
        

    def update(self, app):
        self.angle = (self.angle + self.speed) % 360
        self.x = self.cx + math.cos(math.radians(self.angle)) * self.radius
        self.y = self.cy + math.sin(math.radians(self.angle)) * self.radius

        self.remaining -= self.speed

        if self.remaining <= 180:
            
            if self.target in app.targets:
                app.targets.remove(self.target)
                self.target.kill(app)
                
            if self.remaining <= 0:
                app.bullets.remove(self)

class Bomb(Projectile):
    def __init__(self, x, y, target):
        super().__init__(x, y, target)
        self.radius = 40
        self.type = 'bomb'
        self.sprite = loadImageFromStringReference('cmu_tower_defense\\images\\bomb.png')
        self.width, self.height = getImageSize(self.sprite)
    
    def isIntersecting(self, x, y):
        return math.sqrt((self.targetX - x) ** 2 + (self.targetY - y) ** 2) <= self.radius

    def update(self, app):
        self.distance -= self.speed
        self.x, self.y = getPointInDir(self.x, self.y, self.angle, self.speed)
    
        if self.distance <= 0:
            
            app.targets.remove(self.target)
            app.bullets.remove(self)
            
            if not self.target.explosionResistance:
                self.target.kill(app)

            for i in app.bloons:
                if self.isIntersecting(i.x, i.y) and i not in app.targets:
                    if not i.explosionResistance:
                        i.kill(app)

            
    
    

    
