# nanomine-xml-viz-validation
Visualization validation tool for spectra data in xml files in NanoMine. This tool is developed specifically for boosting the NanoMine manual validation efficiency. To run the tool, install Python 2.7 and the required packages, move the xmls to the folder that contains the tool, and run viz_valid_GUI.py. Please always put eventBasedAnimation.pyc and viz_valid.py in the same folder as viz_valid_GUI.py. eventBasedAnimation V1.10 is downloaded from Carnegie Mellon University 15-112 Professor David Kosbie's website (http://www.kosbie.net/cmu/spring-15/15-112/notes/eventBasedAnimation.py).

Code base: Python 2.7

Package requirement:

    matplotlib==2.1.2
    Pillow==5.1.0
    numpy==1.14.0
    Tkinter               (Python standard library)
    glob                  (Python standard library)
    collections           (Python standard library)
    xml.etree.ElementTree (Python standard library)
    os                    (Python standard library)
    pickle                (Python standard library)

Version 1.0

Click on the two arrows on each side of the plotting window can switch among the plots. The other option is to press "left" key and "right" key. The "Switch X" button and the "Switch Y" button are clickable to change the log-scale option of the corresponding axis. The other option is to press "x" key and "y" key.

About to come: 1) an instruction page 2) an xml directory selection page

Version 2.0

An instruction page and an xml directory selection page are added. The selected xml directory will be displayed with a list of filenames of xml files in that directory on the screen. A dataDict.pkl file will be created externally as a cache file.