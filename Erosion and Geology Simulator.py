#################################################
# 

#################################################

import math, copy, os
import random
##import pygame
from cmu_112_graphics import *
#pygame.init()


#################################################


# Non Specific Helper functions
#################################################


def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def nextIndexInList(L,i):

    return (i+1) % len(L)

def randomWithDecimals(start,end,decimals):
    num = (random.random() * (end - start) - start)
    return  setDecimals(num,decimals)

def setDecimals(num,decimals):
    return math.floor(num * (10**(decimals))) / (10**(decimals ))

def largestVal(L):
    largest = 0
    for row in L:
        for num in row:
            if num > largest:
                largest = int(num + 1)
    return largest

def listFlipper(L):
    newList = [[0]*len(L) for i in range(len(L[0]))]
    for i in range(len(newList)-1,-1,-1):
        for j in range(len(newList[0])):
            newList[i][j] = L[j][len(newList)-i-1]
    return newList

#################################################
# Class's
#################################################

#### Isometric mountanin object

class isome(object):

    def __init__(self):
        self.rows = 5
        self.cols = 5
        self.noise = 1
        self.peakHeight = 5
        self.orientation = 0
        self.heightMap = [[0]*self.cols for i in range(self.rows)]
        self.liquidMap = [[0]*self.cols for i in range(self.rows)]
        self.acidity = 1
        self.water = True
        self.liquidSize = 1
        self.liquidColor = 'blue'
        self.genStyle = 0
        self.genStyles = 4
       
    def genMountian(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.heightMap = [[0]*self.cols for i in range(self.rows)]
        self.liquidMap = [[0]*self.cols for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if self.genStyle == 0:
                    #####  tunable parameters and better generation
                    inc1 = randomWithDecimals(0,self.rows/10,3)
                    height = abs(10*math.cos((i+inc1)*math.pi/self.rows*2 +randomWithDecimals(0,5,4)))
                    inc2 = randomWithDecimals(0,self.rows/30,3)
                    height = abs(3*math.cos((i+inc2)/self.rows*math.pi*6))
                    height -= (i**2)/self.rows/2
                    height += abs(3*math.sin(j/self.cols*math.pi*6))
                    inc4 = randomWithDecimals(0,self.cols/40,3)
                    height += abs(10*math.sin((j+inc4)*math.pi/self.cols*2)) + 20
                    height *= (j+1)/self.rows
                    height += 5 + 30/self.rows*randomWithDecimals(0,1,3)
                    height = setDecimals(height,4)
                    if height > .1:
                        self.heightMap[i][j] = height
                    else:
                        self.heightMap[i][j] = .1 +.001*(j+i)
                elif self.genStyle == 2:
                    inc1 = randomWithDecimals(0,self.rows/10,3)
                    height = abs(10*math.cos((i)*math.pi/self.rows*2))
                    height -= (i**2)/self.rows/2
                    height += abs(10*math.sin((j)*math.pi/self.cols*2)) + 20
                    height *= (j+1)/self.rows
                    height += 5 + randomWithDecimals(0,1,4)
                    height = setDecimals(height,4)\
                    
                    if height > .1:
                        self.heightMap[i][j] = height
                    else:
                        self.heightMap[i][j] = .1 +.001*(j+i)
                elif self.genStyle == 1:
                    inc1 = randomWithDecimals(0,self.rows/10,3)
                    height = abs(10*math.cos((i+inc1)*math.pi/self.rows*2 +randomWithDecimals(0,5,4)))
                    inc2 = randomWithDecimals(0,self.rows/30,3)
                    height = abs(3*math.cos((i+inc2)/self.rows*math.pi*6))
                    height -= (i**2)/self.rows/2
                    height += abs(3*math.sin(j/self.cols*math.pi*6))
                    inc4 = randomWithDecimals(0,self.cols/40,3)
                    height *= (j+1)/self.rows
                    height += 5 + 30/self.rows*randomWithDecimals(0,1,3)
                    height = setDecimals(height,4)
                    if height > .1:
                        self.heightMap[i][j] = height
                    else:
                        self.heightMap[i][j] = .1 +.001*(j+i)
                elif self.genStyle == 3:
                    height = 0
                    if (i > self.rows/4 and  i < self.rows*3/4 and
                        j > self.rows/4 and j < self.rows*3/4):
                        height = abs(3*math.cos((i)*math.pi/self.rows*2))
                        height += abs(3*math.cos((j)*math.pi/self.rows*2))
                        height += abs(.25*math.cos((j)*math.pi/self.rows*10))
                        height += randomWithDecimals(0,.25,4)
                    if height > .1:
                        self.heightMap[i][j] = height
                    else:
                        self.heightMap[i][j] = .1
        self.peakHeight = largestVal(self.heightMap)
        self.emptyLiquid()

    def flipMountian(self):
        self.heightMap = listFlipper(self.heightMap)
        self.liquidMap = listFlipper(self.liquidMap)

    def emptyLiquid(self):
        self.liquidMap = [[0]*self.cols for i in range(self.rows)]

    def toggleLiquid(self):
        self.water = not self.water
        self.setLiquidColor()
        self.emptyLiquid()

    def toggleGenStyle(self):
        self.genStyle = (self.genStyle + 1) % self.genStyles
        self.genMountian(self.rows,self.cols)

    def setLiquidColor(self):
        if self.water:
            self.liquidColor = rgbString(   
                              100 - int(self.acidity/10 * 80),
                              170 - int(self.acidity/10 * 160),
                              200 - int(self.acidity/10 * 100))
        else:
            self.liquidColor = rgbString(   
                              249 - int(self.acidity/10 * 60),
                              75 - int(self.acidity/10 * 20),
                              75 - int(self.acidity/10 * 20))

    def setAcidity(self,acidity):
        self.acidity = acidity
        self.setLiquidColor()
        self.emptyLiquid()

    def setLiquidSize(self,size):
        self.liquidSize = size
        self.emptyLiquid()

    def putLiquid(self,row,col):
        i = row
        j = col
        if not self.genStyle == 3:
            self.liquidMap[row][col] += self.liquidSize
            return None
        elif (i > self.rows/4 and  i < self.rows*3/4 and
            j > self.rows/4 and j < self.rows*3/4):
                self.liquidMap[row][col] += self.liquidSize

    def flowLocation(self,row,col):
        lowestVal = self.heightMap[row][col]
        lowestTupe = (row,col)
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if (0 <= row + i <= self.rows - 1 and 
                    0 <= col + j <= self.cols - 1):
                    height = self.heightMap[row+i][col+j]
                    if lowestVal > height:
                        lowestVal = height
                        lowestTupe = (row + i,col + j)
        return lowestTupe

    def erodePath(self,tuple,nextLoca):
        heightOld = self.heightMap[tuple[0]][tuple[1]]
        heightNew = self.heightMap[nextLoca[0]][nextLoca[1]]
        if self.water:
            dif = heightOld - heightNew
            drops = self.liquidMap[tuple[0]][tuple[1]]
            if drops > 20: 
                drops = 20
            change = 3 *  dif * 1/10 * self.acidity * 1/60 * drops
            if change > 5/7*dif: 
                change = 5/7*dif
            eroded = heightOld - change
            self.heightMap[tuple[0]][tuple[1]] = eroded
        else:
            lava = self.liquidMap[tuple[0]][tuple[1]] * 1/70 * self.acidity
            if lava > .2:
                lava = .2
            possible = self.heightMap[tuple[0]][tuple[1]] + lava
            if possible < self.peakHeight - .3 :
                self.heightMap[tuple[0]][tuple[1]] += lava
        
    def iterLiquid(self):
        nextState = [[0]*self.cols for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                liquid = self.liquidMap[i][j]
                if liquid > 0:
                    curLoca = (i,j)
                    nextLoca = self.flowLocation(i,j)
                    if not nextLoca == curLoca:
                        if self.water:
                            nextState[nextLoca[0]][nextLoca[1]] += liquid*.95
                        else:
                            nextState[nextLoca[0]][nextLoca[1]] += liquid*.8
                        self.erodePath(curLoca,nextLoca)
                    else: 
                        self.heightMap[curLoca[0]][curLoca[1]] += (.01 * 
                            self.liquidMap[curLoca[0]][curLoca[1]])
        return nextState


#### Dot class

class Dot(object):
    
    def __init__(self,cx,cy,radius,color):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.color = color
    
    def getRadius(self):
        return self.radius

    def changeCy(self,cy):
        self.cy = cy

    def changeCx(self,cx):
        self.cy = cx

    def changeRadius(self,radius):
        self.radius = radius

#################### Button Class

class button(object):
    
    def __init__(self,cx,cy,scaleX,scaleY,text,function,color = 'white'):
        self.cx = cx
        self.cy = cy 
        self.width = scaleX
        self.height = scaleY
        self.text = text
        self.function = function
        self.color = color

####### Button functions

def clickedWithin(app,button,location):
    cx,cy = button.cx * app.width ,button.cy * app.height
    radX,radY = button.width * app.height, button.height * app.height
    if (cx - radX <= location[0] and cx + radX/2 >= location[0] and
        cy - radY <= location[1] and cy + radY >= location[1]):
        return True
    return False

def runSplash(app):
    #pygame.mixer.Sound.stop(app.rain)
    app.screen = 'splash'

def runLab(app):
    app.screen = 'lab'
    #if app.baseIso.water:
      #  pygame.mixer.Sound.stop(app.lava)
      #  pygame.mixer.Sound.play(app.rain)
    #else:
       # pygame.mixer.Sound.play(app.lava)
       # pygame.mixer.Sound.stop(app.rain)

def runTerraform(app):
    #pygame.mixer.Sound.stop(app.rain)
    app.screen = 'terraform'
    resetLiquid(app)

def runWorld(app):
    #pygame.mixer.Sound.stop(app.rain)
    app.screen = 'world'

def runSave(app):
   # pygame.mixer.Sound.stop(app.rain)
    app.screen = 'save'

def toggleHelp(app):
    app.help = not app.help

def helpHome(app):
    runSplash(app)
    toggleHelp(app)

def runScreenCap(app):
    app.screen = 'scWindow'
    
def liquidify(app):
    #if app.baseIso.water:
     #   pygame.mixer.Sound.stop(app.lava)
     #   pygame.mixer.Sound.play(app.rain)
    #else:
      #  pygame.mixer.Sound.play(app.lava)
      #  pygame.mixer.Sound.stop(app.rain)
    
    for i in range(app.baseIso.rows):
        for j in range(app.baseIso.cols):
            app.baseIso.putLiquid(i,j)

def increaseMountianSize(app):
    print('size is ',app.baseIso.rows)
    if app.baseIso.rows < 80:
        app.baseIso.genMountian(app.baseIso.rows + 5,app.baseIso.cols + 5)
    app.peakHeight = app.baseIso.peakHeight

def decreaseMountianSize(app):
    if app.baseIso.rows > 10:
        app.baseIso.genMountian(app.baseIso.rows - 5,app.baseIso.cols - 5)
    app.peakHeight = app.baseIso.peakHeight

def toggleGen(app):
    app.baseIso.toggleGenStyle()
    resetMountian(app)

def increaseAcidity(app):
    if app.baseIso.acidity < 10:
        app.baseIso.setAcidity(app.baseIso.acidity + 1)

def decreaseAcidity(app):
    if app.baseIso.acidity >2:
        app.baseIso.setAcidity(app.baseIso.acidity - 1)

def increaseLiquidSize(app):
    if app.baseIso.liquidSize < 3:
        app.baseIso.setLiquidSize(app.baseIso.liquidSize + .25)

def decreaseLiquidSize(app):
    if app.baseIso.liquidSize >.5:
        app.baseIso.setLiquidSize(app.baseIso.liquidSize - .25)

def toggleLiquid(app):
    app.baseIso.toggleLiquid()
    #if app.baseIso.water:
       # pygame.mixer.Sound.stop(app.lava)
       # pygame.mixer.Sound.play(app.rain)
    #else:
        #pygame.mixer.Sound.play(app.lava)
       # pygame.mixer.Sound.stop(app.rain)

def saveTheCap(app):
    app.saveSnapshot()
    
def resetMountian(app):
    app.baseIso.genMountian(app.baseIso.rows,app.baseIso.cols)
    app.peakHeight = app.baseIso.peakHeight

def rotateMountian(app):
    app.baseIso.flipMountian()

def resetLiquid(app):
    app.baseIso.emptyLiquid()

def setHollowView(app):
    app.drawType = 'circles'

def setBlockView(app):
    app.drawType = 'blocks'

def changeView(app):
    if app.drawType == 'circles':
        app.drawType = 'blocks'
    elif app.drawType == 'blocks':
        app.drawType = 'polygons'
    else:
        app.drawType = 'circles'

def incColorStyle(app):
    app.colorStyle = (app.colorStyle + 1) % len(app.cStyles)

def decColorStyle(app):
    app.colorStyle = (app.colorStyle + len(app.cStyles) - 1) % len(app.cStyles)

def getColor(app,height,top):
    style = app.colorStyle
    red = app.cStyles[style][0][0] + int(height/top * app.cStyles[style][0][1])
    green = app.cStyles[style][1][0] + int(height/top * app.cStyles[style][1][1])
    blue = app.cStyles[style][2][0] + int(height/top * app.cStyles[style][2][1])
    return rgbString(red,green,blue)

#################################################
# Major code
#################################################


#### App

def appStarted(app):

    #### App modes
    app.screen = 'splash'  
    app.help = False
    app.helpMsg = """
    Hi, welcome to the Erosion and Geology Simulator
    
    The purpose of this app is to:
       Create your own generative mountain
       Fine tune your own liquid that will weather it
       Simulate erosion/geology on the mountain
       Save your work as art
    
    This app is window scaleable :)
    
    

    """
    app.buttons = dict()
    app.buttons['help'] = [button(7/10-1/40,1/4+1/40,1/15,1/20,'',toggleHelp,'red')]
    app.buttons['help'] += [button(3/10+2/40,1/4+1/40,1/7,1/20,'Home',helpHome,'white')]

    ### Splash 
    app.buttons['splash'] = [button(1/2,9/10,1/3,1/15,'START',runTerraform)]
    
    ## Lab
    app.buttons['lab'] = [button(9/10,1*1/8,1/5,1/20,'Water/Lava',toggleLiquid)]
    app.buttons['lab'] += [button(9/10,1*2/8,1/5,1/20,'Increase Size',increaseLiquidSize)]
    app.buttons['lab'] += [button(9/10,1*3/8,1/5,1/20,'Decrease Size',decreaseLiquidSize)]
    app.buttons['lab'] += [button(9/10,1/2,1/5,1/20,'Increase Acidity',increaseAcidity)]
    app.buttons['lab'] += [button(9/10,1*5/8,1/5,1/20,'Decrease Acidity',decreaseAcidity)]
    app.buttons['lab'] += [button(9/10,1*7/8,1/5,1/20,'Enter Simulation',runWorld)]
    app.buttons['lab'] += [button(9/10,1*6/8,1/5,1/20,'Edit Mountain',runTerraform)]

    ### Terraform
    #app.buttons['terraform'] = [button(1*1/5,1*1/8,1/5,1/20,'Edit Liquid',runLab)]
    app.buttons['terraform'] = [button(9/10,1/2,1/5,1/20,'Increase Fidelity',increaseMountianSize)]
    app.buttons['terraform'] += [button(9/10,1*5/8,1/5,1/20,'Decrease Fidelity',decreaseMountianSize)]
    app.buttons['terraform'] += [button(9/10,1*6/8,1/5,1/20,'Edit Liquid',runLab)]
    app.buttons['terraform'] += [button(9/10,1*3/8,1/5,1/20,'View Style',changeView)]
    app.buttons['terraform'] += [button(9/10,1*1/8,1/5,1/20,'Regenerate',resetMountian)]
    app.buttons['terraform'] += [button(9/10,1*2/8,1/5,1/20,'Generation Style',toggleGen)]
    app.buttons['terraform'] += [button(9/10,1*7/8,1/5,1/20,'Enter Simulation',runWorld)]
    app.buttons['terraform'] += [button(8/20,19/20,1/8,1/20,'<- Color',incColorStyle)]
    app.buttons['terraform'] += [button(12/20,19/20,1/8,1/20,'Color ->',decColorStyle)]

    ### World
    app.buttons['world'] = [button(9/10,9/20,2/15,1/30,'Lava/ Water',toggleLiquid)]
    app.buttons['world'] += [button(9/10,1/2,1/5,1/20,'Press for liquid',liquidify)]
    app.buttons['world'] += [button(9/10,5/8+1/40,2/15,1/30,'View Style',changeView)]
    app.buttons['world'] += [button(9/10,5/8-1/40,2/15,1/30,'Rotate View',rotateMountian)]
    app.buttons['world'] += [button(9/10,1*6/8,1/5,1/20,'Save Mountain',runScreenCap)]
    app.buttons['world'] += [button(1*1/5,1*1/8,1/5,1/20,'Adjust Liquid',runLab)]
    app.buttons['world'] += [button(9/10,1*7/8,1/5,1/20,'Reset Mountain',resetMountian)]
    app.buttons['world'] += [button(1*2/5,1*1/8,1/5,1/20,'Edit Mountain',runTerraform)]

    ### End of simulation png stugff
    app.buttons['save'] = [button(1/2,1*2/8,1/5,1/20,'Save your Work',saveTheCap)]
    app.buttons['save'] += [button(1*3/4,1*2/8,1/5,1/20,'Return Simulation',runWorld)]
    for screen in app.buttons:
        if not screen == 'help':
            app.buttons[screen] += [button(1/15,1/20,1/8,1/20,'Help',toggleHelp)]

    ### Isome Object
    app.totalScale = 20
    app.yScale = 5
    app.baseIso = isome()
    app.baseIso.genMountian(100,100)
    app.baseIso.genMountian(50,50)
    app.convertedMap = [[(0,0)]*app.baseIso.cols for i in range(app.baseIso.rows)]
    app.totalScale = 200 / app.baseIso.rows
    app.printLiquid = [[[(0,0)]*app.baseIso.cols for i in range(app.baseIso.rows)]*5]
    app.baseIso.heightMap
    app.baseIso.setAcidity(5)
    app.drawTypes = ['blocks','hollow','polygons']
    app.drawType = app.drawTypes[2]
    app.style0 = ((160,-160),(0,200),(160,-160))
    app.style1 = ((0,160),(0,200),(160,-160))
    app.style2 = ((160,-160),(0,200),(0,160))
    app.style3 = ((160,-160),(230,-200),(160,-160))
    app.style4 = ((100,-80),(50,150),(160,-160))
    app.style5 = ((30,210),(20,220),(0,240))
    app.style6 = ((160,-160),(120,-90),(160,-160))
    app.style7 = ((240,-2),(240,-2),(240,-2))
    app.style8 = ((230,-160),(120,-90),(80,140))
    app.style9 = ((150,+80),(90,90),(160,-160))
    app.cStyles = [app.style0,app.style1,app.style2,app.style3,app.style4,
                    app.style5,app.style6,app.style7,app.style8,app.style9]
    app.colorStyle = 5
    app.peakHeight = app.baseIso.peakHeight
    app.labRain =[]

    ### Music sounds
   # app.music = pygame.mixer.Sound("Music.wav")
   # app.music.set_volume(100)
   # app.rain = pygame.mixer.Sound("ThunderRain.wav")
   # app.lava = pygame.mixer.Sound("Lava.wav")
   # app.buttonSound = pygame.mixer.Sound('Button.wav')
   # app.buttonSound.set_volume(1)
   # pygame.mixer.Sound.play(app.music,5)

    ## timeadjusters
    app.curRow = 0
    app.dots = []
    app.dotRadius = 50
    app.frame = 0
    app.maxFrames = 0
    app.timeSinceFrame = 0
    app.frameTime = 200
    app.curLoca = (-100,-100)
    app.pastLoca = (-100,-100)
    app.timerDelay = 100
    app.notAnNft = None

########## Interactivity

def mousePressed(app, event):
    location = (event.x,event.y)
    buttonClicked(app,location)
    
    
def keyPressed(app, event):
    pass

def buttonClicked(app,location):
    if app.screen in app.buttons:
        for button in app.buttons[app.screen]:
            ### check if button was clicked and run appropriate code
            if clickedWithin(app,button,location):
                #pygame.mixer.Sound.play(app.buttonSound)
                button.function(app)
                return None
    if app.help:
        for button in app.buttons['help']:
            if clickedWithin(app,button,location):
                #pygame.mixer.Sound.play(app.buttonSound)
                button.function(app)
                return None

def timerFired(app):
    app.timeSinceFrame += app.timerDelay
    if not app.timeSinceFrame >= app.frameTime:
        if(app.screen == 'lab'):
            for i in range(0,9):
                xLoca = int(randomWithDecimals(0,int(app.width),1))
                liquid = Dot(xLoca,-10,app.baseIso.liquidSize*10,app.baseIso.liquidColor)
                app.labRain.append(liquid)
            i = 0
            while i < len(app.labRain) - 1:
                cy = app.labRain[i].cy
                if  cy < app.height:
                    app.labRain[i].changeCy(cy + 40)
                    i += 1
                else:
                    app.labRain.remove(app.labRain[i])
    if app.screen == 'scWindow':
        snapshotImage = app.getSnapshot()
        app.notAnNft = app.scaleImage(snapshotImage, .5)
        runSave(app)
        return None
    app.timeSinceFrame = 0
    if app.screen == 'world':
       app.baseIso.liquidMap = app.baseIso.iterLiquid()

#### Draw shape functions    #######

def drawDot(app,canvas,cx,cy,radius,color = 'green'):
    x0,y0 = cx - radius,cy-radius
    x1,y1 = cx + radius,cy+radius
    canvas.create_oval(x0,y0,x1,y1,fill = color, outline = color)

def drawPoly(app,canvas,cx,cy,scaleX,scaleY,color):
    canvas.create_polygon(cx,cy-scaleY,cx-scaleX,cy,cx,cy+scaleY,cx+scaleX,cy,fill=color,outline="black", width=2)

def drawButton(app,canvas,button):
    cx,cy = button.cx * app.width ,button.cy * app.height
    radX,radY = button.width/2*app.height,button.height/2*app.height
    #font = f'Times {int(radX/6)} bold'
    font = f'Times {int(100/6)} '
    color = button.color
    canvas.create_rectangle(cx-radX,cy-radY,cx+radX,cy+radY,fill = color)
    canvas.create_text(cx,cy, text= button.text, font=font, fill = 'black')

####### Draws world Items

def drawBase(app,canvas,tx,ty,scale):
    for i in range(app.baseIso.rows):
        for j in range(app.baseIso.cols-1,-1,-1):
            cx,cy = tx + j*scale + i*scale , ty + (i*scale - j*scale)/5
            scaleX, scaleY = scale, scale / 5
            drawPoly(app,canvas,cx,cy,scaleX,scaleY,'grey')

def drawMountian(app,canvas,tx,ty,scale2):
    scale = app.width/4/(app.baseIso.rows) * (scale2 ** .5)
    ratio = app.yScale
    scaleX, scaleY = scale, scale / ratio
    topHeight = app.peakHeight
    #drawBase(app,canvas,tx,ty,scale)
    convertedMap = [[(0,0)]*app.baseIso.cols for i in range(app.baseIso.rows)]
    for i in range(app.baseIso.rows):
        for j in range(app.baseIso.cols-1,-1,-1):
        #for j in range(app.baseIso.cols):
            ## Center base of polygon on flat plane
            cx,cy = tx + j*scale + i*scale , ty + (i*scale - j*scale)/ratio
            actualHeight = app.baseIso.heightMap[i][j]
            height = app.height / 2 * (actualHeight/topHeight) 
            polyFill = getColor(app,actualHeight,topHeight)
            right = getColor(app,actualHeight,topHeight)
            left = getColor(app,actualHeight,topHeight)      
            top = getColor(app,actualHeight,topHeight)
            ctx = cx
            cty = cy-height
            centerTuple = (ctx,cty,cx,cy,height,right,left,top,polyFill)
            convertedMap[i][j] = centerTuple
    for i in range(app.baseIso.rows):
        for j in range(app.baseIso.cols-1,-1,-1):
            cx = convertedMap[i][j][2]
            cy = convertedMap[i][j][3]
            height = convertedMap[i][j][4]
            right  = convertedMap[i][j][5]
            left = convertedMap[i][j][6]
            top = convertedMap[i][j][7]
            if height <= 0:
                continue
            if app.drawType == 'blocks':
                #### left
                canvas.create_polygon(cx-scaleX,cy,cx,cy+scaleY,cx,cy - (height) , cx - scaleX , cy - height,fill=left,outline="black", width=2)
                ### right
                canvas.create_polygon(cx+scaleX,cy,cx,cy+scaleY,cx,cy - (height)  , cx + scaleX , cy- height,fill=right,outline="black", width=2)
                ### top
                drawPoly(app,canvas,cx,cy - height,scaleX,scaleY,top)
            elif app.drawType == 'circles':
                drawDot(app,canvas,cx,cy - height,2,'black')
            elif app.drawType == 'squares':
                print('squares bby')
            elif app.drawType == 'polygons':
                if i < app.baseIso.rows - 2 and j < app.baseIso.cols -2:
                    tx = convertedMap[i][j][0]
                    rx = convertedMap[i+1][j][0]
                    bx = convertedMap[i+1][j + 1][0]
                    lx = convertedMap[i][j+1][0]
                    ty = convertedMap[i][j][1]
                    ry = convertedMap[i+1][j][1]
                    by = convertedMap[i+1][j + 1][1]
                    ly = convertedMap[i][j+1][1]
                    canvas.create_polygon(tx,ty,rx,ry,bx,by,lx,ly,fill=convertedMap[i][j][8],outline="black", width=2)
            if app.baseIso.liquidMap[i][j] > 0:
                drawDot(app,canvas,cx,cy - height - 7*app.baseIso.liquidMap[i][j]**.25,7*app.baseIso.liquidMap[i][j]**.25 ,app.baseIso.liquidColor)

def drawTopDown(app,canvas,tx,ty,scale):
    width = scale
    smolWidth = width/app.baseIso.rows
    topHeight = app.peakHeight
    for i in range(app.baseIso.rows):
        for j in range(app.baseIso.cols):
            actualHeight = app.baseIso.heightMap[i][j]
            color = getColor(app,actualHeight,topHeight)
            canvas.create_rectangle(tx + smolWidth * (i),ty + smolWidth * (j),
                                    tx + smolWidth * (i + 1), ty + smolWidth * (j + 1),
                                    fill = color) 
            if app.baseIso.liquidMap[i][j] > 0:
                drawDot(app,canvas,tx + smolWidth * (i + .5),ty + smolWidth * (j + .5),2*app.baseIso.liquidMap[i][j]**.25 ,app.baseIso.liquidColor)
#######  

def drawSplash(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='#ADDFAD',width=app.width/40)
    font = f'Times {int(app.height/30)} bold'
    canvas.create_text(app.width/2, app.height/10, text='Mountain Erosion and Geology Simulator', font=font)
    drawMountian(app,canvas,app.width/15,app.height*4/5,3)

def drawLab(app,canvas):
    backColor = rgbString(200, 200, 200)
    canvas.create_rectangle(0,0,app.width,app.height,fill=backColor,width=app.width/40)
    font = f'Times {int(app.height/30)} bold'
    color = app.baseIso.liquidColor 
    rad = app.width/10*app.baseIso.liquidSize/1.5
    canvas.create_oval(app.width/2-rad,app.height/2 - rad,app.width/2+rad,app.height/2+rad, fill = color)
    for dot in app.labRain:
        drawDot(app,canvas,dot.cx,dot.cy,dot.radius,dot.color)
    canvas.create_text(app.width/2, app.height/10, text='Adjust liquid properties', font=font)

def drawTerraform(app,canvas):
    leftX,leftY = app.width/20,app.height*4/5
    canvas.create_rectangle(0,0,app.width,app.height,fill='#ADDFAD',width=app.width/40)
    font = f'Times {int(app.height/30)} bold'
    drawMountian(app,canvas,leftX,leftY,2.7)
    canvas.create_text(app.width/2, app.height/10, text='Adjust mountain generation', font=font)

def drawWorld(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='light yellow',width=app.width/40)
    color = app.baseIso.liquidColor 
    rad = app.width/100*app.baseIso.liquidSize/1.5
    canvas.create_oval(app.width*66/80-rad,app.height*9/20 - rad,app.width*66/80+rad,app.height*9/20+rad, fill = color)
    leftX,leftY = app.width/20,app.height*4/5
    drawMountian(app,canvas,leftX,leftY,2.7)
    flatTx,flatTy = app.width*7/10,app.height*1/20
    drawTopDown(app,canvas,flatTx,flatTy,app.height*3/10)

def drawSave(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='light blue',width=app.width/40)
    font = f'Times {int(app.height/20)} bold'
    canvas.create_text(app.width/2, app.height/10, text='Nice mountain!', font=font)
    if (app.notAnNft != None):
            canvas.create_image(app.width/2, app.height*3/5, image=ImageTk.PhotoImage(app.notAnNft))

def drawHelp(app,canvas):
    canvas.create_rectangle(app.width*3/10,app.height/4,app.width*7/10,app.height*3/4,fill='light grey',width=app.width/200)
    #canvas.create_rectangle(app.width*7/10-app.width/20,app.height/4,app.width*7/10,app.height/4+app.height/20,fill='red',width=app.width/200)
    font = f'Times {int(app.height/60)} bold'
    canvas.create_text(app.width/2, app.height/2, text=app.helpMsg, font=font)
    for button in app.buttons['help']:
        drawButton(app,canvas,button)

def drawScWindow(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='#ADDFAD',width=app.width/40)
    drawMountian(app,canvas,app.width/15,app.height*4/5,3)

################################

def redrawAll(app, canvas):

    if app.screen == 'world':
        drawWorld(app,canvas)
    elif app.screen == 'splash':
        drawSplash(app,canvas)
    elif app.screen == 'lab':
        drawLab(app,canvas)
    elif app.screen == 'save':
        drawSave(app,canvas)
    elif app.screen == 'terraform':
        drawTerraform(app,canvas)
    elif app.screen == 'scWindow':
        drawScWindow(app,canvas)
    if app.screen in app.buttons:
        for button in app.buttons[app.screen]:
            drawButton(app,canvas,button)
    if app.help:
        drawHelp(app,canvas)

def runMover():
    runApp(width=1500, height=1000)

#################################################
# Test Functions
#################################################

### Im good at these

#################################################
# Main
#################################################

def testAll():
    runMover()

def main():
    testAll()

if (__name__ == '__main__'):
    main()
