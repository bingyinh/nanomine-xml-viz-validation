import eventBasedAnimation
from viz_valid import xml2dataDict
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk
import glob
import pickle

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)


class VizValidation(eventBasedAnimation.Animation):
    def onInit(self):
        # reset dataDict.pkl
        with open('dataDict.pkl','wb') as f:
            pickle.dump(('',{},True), f)
        # define windows and pages
        self.windowTitle = "Viz Validation"
        self.Pages = [Instruction(), SelectDir(), Viz()]
        self.currentPage = 0
        self.buttonpos()
    def onMouse(self, event):
        self.Pages[self.currentPage].Mouse(event.x, event.y)
        # Click on Next (Instruction, SelectDir)
        if self.currentPage == 0 or self.currentPage == 1:
            if (self.nextx-20 <= event.x <= self.nextx+20 and
                self.nexty-10 <= event.y <= self.nexty+10):
                self.currentPage += 1
        # Click on Back (SelectDir)
        if self.currentPage == 1:
            if (self.backx-20 <= event.x <= self.backx+20 and
                self.backy-10 <= event.y <= self.backy+10):
                self.currentPage -= 1
        # Click on Back (Viz)
        if self.currentPage == 2:
            if (self.backx-20 <= event.x <= self.backx+20 and
                self.backyviz-10 <= event.y <= self.backyviz+10):
                self.currentPage -= 1
        
    def onKey(self, event):
        self.Pages[self.currentPage].KeyFn(event.keysym)
    def onDraw(self, canvas):
        self.Pages[self.currentPage].Draw(canvas, self.step)
    # def onQuit(self):
    #     if len(self.dataDict) > 0:
    #         self.PILim.close()
    def buttonpos(self):
        self.nextx = self.width - 30
        self.nexty = self.height - 30
        self.backx = self.width - self.nextx
        self.backy = self.nexty
        self.backyviz = 30

class Page(object):
    def __init__(self, dataDict):
        self.width = 850
        self.height = 600
        self.colorsettings()
        self.buttonpos()
        self.readDataDict()
        self.xmldir = ''
        self.xmllist = []
    def Mouse(self, mouseX, mouseY):
        pass
    def Key(self, keystroke):
        pass
    # method for text drawing
    def drawText(self, canvas):
        for piece in self.textInPage:
            text, font, posx, posy = piece[0], piece[1], piece[2], piece[3]
            if (piece[4] == True): # change color when mouse moves onto button
                canvas.create_text(posx, posy, text = text,
                                   fill = self.btnColor,
                                   font = "Arial " + str(font),
                                   activefill = self.btnActive)
            else: # static color when mouse moves onto non-button text
                canvas.create_text(posx, posy, text = text,
                                   fill = self.btnColor,
                                   font = "Arial " + str(font), width = 650)
    def Draw(self, canvas, step):
        sfm = 10 # safe margin
        canvas.create_rectangle(-sfm, -sfm, self.width+sfm, self.height+sfm,
                                fill = self.bgd)
        self.drawText(canvas)

    def colorsettings(self):
        self.btnColor = rgbString(111, 195, 223) # color theme of Tron Legacy
        self.btnShading1 = rgbString(66, 176, 213) # color theme of Tron Legacy
        self.btnShading2 = rgbString(31, 113, 139) # color theme of Tron Legacy
        self.btnShading3 = rgbString(16, 60, 73) # color theme of Tron Legacy
        self.btnActive = rgbString(230, 255, 255)# color theme of Tron Legacy
        self.bgd = rgbString(12, 20, 31) # background color
        self.btnXbgd = self.btnColor
        self.btnXcolor = self.bgd
        self.btnYbgd = self.btnColor
        self.btnYcolor = self.bgd
        
    def buttonpos(self):
        self.nextx = self.width - 30
        self.nexty = self.height - 30
        self.backx = self.width - self.nextx
        self.backy = self.nexty
        self.backyviz = 30
    # read pickle file for dataDict
    def readDataDict(self):
        with open('dataDict.pkl','rb') as f:
            (self.imageDir, self.dataDict, self.showClick) = pickle.load(f)
    # write pickle file for dataDict
    def writeDataDict(self, imageDir, dataDict, showClick):
        with open('dataDict.pkl','wb') as f:
            pickle.dump((imageDir, dataDict, showClick), f)

    # generate all of the default plot
    def generateAll(self):
        graph_num = 0
        for graph in self.dataDict:
            plt.figure(graph_num)
            for sample in self.dataDict[graph]['data']:
                legend = sample
                x = self.dataDict[graph]['data'][sample]['x']
                y = self.dataDict[graph]['data'][sample]['y']
                plt.plot(x, y, label = legend)
            # end of the loop
            plt.title(graph, fontsize = 10)
            plt.xlabel(self.dataDict[graph]['xlabel'])
            plt.ylabel(self.dataDict[graph]['ylabel'])
            leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
            leg.get_frame().set_alpha(0.5)
            filename = self.imageDir + "%d.jpg" %(graph_num)
            plt.savefig(filename)
            graph_num += 1
        currentFilename = self.imageDir + "0.jpg"
        self.PILim = Image.open(currentFilename)
        self.PILphoto = ImageTk.PhotoImage(image = self.PILim)

class Instruction(Page):
    def __init__(self):
        super(Instruction, self).__init__({})
        self.textInPage = [("Viz Validation", 40, self.width/2, 100, False),
                           ("Next", 15, self.nextx, self.nexty, True)]
        self.instxt = '''Instruction: \n
        This tool is developed for boosting the NanoMine manual validation \
efficiency. With this tool, you can visually check the spectra data in \
the xml files and change log-scale on both axes with one click. The \
next page will ask you to select the directory that contains the xml \
files you would like to check on. Then you can click on "Next" to \
navigate to the visualization page. On the visualization page, you \
will see two arrow buttons and two "Switch" buttons. Click on the two \
arrows on each side of the plotting window can switch among the plots. \
The other option is to press "left" key and "right" key. The \
"Switch X" button and the "Switch Y" button are clickable to change \
the log-scale option of the corresponding axis. The other option is to \
press "x" key and "y" key.'''
    def Draw(self, canvas, step):
        super(Instruction, self).Draw(canvas, step)
        canvas.create_text(self.width/2, self.height/2+20, text = self.instxt,
                           fill = self.btnColor,
                           font = "Arial 15", width = self.width-150)
    def Mouse(self, mouseX, mouseY):
        pass
    def KeyFn(self, keystroke):
        pass

class SelectDir(Page):
    def __init__(self):
        super(SelectDir, self).__init__({})
        self.textInPage = [("Please select the directory:", 15, self.width/4,
                            self.height/6, False),
                           ("Next", 15, self.nextx, self.nexty, True),
                           ("Back", 15, self.backx, self.backy, True)]
        # position of the directory box
        self.dirBoxx0 = self.width/6
        self.dirBoxx1 = self.width/6*4
        self.dirBoxy0 = self.height/4
        self.dirBoxy1 = self.dirBoxy0+30
        # position of the Browse... button
        self.browsex0 = self.width/6*4
        self.browsex1 = self.width/6*5
        self.browsey0 = self.dirBoxy0
        self.browsey1 = self.dirBoxy1
        # # check whether an xmldir exists
        # if not hasattr(self, 'xmldir'):
        #     self.xmldir = ''
        # # check whether an xmllist exists
        # if not hasattr(self, 'xmllist'):
        #     self.xmllist = []
    # need to additionally draw directory box, browse button, browse text,
    # and xml list
    def Draw(self, canvas, step):
        super(SelectDir, self).Draw(canvas, step)
        canvas.create_rectangle(self.dirBoxx0, self.dirBoxy0, self.dirBoxx1,
                                self.dirBoxy1, outline = self.btnColor)
        canvas.create_rectangle(self.browsex0, self.browsey0, self.browsex1,
                                self.browsey1, outline = self.btnColor,
                                fill = self.bgd, activefill = self.btnActive)
        canvas.create_text((self.browsex0+self.browsex1)/2,
                           (self.browsey0+self.browsey1)/2, text = "Browse...",
                            fill = self.btnColor, font = "Arial 15")
        canvas.create_text(self.dirBoxx0+2, self.dirBoxy0+4, anchor = NW,
                           text = self.xmldir, fill = self.btnColor,
                           font = "Arial 15")
        self.drawxmlList(canvas)
    # draw the xml list
    def drawxmlList(self, canvas):
        counter = 0
        xmlListstr = ''
        while counter < len(self.xmllist) and counter < 10:
            xmlListstr += self.xmllist[counter] + '\n'
            counter += 1
        if counter < len(self.xmllist):
            xmlListstr += '...'
        canvas.create_text(self.dirBoxx0, self.dirBoxy1+10, anchor = NW,
                           fill = self.btnColor, text = xmlListstr,
                           font = "Arial 15")
    # need to configure the browse button and the next button
    def Mouse(self, mouseX, mouseY):
        if (self.browsex0 <= mouseX <= self.browsex1 and
            self.browsey0 <= mouseY <= self.browsey1):
            self.getxmlDir() # call the askdirectory() function

    # open the askdirectory() dialog window, get the dataDict, call other fn's
    def getxmlDir(self):
        self.xmldir = tkFileDialog.askdirectory()
        if self.xmldir != '':
            self.dataDict = xml2dataDict(self.xmldir)
            self.getxmlList()
            self.makeOutputDir()
            self.writeDataDict(self.imageDir, self.dataDict, True)
    # get the list of xml files in self.xmldir
    def getxmlList(self):
        self.xmllist = [] # init
        xmls = glob.glob(self.xmldir + '/*.xml')
        for xml in xmls:
            self.xmllist.append(xml.split('\\')[-1])
    # make the vvOutput folder in the self.xmldir
    def makeOutputDir(self):
        if not os.path.exists(self.xmldir+'/vvOutput'):
            os.mkdir(self.xmldir+'/vvOutput') # image files will be saved here
        self.imageDir = self.xmldir+'/vvOutput/'
        self.generateAll()
    def KeyFn(self, keystroke):
        pass

class Viz(Page):
    def __init__(self):
        super(Viz, self).__init__({})
        self.textInPage = [("Back", 15, self.backx, self.backyviz, True)]
        self.currentGraph = 0
        self.xlog = False
        self.ylog = False
        self.imageWidth = 640
        self.imageHeight = 480
        self.vizButtonPos()
        self.PILim = Image.new('RGB', (self.imageWidth, self.imageHeight),
                               (255, 255, 255))
        self.PILphoto = ImageTk.PhotoImage(image = self.PILim)
        self.showClick = True # flag for "Click here ..." message
        self.maxGraph = 0

    def Draw(self, canvas, step):
        super(Viz, self).Draw(canvas, step)
        self.drawBoard(canvas)
        self.readDataDict()
        # check whether an dataDict exists
        if len(self.dataDict) > 0:
            self.maxGraph = len(self.dataDict) - 1

    def drawBoard(self, canvas):
        self.drawButton(canvas)
        if not self.showClick:
            self.drawPlot(canvas)
        self.drawSign(canvas)

    # everytime self.xlog or self.ylog is changed, call generateCurrent(self)
    def generateCurrent(self):
        self.showClick = False
        graph = self.dataDict.keys()[self.currentGraph]
        plt.figure()
        for sample in self.dataDict[graph]['data']:
            legend = sample
            x = self.dataDict[graph]['data'][sample]['x']
            y = self.dataDict[graph]['data'][sample]['y']
            if self.xlog:
                if self.ylog:
                    plt.loglog(x, y, label = legend, basex = 10)
                else:
                    plt.semilogx(x, y, label = legend)
            else:
                if self.ylog:
                    plt.semilogy(x, y, label = legend)
                else:
                    plt.plot(x, y, label = legend)
            # end of the loop
        plt.title(graph, fontsize = 10)
        plt.xlabel(self.dataDict[graph]['xlabel'])
        plt.ylabel(self.dataDict[graph]['ylabel'])
        leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
        leg.get_frame().set_alpha(0.5)
        filename = self.imageDir + "%d.jpg" %(self.currentGraph)
        plt.savefig(filename)
        self.PILim.close()
        self.PILim = Image.open(filename)
        self.PILphoto = ImageTk.PhotoImage(image = self.PILim)
        self.logColorUpdate()

    # draw the signs for log-scale on and off
    def drawSign(self, canvas):
        # x axis
        canvas.create_text(self.width - 200, self.height - 30,
                           text = 'X Axis Log-scale: ',
                          anchor = NW, font = "Arial 15 bold", fill = self.btnColor)
        if self.xlog:
            canvas.create_text(self.width - 35, self.height - 30, anchor = NW,
                           text = 'On', font = "Arial 15 bold", fill = "green")
        else:
            canvas.create_text(self.width - 35, self.height - 30, anchor = NW,
                           text = 'Off', font = "Arial 15 bold", fill = "red")
        # y axis
        canvas.create_text(5, self.height - 30, text = 'Y Axis Log-scale: ',
                          anchor = NW, font = "Arial 15 bold", fill = self.btnColor)
        if self.ylog:
            canvas.create_text(170, self.height - 30, anchor = NW,
                           text = 'On', font = "Arial 15 bold", fill = "green")
        else:
            canvas.create_text(170, self.height - 30, anchor = NW,
                           text = 'Off', font = "Arial 15 bold", fill = "red")
        # page number
        if self.maxGraph == 0:
            pagetxt = 'Page 0 of 0'
        else:
            pagetxt = 'Page %d of %d' %(self.currentGraph+1, self.maxGraph+1)
        canvas.create_text(self.width/2,
                           self.imageHeight+(self.height-self.imageHeight)/2+30,
                           text = pagetxt, font = "Arial 15 bold",
                           fill = self.btnColor)
        # in the middle of the page
        if self.showClick:
            canvas.create_text(self.width/2, self.height/2,
                               text="Click here to show images",
                               font = "Arial 20", fill = self.btnActive)

    def drawPlot(self, canvas):
        # get the back
        canvas.create_image(self.width/2, self.height/2, image = self.PILphoto)

    def drawButton(self, canvas):
        # x button
        canvas.create_rectangle(self.xlogx0, self.xlogy0, self.xlogx1, self.xlogy1,
                                fill = self.btnXbgd)
        canvas.create_text((self.xlogx0 + self.xlogx1) / 2,
                           (self.xlogy0 + self.xlogy1) / 2, anchor = CENTER,
                           fill = self.btnXcolor, text = "Switch X", font = "Arial 10 bold")
        # y button
        canvas.create_rectangle(self.ylogx0, self.ylogy0, self.ylogx1, self.ylogy1,
                                fill = self.btnYbgd)
        canvas.create_text((self.ylogx0 + self.ylogx1) / 2,
                           (self.ylogy0 + self.ylogy1) / 2, anchor = CENTER,
                           fill = self.btnYcolor, text = "Switch Y", font = "Arial 10 bold")
        # Image button
        for arrow in self.arrowPos:
            self.drawArrow(canvas, *arrow)

    def drawArrow(self, canvas, direction, x0, y0, x1, y1):
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
                                outline = self.btnShading1,
                                outlinestipple = 'gray50')
        canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 8,
                                outline = self.btnShading2,
                                outlinestipple = 'gray25')
        canvas.create_rectangle(x0, y0, x1, y1, fill = None, width = 10,
                                outline = self.btnShading3,
                                outlinestipple = 'gray12')
        canvas.create_rectangle(x0, y0, x1, y1, fill = self.bgd,
                                outline = self.btnColor,
                                activefill = self.btnActive)
        canvas.create_polygon(tri1x, tri1y, tri2x, tri2y, tri3x, tri3y,
                              fill = self.bgd, outline = self.btnColor,
                              activefill = self.btnActive)

    def vizButtonPos(self):
        self.ylogx0 = 21
        self.ylogy0 = self.height - 55
        self.ylogx1 = self.ylogx0 + 100
        self.ylogy1 = self.ylogy0 + 20
        self.xlogx1 = self.width - 21
        self.xlogy0 = self.height - 55
        self.xlogy1 = self.xlogy0 + 20
        self.xlogx0 = self.xlogx1 - 100
        self.arrowPos = [("left",(self.width-self.imageWidth)/2-30, 
                                 (self.height-self.imageHeight)/2,
                                 (self.width-self.imageWidth)/2-5,
                                 (self.height-self.imageHeight)/2+self.imageHeight),
                         ("right",(self.width-self.imageWidth)/2+self.imageWidth+5, 
                                 (self.height-self.imageHeight)/2,
                                 (self.width-self.imageWidth)/2+self.imageWidth+30,
                                 (self.height-self.imageHeight)/2+self.imageHeight)]

    def Mouse(self, mouseX, mouseY):
        # x log-scale button
        if (self.xlogx0 <= mouseX <= self.xlogx1 and
            self.xlogy0 <= mouseY <= self.xlogy1):
            self.xlog = not self.xlog
            self.generateCurrent()
        # y log-scale button
        if (self.ylogx0 <= mouseX <= self.ylogx1 and
            self.ylogy0 <= mouseY <= self.ylogy1):
            self.ylog = not self.ylog
            self.generateCurrent()
        # left arrow
        arrowL = self.arrowPos[0]
        (_, arrowLx0, arrowLy0, arrowLx1, arrowLy1) = arrowL
        if (arrowLx0 <= mouseX <= arrowLx1 and
            arrowLy0 <= mouseY <= arrowLy1 and self.currentGraph > 0):
            self.currentGraph -= 1
            self.generateCurrent()
        # right arrow
        arrowR = self.arrowPos[1]
        (_, arrowRx0, arrowRy0, arrowRx1, arrowRy1) = arrowR
        if (arrowRx0 <= mouseX <= arrowRx1 and
            arrowRy0 <= mouseY <= arrowRy1 and self.currentGraph < self.maxGraph):
            self.currentGraph += 1
            self.generateCurrent()
        # image window
        if ((self.width-self.imageWidth)/2 <= mouseX <= (self.width+self.imageWidth)/2 and
            (self.height-self.imageHeight)/2 <= mouseY <= (self.height+self.imageHeight)/2 and
            self.showClick):
            self.showClick = False
            self.writeDataDict(self.imageDir, self.dataDict, self.showClick)
            self.generateCurrent()

    def logColorUpdate(self):
        if self.xlog:
            self.btnXbgd = self.bgd
            self.btnXcolor = self.btnActive
        else:
            self.btnXbgd = self.btnColor
            self.btnXcolor = self.bgd
        if self.ylog:
            self.btnYbgd = self.bgd
            self.btnYcolor = self.btnActive
        else:
            self.btnYbgd = self.btnColor
            self.btnYcolor = self.bgd

    def KeyFn(self, keystroke):
        if keystroke == "Left" and self.currentGraph > 0:
            self.currentGraph -= 1
            self.generateCurrent()
        if keystroke == "Right" and self.currentGraph < self.maxGraph:
            self.currentGraph += 1
            self.generateCurrent()
        if keystroke == "x":
            self.xlog = not self.xlog
            self.generateCurrent()
        if keystroke == "y":
            self.ylog = not self.ylog
            self.generateCurrent()

VizValidation(width=850, height=600).run()
