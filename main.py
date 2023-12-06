from cmu_graphics.shape_logic import loadImageFromStringReference
from cmu_graphics import *
from Bloons import *
from Towers import *
from Map import *

debug = False

def onAppStart(app):
    # game logic
    app.towerOrd = [Monkey, TackShooter, NinjaMonkey, Cannon, BoomerangMonkey, SniperMonkey, GlueGunner, IceMonkey, SuperMonkey]
    app.bloonOrd = [RedBloon, BlueBloon, GreenBloon, YellowBloon, PinkBloon, BlackBloon, WhiteBloon, ReinforcedBloon]
    app.levels = [
        [10, 0, 0, 0, 0, 0, 0, 0],
        [20, 0, 0, 0, 0, 0, 0, 0],
        [15, 5, 0, 0, 0, 0, 0, 0],
        [20, 10, 0, 0, 0, 0, 0, 0], 
        [20, 5, 5, 0, 0, 0, 0, 0],
        [10, 10, 10, 10, 0, 0, 0, 0],
        [0, 20, 5, 5, 5, 0, 0, 0],
        [9, 9, 9, 9, 9, 9, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 10],
        [40, 0, 10, 20, 0, 20, 20, 0],
        [0, 0, 40, 50, 0, 20, 10, 0],
        [0, 40, 30, 20, 10, 10, 10, 10],
        [0, 40, 40, 0, 40, 30, 30, 30]
    ]
    app.levelStarted = False
    app.levelEnded = True
    app.level = 1
    app.coins = 400
    app.hp = 100
    app.bloons = []
    app.towers = []
    app.bullets = []
    app.targets = set()

    # scales
    updateScales(app)

    # fps
    app.stepsPerSecond = 30

    # state control
    app.storeSelection = False
    app.storePlacement = False
    app.towerSelection = False
    app.drawHomeScreen = True
    app.printLabel = ''

    # images

    app.images = [
        'meadows', 'corn', 'gluecover', 'icecover', 'hp', 'coins', 'storebg', 'background', 'button', 'start', 'home',
        'dartmonkey', 'boomerangmonkey', 'tackshooter', 'snipermonkey', 'ninjamonkey', 'supermonkey', 'cannon',
        'icemonkey', 'gluegunner', 'homescreen', 'bloons', 'cmu', 'road', 'win', 'defeat'
    ]

    # image sprites and dimensions
    app.sprites = {
        i: [loadImageFromStringReference(f'cmu_tower_defense\\images\\{i}.png'),
            (getImageSize(loadImageFromStringReference(f'cmu_tower_defense\\images\\{i}.png')))]
        for i in app.images
    }
    
def updateScales(app):
    # scales
    app.cols = 18
    app.rows = 12
    app.canvasWidth = 0.84375 * app.width
    app.cell = app.canvasWidth / app.cols
    app.cellH = app.height / app.rows
    
    app.storeWidth = app.width - app.canvasWidth
    app.storeMarginX = 0.05 * app.storeWidth
    app.storeMarginY = 0.03 * app.height
    app.storeItemWidth = 0.5 * (app.storeWidth - 2 * app.storeMarginX)
    app.storeItemHeight = 0.125 * (app.height - 2 * app.storeMarginY)

def checkGameState(app):
    return (app.levels or app.bloons) and app.hp > 0

def onStep(app):    
    updateScales(app)

    # win conditions
    if checkGameState(app) and not app.drawHomeScreen:

        # spawn queue of bloons
        if app.levelStarted:
            bloons = 0
            for i in range(len(app.levels[0])):
                for j in range(app.levels[0][i]):
                    isXStart = (app.m.start[0] < 0) * (-0.5 * app.cell * bloons)
                    isYStart = (app.m.start[1] < 0) * (-0.5 * app.cell * bloons)
                    app.bloons.append(app.bloonOrd[i](app.map, app.cell, app.m.start[0] * app.cell + isXStart, app.m.start[1] * app.cell + isYStart))
                    bloons += 1
                
            app.levelStarted = app.levelEnded = False
            app.levels.pop(0)
        
        # perform movement, check defeat
        for i in app.bloons:
            tryMove(app, i)
            
            if app.hp <= 0:
                app.bloons.clear()
                break
        
        # try shooting bloons
        for i in app.towers:
            i.shootBloon(app)

        # move bullets
        for i in app.bullets:
            i.update(app)

        # next level
        if not app.bloons and not app.levelEnded:
                app.levelEnded = True

                # check win
                if checkGameState(app):
                    app.level += 1

def tryMove(app, bloon):
    bloon.makeMove()
    if bloon.distanceLeft <= bloon.speed:
        app.hp -= bloon.hp
        app.bloons.remove(bloon)

def getCell(app, x, y):
    col = int(x // (app.canvasWidth / app.cols))
    row = int(y // (app.height / app.rows))
    return col, row

def onMousePress(app, x, y):
    if app.drawHomeScreen:
        width = app.width * 0.22 * 0.5
        height = app.height * 0.15 * 0.5

        if app.width * 0.2 - width <= x <= app.width * 0.2  + width and \
           app.height * 0.75 - height <= y <= app.height * 0.75 + height:
            app.drawHomeScreen = False
            map, preset = map1, None
            app.scene = 'meadows'

        elif app.width * 0.8 - width <= x <= app.width * 0.8 + width and \
             app.height * 0.75 - height <= y <= app.height * 0.75 + height:
            app.drawHomeScreen = False
            map, preset = map3, preset3
            app.scene = 'road'

        elif app.width * 0.5 - width <= x <= app.width * 0.5 + width and \
             app.height * 0.75 - height <= y <= app.height * 0.75 + height:
            app.drawHomeScreen = False
            map, preset = map2, preset2
            app.scene = 'corn'
            
        # canvas
        if not app.drawHomeScreen:
            app.m = Map(map, app.cell, presetHitbox = preset)
            app.map = app.m.distances
            app.hitbox = app.m.hitbox
            app.totalDistance = sum(list(zip(*app.map))[0]) + 1

    elif checkGameState(app):
        
        # store
        if x > app.canvasWidth:
            # start game or start next level
            if app.levelEnded and \
            x <= app.canvasWidth + app.storeMarginX + app.sprites['start'][1][0] and \
            x >= app.canvasWidth + app.storeMarginX and \
            y <= app.height - app.storeMarginY and \
            y >= app.height - app.storeItemHeight - app.storeMarginY:
                app.levelStarted = True

            # home screen
            if app.levelEnded and \
            x <= app.canvasWidth + 2 * (app.storeMarginX + app.sprites['start'][1][0]) and \
            x >= app.canvasWidth + 2* app.storeMarginX + app.sprites['start'][1][0] and \
            y <= app.height - app.storeMarginY and \
            y >= app.height - app.storeItemHeight - app.storeMarginY:
                onAppStart(app)

            # buy monkeys
            for i in range(9):
                left = app.canvasWidth + 0.5 * app.storeMarginX + (i // 5) * (app.storeItemWidth +  app.storeMarginX)
                top = app.storeMarginY + (i % 5) * (app.storeItemHeight + app.storeMarginY)
                
                if  left <= x <= left + app.storeItemWidth and top <= y <= top + app.storeItemHeight:
                    app.storeSelection = app.towerOrd[i]
            
            app.towerSelection = False
                    
        # placing tower
        elif app.storeSelection: 
            if isValidPlacement(app, x, y):
                
                # must have enough money
                if app.storeSelection.cost <= app.coins:
                    app.towers.append(app.storeSelection(x, y))
                    app.coins -= app.storeSelection.cost

            app.storeSelection = False
            app.storePlacement = False
            app.towerSelection = False

        # selecting tower
        else:
            for i in app.towers:

                # sell button
                if distance(x, y, i.x, i.y - 2 * i.spriteRadius) < i.spriteRadius // 3:
                    app.coins += i.cost
                    app.towers.remove(i)    
                    app.towerSelection = False
                    break
                
                # select tower
                if distance(x, y, i.x, i.y) <= i.spriteRadius and app.towerSelection != i:
                    app.towerSelection = i
                    break
            else:
                app.towerSelection = False

def onMouseMove(app, x, y):
    if x < app.canvasWidth and app.storeSelection:
        app.storePlacement = (x, y)

    # name of the tower when hovering
    for i in range(9):
        left = app.canvasWidth + 0.5 * app.storeMarginX + (i // 5) * (app.storeItemWidth +  app.storeMarginX)
        top = app.storeMarginY + (i % 5) * (app.storeItemHeight + app.storeMarginY)
        
        if  left <= x <= left + app.storeItemWidth and top <= y <= top + app.storeItemHeight:
            app.printLabel = app.towerOrd[i].name
            break
    else:
        app.printLabel = ''

def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)

def isValidPlacement(app, x, y):
    for i in app.hitbox:
        if (x >= i[0] and x <= i[0] + i[2]) and \
           (y >= i[1] and y <= i[1] + i[3]): 
            return False
    else:
        for i in app.towers:
            if i.towerIntersection(x, y, *app.storeSelection.getDimensions(app.storeSelection.getSprite())):
                return False            
    return True

# View

def drawCanvas(app):
    drawImage(app.sprites[app.scene][0], 0, 0, width = 1080, height = 720)
    
    if debug:
        for i in range(18):
            for j in range(12):
                drawRect(i * app.cell, j * app.cell, app.cell, app.cell, fill = None, border = 'black')

def drawStore(app):
    # store background
    drawImage(app.sprites['storebg'][0], app.canvasWidth, 0)
    drawRect(app.width - app.storeWidth, 0, app.storeWidth, app.height, fill = rgb(191, 151, 95), opacity = 50)

    # buttons
    drawImage(app.sprites['start'][0], app.canvasWidth + app.storeMarginX, app.height - app.storeItemHeight - app.storeMarginY)
    drawImage(app.sprites['home'][0], app.canvasWidth + 2 * app.storeMarginX + app.sprites['start'][1][0], app.height - app.storeItemHeight - app.storeMarginY)
    
    for i in range(9):
        # coordinates
        x = app.canvasWidth + 0.5 * app.storeMarginX + (i // 5) * (app.storeItemWidth +  app.storeMarginX)
        y = app.storeMarginY + (i % 5) * (app.storeItemHeight + app.storeMarginY)
        
        # sprites
        background = app.sprites['background']
        sprite = app.sprites[app.towerOrd[i].getStoreSprite()]
        
        # towers
        drawImage(background[0], x, y, width = background[1][0], height = background[1][1])
        drawImage(sprite[0], x + (background[1][0] - sprite[1][0]) // 2, y,
                  width = sprite[1][0], height = sprite[1][1])
        
        # cost
        drawLabel(f'${app.towerOrd[i].cost}', x + background[1][0] // 2, y + background[1][1],
                  size = 25, fill = 'white', bold = True, align = 'bottom')
    
    # name label
    x = app.canvasWidth + (app.width - app.canvasWidth) // 2
    y = app.storeMarginY + 5 * (app.storeItemHeight + app.storeMarginY) +  + (app.sprites['button'][1][1] // 2)
    drawImage(app.sprites['button'][0], x, y, align = 'center')
    drawLabel(app.printLabel, x, y, size = 18, fill = 'white')

def drawLabels(app):
    fontSize = app.cell // 2
    cWidth = 0.5 * app.cell
    hWidth = 3.5 * app.cell 
    wWidth = app.canvasWidth - 0.5 * app.cell
    
    # health points, coins and waves
    drawImage(app.sprites['hp'][0], cWidth, 0.5 * app.cell, align = 'center')
    drawImage(app.sprites['coins'][0], hWidth, 0.5 * app.cell, align = 'center')
    drawLabel(f'{app.hp}', 2 * cWidth, app.cell * 0.5, size = fontSize, bold = True, align = 'left', fill = 'white')
    drawLabel(f'{app.coins}', hWidth + cWidth, app.cell * 0.5, size = fontSize, bold = True, align = 'left', fill = 'white')
    drawLabel(f'Wave {app.level}/10', wWidth, app.cell * 0.5, size = fontSize, bold = True, align = 'right', fill = 'white')

def drawBloons(app):
    for i in app.bloons:
        drawImage(i.image, i.x, i.y, width = i.width, height = i.height, align = 'center')

        if i.glued:
            drawImage(app.sprites['gluecover'][0], i.x, i.y, align = 'center')

        if i.speed == 0:
            drawImage(app.sprites['icecover'][0], i.x, i.y, align = 'center')

def drawTowers(app):
    # tower preview if clicked on store
    if app.storePlacement:
        x, y = app.storePlacement[0], app.storePlacement[1]

        drawImage(app.storeSelection.getSprite(), x, y, align = 'center')
        
        # position validity
        if isValidPlacement(app, x, y):
            drawCircle(x, y, app.storeSelection.radius, fill = None, border = 'black')
        else:
            drawCircle(x, y, app.storeSelection.radius, fill = 'red', border = 'black', opacity = 50)
    
    # placed towers
    for i in app.towers:
        drawImage(i.sprite, i.x, i.y, width = i.width, height = i.height, align = 'center', rotateAngle = i.angle)
        
        if debug or i == app.towerSelection:
            drawCircle(i.x, i.y, type(i).radius, fill = None, border = 'black')

            drawCircle(i.x, i.y - 2 * i.spriteRadius, i.spriteRadius // 3, fill = 'green')
            drawLabel('$', i.x, i.y - 2 * i.spriteRadius, fill = 'white')

            if debug and type(i) == TackShooter:
                    for x, y in i.shoots:
                        drawLine(i.x, i.y, x, y)

def drawHomeScreen(app):
    # wallpaper
    drawImage(app.sprites['homescreen'][0], 0, 0)
    drawRect(0, 0, app.width, app.height, fill = 'grey', opacity = 50) # mask

    # logo
    bloon = app.sprites['bloons']
    drawImage(bloon[0], app.width * 0.5, app.height * 0.25, align = 'center')
    drawLabel('112 Edition!', (app.width * 0.5) + bloon[1][0] // 2, app.height * 0.25 + bloon[1][1] // 3, 
              size = 25, fill = 'pink', border = 'black', borderWidth = 0.5, rotateAngle = -45, bold = True)
    
    # buttons
    bg = app.sprites['storebg']
    level1 = app.sprites['meadows']
    level2 = app.sprites['corn']
    level3 = app.sprites['road']
    
    # level 1
    drawImage(bg[0], app.width * 0.2, app.height * 0.75, width = 0.22 * app.width, height = 0.17 * app.width, align = 'center')
    drawImage(level1[0], app.width * 0.2, app.height * 0.75, width = 0.2 * app.width, height = 0.15 * app.width, align = 'center')
    
    # level 2
    drawImage(bg[0], app.width * 0.5, app.height * 0.75, width = 0.22 * app.width, height = 0.17 * app.width, align = 'center')
    drawImage(level2[0], app.width * 0.5, app.height * 0.75, width = 0.2 * app.width, height = 0.15 * app.width, align = 'center')

    # level 3
    drawImage(bg[0], app.width * 0.8, app.height * 0.75, width = 0.22 * app.width, height = 0.17 * app.width, align = 'center')
    drawImage(level3[0], app.width * 0.8, app.height * 0.75, width = 0.2 * app.width, height = 0.15 * app.width, align = 'center')

def drawGameOver(app):
    if app.hp > 0:
        drawImage(app.sprites['win'][0], app.width // 2, app.height // 2, align = 'center')
    else:
        drawImage(app.sprites['defeat'][0], app.width // 2, app.height // 2, align = 'center')

def redrawAll(app):
    if app.drawHomeScreen:
        drawHomeScreen(app)
    else:
        drawCanvas(app)
        
        if debug:
            for i in app.hitbox:
                drawRect(i[0], i[1], i[2], i[3], fill = 'lightBlue', borderWidth = 1)

        drawTowers(app)
        drawLabels(app)
        drawStore(app)

        for i in app.bullets:
            drawImage(i.sprite, i.x, i.y, width = i.width, height = i.height, align = 'center', rotateAngle = i.angle)
            
        if checkGameState(app):
            drawBloons(app)
        else:
            drawGameOver(app)

runApp(width = 1280, height = 720)
   