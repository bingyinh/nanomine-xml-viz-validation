import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import glob
import numpy as np
import collections

def xml2dataDict(xmldir):
    dataDict = collections.OrderedDict()
    # load xml files
    xmlfiles = glob.glob(xmldir + '/*.xml')
    # extract data
    for xml in xmlfiles:
        dataDict = xmlDataExt(xml, dataDict)
    return dataDict


def xml2graph():
    dataDict = collections.OrderedDict()
    # load xml files
    xmlfiles = glob.glob('*.xml')
    # extract data
    for xml in xmlfiles:
        dataDict = xmlDataExt(xml, dataDict)
    # plot
    graph_num = 0
    for graph in dataDict:
        plt.figure(graph_num)
        for sample in dataDict[graph]['data']:
            legend = sample
            x = dataDict[graph]['data'][sample]['x']
            y = dataDict[graph]['data'][sample]['y']
            if dataDict[graph]['xlog']:
                if dataDict[graph]['ylog']:
                    plt.loglog(x, y, label = legend, basex = 10)
                else:
                    plt.semilogx(x, y, label = legend)
            else:
                if dataDict[graph]['ylog']:
                    plt.semilogy(x, y, label = legend)
                else:
                    plt.plot(x, y, label = legend)
        # end of the loop
        plt.title(graph)
        plt.xlabel(dataDict[graph]['xlabel'])
        plt.ylabel(dataDict[graph]['ylabel'])
        leg = plt.legend(loc='best', ncol=2, mode="expand", shadow=True, fancybox=True)
        leg.get_frame().set_alpha(0.5)
        graph_num += 1
    plt.show()

def xmlDataExt(xml, dataDict):
    # extract the sampleID
    sampleID = xml.split('\\')[-1].split('_')[1]
    # read the xml as a tree
    tree = ET.parse(xml)
    # find all parent elements with child "data"
    temp_parents = tree.findall('.//data/..')
    # eliminate all elements whose tag is "data"
    for par in temp_parents:
        if not par.tag == 'data':
            # traverse through all par, if description element exists use
            # description as key, otherwise, use the tag of the parent element
            # as key.
            parKey = par.tag
            Des = par.find('.//Description')
            if Des is not None:
                parKey = Des.text
            des = par.find('.//description')
            if des is not None:
                parKey += '-' + des.text
            alx = par.find('.//xName') # AxisLabel/xName
            alxtxt = alx.text if alx is not None else ''
            aly = par.find('.//yName') # AxisLabel/yName
            alytxt = aly.text if aly is not None else ''
            parKey += '\n' + alytxt + ' vs. ' + alxtxt
            # extract data
            data = par.find('.//headers/..')
            if data is None:
                continue
            # extract headers
            xlabel = data.find('.//headers/column[@id="0"]').text
            ylabel = data.find('.//headers/column[@id="1"]').text
            # init
            xraw = []
            yraw = []
            xlog = False
            ylog = False
            # fill in xraw and yraw
            for i in data.findall('.//rows/row/column[@id="0"]'):
                xraw.append(float(i.text))
            for i in data.findall('.//rows/row/column[@id="1"]'):
                yraw.append(float(i.text))
            # zip xraw and yraw and sort
            coords = zip(xraw,yraw)
            coords.sort(key=lambda x:x[0])
            # unzip x and y
            (x,y) = zip(*coords)
            # log scale or not
            if abs(np.log10(abs(x[-1]/x[0])))>=4:
                xlog = True
            if abs(np.log10(abs(y[-1]/y[0])))>=4 or np.log10(max(y)) >= 4:
                ylog = True
            # initialize dataDict
            if parKey not in dataDict:
                dataDict[parKey] = {'xlog':False,'ylog':False,'xlabel':'',
                                    'ylabel':'','data':{sampleID:{}}}
            if sampleID not in dataDict[parKey]['data']:
                dataDict[parKey]['data'][sampleID] = {}
            # update dataDict
            dataDict[parKey]['xlog'] = dataDict[parKey]['xlog'] or xlog
            dataDict[parKey]['ylog'] = dataDict[parKey]['ylog'] or ylog
            dataDict[parKey]['xlabel'] = xlabel
            dataDict[parKey]['ylabel'] = ylabel
            # print parKey
            # print sampleID
            assert(len(dataDict[parKey]['data'][sampleID]) == 0)
            dataDict[parKey]['data'][sampleID]['x'] = np.array(x)
            dataDict[parKey]['data'][sampleID]['y'] = np.array(y)
    # end of the loop
    return dataDict

if __name__ == '__main__':
    raw_input('Make sure you put all the xml files into the same directory as this script. Press Enter to continue.')
    xml2graph()
