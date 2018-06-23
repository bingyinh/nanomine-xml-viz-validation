import eventBasedAnimation
from viz_valid import xml2dataDict
from Tkinter import *
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def vizInitFn(data):
    data.dataDict = xml2dataDict('')
    data.windowTitle = "Viz Validation"
    data.currentGraph = 0
    data.maxGraph = len(data.dataDict) - 1
    data.xlog = False
    data.ylog = False
    if not os.path.exists('vvOutput'):
        os.mkdir('vvOutput') # image files will be saved here
    data.imageDir = 'vvOutput/'
    data.imageWidth = 640
    data.imageHeight = 480
    data.PILim = Image.new('RGB', (data.imageWidth, data.imageHeight),
                           (255, 255, 255))
    data.PILphoto = ImageTk.PhotoImage(image = data.PILim)
    colorsettings(data)
    buttonpos(data)
    generateAll(data)


def colorsettings(data):
    data.btnColor = rgbString(111, 195, 223) # color theme of Tron Legacy
    data.btnShading1 = rgbString(66, 176, 213) # color theme of Tron Legacy
    data.btnShading2 = rgbString(31, 113, 139) # color theme of Tron Legacy
    data.btnShading3 = rgbString(16, 60, 73) # color theme of Tron Legacy
    data.btnActive = rgbString(230, 255, 255)# color theme of Tron Legacy
    data.bgd = rgbString(12, 20, 31) # background color
    data.btnXbgd = data.btnColor
    data.btnXcolor = data.bgd
    data.btnYbgd = data.btnColor
    data.btnYcolor = data.bgd

def buttonpos(data):
    data.ylogx0 = 21
    data.ylogy0 = data.height - 55
    data.ylogx1 = data.ylogx0 + 100
    data.ylogy1 = data.ylogy0 + 20
    data.xlogx1 = data.width - 21
    data.xlogy0 = data.height - 55
    data.xlogy1 = data.xlogy0 + 20
    data.xlogx0 = data.xlogx1 - 100
    data.arrowPos = [("left",(data.width-data.imageWidth)/2-30, 
                             (data.height-data.imageHeight)/2,
                             (data.width-data.imageWidth)/2-5,
                             (data.height-data.imageHeight)/2+data.imageHeight),
                     ("right",(data.width-data.imageWidth)/2+data.imageWidth+5, 
                             (data.height-data.imageHeight)/2,
                             (data.width-data.imageWidth)/2+data.imageWidth+30,
                             (data.height-data.imageHeight)/2+data.imageHeight)]
# default plot
def generateAll(data):
    graph_num = 0
    for graph in data.dataDict:
        plt.figure(graph_num)
        for sample in data.dataDict[graph]['data']:
            legend = sample
            x = data.dataDict[graph]['data'][sample]['x']
            y = data.dataDict[graph]['data'][sample]['y']
            plt.plot(x, y, label = legend)
        # end of the loop
        plt.title(graph, fontsize = 10)
        plt.xlabel(data.dataDict[graph]['xlabel'])
        plt.ylabel(data.dataDict[graph]['ylabel'])
        leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
        leg.get_frame().set_alpha(0.5)
        filename = data.imageDir + "%d.jpg" %(graph_num)
        plt.savefig(filename)
        graph_num += 1
    currentFilename = data.imageDir + "%d.jpg" %(data.currentGraph)
    data.PILim.close()
    data.PILim = Image.open(currentFilename)
    data.PILphoto = ImageTk.PhotoImage(image = data.PILim)

def vizDrawFn(canvas, data):
    drawBoard(canvas, data)
    
def drawBoard(canvas, data):
    safemargin = 10
    canvas.create_rectangle(- safemargin, - safemargin, data.width + safemargin,
                            data.height + safemargin, fill = data.bgd)
    drawButton(canvas, data)
    drawPlot(canvas, data)
    drawSign(canvas, data)

# everytime data.xlog or data.ylog is changed, call generateCurrent(data)
def generateCurrent(data):
    graph = data.dataDict.keys()[data.currentGraph]
    plt.figure()
    for sample in data.dataDict[graph]['data']:
        legend = sample
        x = data.dataDict[graph]['data'][sample]['x']
        y = data.dataDict[graph]['data'][sample]['y']
        if data.xlog:
            if data.ylog:
                plt.loglog(x, y, label = legend, basex = 10)
            else:
                plt.semilogx(x, y, label = legend)
        else:
            if data.ylog:
                plt.semilogy(x, y, label = legend)
            else:
                plt.plot(x, y, label = legend)
        # end of the loop
    plt.title(graph, fontsize = 10)
    plt.xlabel(data.dataDict[graph]['xlabel'])
    plt.ylabel(data.dataDict[graph]['ylabel'])
    leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
    leg.get_frame().set_alpha(0.5)
    filename = data.imageDir + "%d.jpg" %(data.currentGraph)
    plt.savefig(filename)
    data.PILim.close()
    data.PILim = Image.open(filename)
    data.PILphoto = ImageTk.PhotoImage(image = data.PILim)
    logColorUpdate(data)

# draw the signs for log-scale on and off
def drawSign(canvas, data):
    # x axis
    canvas.create_text(data.width - 200, data.height - 30,
                       text = 'X Axis Log-scale: ',
                      anchor = NW, font = "Arial 15 bold", fill = data.btnColor)
    if data.xlog:
        canvas.create_text(data.width - 35, data.height - 30, anchor = NW,
                       text = 'On', font = "Arial 15 bold", fill = "green")
    else:
        canvas.create_text(data.width - 35, data.height - 30, anchor = NW,
                       text = 'Off', font = "Arial 15 bold", fill = "red")
    # y axis
    canvas.create_text(5, data.height - 30, text = 'Y Axis Log-scale: ',
                      anchor = NW, font = "Arial 15 bold", fill = data.btnColor)
    if data.ylog:
        canvas.create_text(170, data.height - 30, anchor = NW,
                       text = 'On', font = "Arial 15 bold", fill = "green")
    else:
        canvas.create_text(170, data.height - 30, anchor = NW,
                       text = 'Off', font = "Arial 15 bold", fill = "red")
    # page number
    pagetxt = 'Page %d of %d' %(data.currentGraph+1, data.maxGraph+1)
    canvas.create_text(data.width/2,
                       data.imageHeight+(data.height-data.imageHeight)/2+30,
                       text = pagetxt, font = "Arial 15 bold",
                       fill = data.btnColor)

def drawPlot(canvas, data):
    # get the back
    canvas.create_image(data.width/2, data.height/2, image = data.PILphoto)

def drawButton(canvas, data):
    # x button
    canvas.create_rectangle(data.xlogx0, data.xlogy0, data.xlogx1, data.xlogy1,
                            fill = data.btnXbgd)
    canvas.create_text((data.xlogx0 + data.xlogx1) / 2,
                       (data.xlogy0 + data.xlogy1) / 2, anchor = CENTER,
                       fill = data.btnXcolor, text = "Switch X", font = "Arial 10 bold")
    # y button
    canvas.create_rectangle(data.ylogx0, data.ylogy0, data.ylogx1, data.ylogy1,
                            fill = data.btnYbgd)
    canvas.create_text((data.ylogx0 + data.ylogx1) / 2,
                       (data.ylogy0 + data.ylogy1) / 2, anchor = CENTER,
                       fill = data.btnYcolor, text = "Switch Y", font = "Arial 10 bold")
    # Image button
    for arrow in data.arrowPos:
        drawArrow(data, canvas, *arrow)

def drawArrow(data, canvas, direction, x0, y0, x1, y1):
    ratio = 0.25
    if (direction == "left"):
        tri1x, tri1y = x0 + ratio * (x1 - x0), (y0 + y1) * 0.5
        tri2x, tri2y = x1 - ratio * (x1 - x0), y0 + ratio * (y1 - y0)
        tri3x, tri3y = x1 - ratio * (x1 - x0), y1 - ratio * (y1 - y0)
    elif (direction == "right"):
        tri1x, tri1y = x1 - ratio * (x1 - x0), (y0 + y1) * 0.5
        tri2x, tri2y = x0 + ratio * (x1 - x0), y0 + ratio * (y1 - y0)
        tri3x, tri3y = x0 + ratio * (x1 - x0), y1 - ratio * (y1 - y0)
    # shading idea comes from 112 course notes
    canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 6,
                            outline = data.btnShading1,
                            outlinestipple = 'gray50')
    canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 8,
                            outline = data.btnShading2,
                            outlinestipple = 'gray25')
    canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 10,
                            outline = data.btnShading3,
                            outlinestipple = 'gray12')
    canvas.create_rectangle(x0, y0, x1, y1, fill = data.bgd,
                            outline = data.btnColor,
                            activefill = data.btnActive)
    canvas.create_polygon(tri1x, tri1y, tri2x, tri2y, tri3x, tri3y,
                          fill = data.bgd, outline = data.btnColor,
                          activefill = data.btnActive)

def onMouseFn(event, data):
    # x log-scale button
    if (data.xlogx0 <= event.x <= data.xlogx1 and
        data.xlogy0 <= event.y <= data.xlogy1):
        data.xlog = not data.xlog
        generateCurrent(data)
    # y log-scale button
    if (data.ylogx0 <= event.x <= data.ylogx1 and
        data.ylogy0 <= event.y <= data.ylogy1):
        data.ylog = not data.ylog
        generateCurrent(data)
    # left arrow
    arrowL = data.arrowPos[0]
    (_, arrowLx0, arrowLy0, arrowLx1, arrowLy1) = arrowL
    if (arrowLx0 <= event.x <= arrowLx1 and
        arrowLy0 <= event.y <= arrowLy1 and data.currentGraph > 0):
        data.currentGraph -= 1
        generateCurrent(data)
    # right arrow
    arrowR = data.arrowPos[1]
    (_, arrowRx0, arrowRy0, arrowRx1, arrowRy1) = arrowR
    if (arrowRx0 <= event.x <= arrowRx1 and
        arrowRy0 <= event.y <= arrowRy1 and data.currentGraph < data.maxGraph):
        data.currentGraph += 1
        generateCurrent(data)

def logColorUpdate(data):
    if data.xlog:
        data.btnXbgd = data.bgd
        data.btnXcolor = data.btnActive
    else:
        data.btnXbgd = data.btnColor
        data.btnXcolor = data.bgd
    if data.ylog:
        data.btnYbgd = data.bgd
        data.btnYcolor = data.btnActive
    else:
        data.btnYbgd = data.btnColor
        data.btnYcolor = data.bgd

def onKeyFn(event, data):
    if event.keysym == "Left" and data.currentGraph > 0:
        data.currentGraph -= 1
        generateCurrent(data)
    if event.keysym == "Right" and data.currentGraph < data.maxGraph:
        data.currentGraph += 1
        generateCurrent(data)
    if event.keysym == "x":
        data.xlog = not data.xlog
        generateCurrent(data)
    if event.keysym == "y":
        data.ylog = not data.ylog
        generateCurrent(data)

def runVizValidation():
    eventBasedAnimation.run(
    initFn = vizInitFn,
    drawFn = vizDrawFn,
    mouseFn = onMouseFn,
    keyFn = onKeyFn,
    width=850, height=600
    )

runVizValidation()
