from cmu_graphics.shape_logic import loadImageFromStringReference
from cmu_graphics import *
from Projectile import *
from time import time
import math
from functools import cache

class Tower:
    spriteRadius = 25 # check the need for this
    radius = 120
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cooldown = 1
        self.lastShot = 0
        self.angle = 0

    def isIntersecting(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2) <= self.radius
    
    def towerIntersection(self, x, y, width, height):
        if ((self.x <= x <= self.x + self.width) or (self.x <= x + width <= self.x + self.width)) and \
           ((self.y <= y <= self.y + self.height) or (self.y <= y + height <= self.y + self.height)):
            return True
        return False

    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            bloon, distance = None, app.totalDistance
            for i in app.bloons:
                if self.isIntersecting(i.x, i.y) and i.x > 0 and i not in app.targets:
                    if i.distanceLeft < distance:
                        distance = i.distanceLeft
                        bloon = i
                        
            if bloon:
                self.angle = (angleTo(self.x, self.y, bloon.x, bloon.y) + 180) % 360
                self.lastShot = time() 
                app.targets.add(bloon)
                app.bullets.append(Projectile(self.x, self.y, bloon))

class Monkey(Tower):
    name = 'Monkey'
    cost = 200
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Monkey.getSprite()
        self.width, self.height = Monkey.getDimensions(self.sprite)

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\dartmonkey.png')
    
    @cache
    def getStoreSprite():
        return 'dartmonkey'

    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)

# needs work       
class TackShooter(Tower):
    name = 'Tack Shooter'
    cost = 300
    radius = 80

    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = TackShooter.getSprite()
        self.width, self.height = TackShooter.getDimensions(self.sprite)
        
        # get directions
        self.shoots = []
        self.getShoots()

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\tackshooter.png')
    
    @cache
    def getStoreSprite():
        return 'tackshooter'

    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)

    def getShoots(self):
        for i in range(0, 316, 45):
            self.shoots.append(getPointInDir(self.x, self.y, i, self.radius))

    def linePoint(self, x1, y1, x2, y2, px, py):
        d1 = distance(px, py, x1, y1)
        d2 = distance(px, py, x2, y2)
        if d1 + d2 >= self.radius - 0.1 and d1 + d2 <= self.radius + 0.1:
            return True
        return False

    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            for x, y in self.shoots:    
                for i in app.bloons:
                    if i.x > 0 and i not in app.targets:
                        # line circle intersection
                        dot = (((i.x - self.x) * (x - self.x)) + ((i.y - self.y) * (y - self.y))) / self.radius ** 2
                        closestX = self.x + (dot * (x - self.x))
                        closestY = self.y + (dot * (y - self.y))
                        
                        if not self.linePoint(self.x, self.y, x, y, closestX, closestY):
                            continue
                        
                        distX = closestX - i.x
                        distY = closestY - i.y
                        
                        if math.sqrt((distX * distX) + (distY * distY)) <= i.radius:
                            if not i.dartResistance:
                                i.kill(app)
                                break

            self.lastShot = time()
        
class NinjaMonkey(Tower):
    name = 'Ninja'
    cost = 600
    
    radius = 150

    def __init__(self, x, y):
        super().__init__(x, y)
        self.cooldown = 0.8
        
        self.sprite = NinjaMonkey.getSprite()
        self.width, self.height = NinjaMonkey.getDimensions(self.sprite)

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\ninjamonkey.png')
    
    @cache
    def getStoreSprite():
        return 'ninjamonkey'
    
    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)

    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            bloon, distance = None, app.totalDistance
            for i in app.bloons:
                if self.isIntersecting(i.x, i.y) and i.x > 0 and i not in app.targets:
                    if i.distanceLeft < distance:
                        distance = i.distanceLeft
                        bloon = i
                        
            if bloon:
                self.angle = (angleTo(self.x, self.y, bloon.x, bloon.y) + 180) % 360
                self.lastShot = time() 
                app.targets.add(bloon)
                app.bullets.append(Shuriken(self.x, self.y, bloon))
    
class Cannon(Tower):
    name = 'Cannon'
    cost = 500
    radius = 180
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = Cannon.getSprite()
        self.width, self.height = Cannon.getDimensions(self.sprite)
        self.cooldown = 2

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\cannon.png')
    
    @cache
    def getStoreSprite():
        return 'cannon'

    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)

    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            bloon, distance = None, app.totalDistance
            for i in app.bloons:
                if self.isIntersecting(i.x, i.y) and i.x > 0 and i not in app.targets:
                    if i.distanceLeft < distance:
                        distance = i.distanceLeft
                        bloon = i
                        
            if bloon:
                self.angle = (angleTo(self.x, self.y, bloon.x, bloon.y) + 180) % 360
                self.lastShot = time() 
                app.targets.add(bloon)
                app.bullets.append(Bomb(self.x, self.y, bloon))
        
class BoomerangMonkey(Tower):
    name = 'Boomerang Monkey'
    cost = 300
    radius = 240

    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = BoomerangMonkey.getSprite()
        self.width, self.height = BoomerangMonkey.getDimensions(self.sprite)
        self.cooldown = 1

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\boomerangmonkey.png')
    
    @cache
    def getStoreSprite():
        return 'boomerangmonkey'

    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)
    
    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            bloon, distance = None, app.totalDistance
            for i in app.bloons:
                if self.isIntersecting(i.x, i.y) and i.x > 0 and i not in app.targets:
                    if i.distanceLeft < distance:
                        distance = i.distanceLeft
                        bloon = i
                        
            if bloon:
                self.angle = (angleTo(self.x, self.y, bloon.x, bloon.y) + 180) % 360
                self.lastShot = time() 
                app.targets.add(bloon)
                app.bullets.append(Boomerang(self.x, self.y, bloon))

class SniperMonkey(Tower):
    name = 'Sniper Monkey'
    cost = 400
    radius = 50

    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = SniperMonkey.getSprite()
        self.width, self.height = SniperMonkey.getDimensions(self.sprite)
        self.cooldown = 1.25

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\snipermonkey.png')
    
    @cache
    def getStoreSprite():
        return 'snipermonkey'

    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)

    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            bloon, distance = None, app.totalDistance
            for i in app.bloons:
                if i.x > 0 and i not in app.targets:
                    if i.distanceLeft < distance:
                        distance = i.distanceLeft
                        bloon = i
                        
            if bloon:
                self.angle = (angleTo(self.x, self.y, bloon.x, bloon.y) + 180) % 360
                self.lastShot = time() 
                
                # no bullets
                if not bloon.dartResistance:
                    bloon.kill(app)

class GlueGunner(Tower):
    name = 'Glue Gunner'
    cost = 300

    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = GlueGunner.getSprite()
        self.width, self.height = GlueGunner.getDimensions(self.sprite)
        self.cooldown = 0.8
    
    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\gluegunner.png')
    
    @cache
    def getStoreSprite():
        return 'gluegunner'

    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)

    def shootBloon(self, app):
        bloon, distance = None, app.totalDistance
        for i in app.bloons:
            if self.isIntersecting(i.x, i.y) and not i.glued:
                if i.distanceLeft < distance:
                    distance = i.distanceLeft
                    bloon = i
                    
        if time() - self.lastShot > self.cooldown and bloon:
            self.lastShot = time() 
            bloon.glued = True
            bloon.speed *= 0.5

class IceMonkey(Tower):
    name = 'Ice Monkey'
    cost = 300
    radius = 80

    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = IceMonkey.getSprite()
        self.width, self.height = IceMonkey.getDimensions(self.sprite)
        self.cooldown = 3
        self.frozen = []

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\icemonkey.png')
    
    @cache
    def getStoreSprite():
        return 'icemonkey'
    
    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)
    
    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            for i in app.bloons:
                if self.isIntersecting(i.x, i.y) and i.x > 0 and i not in app.targets:
                    if not i.iceResistance:
                        self.frozen.append([i, i.speed, i.dartResistance, i.explosionResistance])
                        i.speed = 0
                        i.dartResistance = True
                        i.explosionResistance = False

            self.lastShot = time() 

        elif time() - self.lastShot > self.cooldown / 2:
            for i in self.frozen:
                i[0].speed = i[1]
                i[0].dartResistance = i[2]
                i[0].explosionResistance = i[3]
                
            self.frozen = []
    
class SuperMonkey(Tower):
    name = 'Super Monkey'
    cost = 3500
    radius = 240

    def __init__(self, x, y):
        super().__init__(x, y)
        self.sprite = SuperMonkey.getSprite()
        self.width, self.height = SuperMonkey.getDimensions(self.sprite)
        self.cooldown = 0.2
        self.radius = SuperMonkey.radius
        self.cost = SuperMonkey.cost

    @cache
    def getSprite():
        return loadImageFromStringReference('cmu_tower_defense\\images\\hd\\supermonkey.png')
    
    @cache
    def getStoreSprite():
        return 'supermonkey'
    
    @cache
    def getDimensions(sprite):
        return getImageSize(sprite)
    
    def shootBloon(self, app):
        if time() - self.lastShot > self.cooldown:
            bloon, distance = None, app.totalDistance
            for i in app.bloons:
                if self.isIntersecting(i.x, i.y) and i.x > 0 and i not in app.targets:
                    if i.distanceLeft < distance:
                        distance = i.distanceLeft
                        bloon = i
                        
            if bloon:
                self.angle = (angleTo(self.x, self.y, bloon.x, bloon.y) + 180) % 360
                self.lastShot = time() 
                app.targets.add(bloon)
                app.bullets.append(Ball(self.x, self.y, bloon))