from enum import auto
from genericpath import exists
from sqlite3 import Row
from typing import Counter
from cv2 import mean
from matplotlib.pyplot import title
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import time
import pandas as pd
import serial
from PIL import Image
from numpy import asarray
import numpy as np
# from FlightComputerSimulator import Simulator
from scipy.spatial.transform import Rotation as Rot  # used for rotations
from collections import defaultdict


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):  # CONFIGURE WINDOW

        # Can initulise the Ui with either the simulator or the COM ports, it will defualt to com ports inless Simulator = True

        super(MainWindow, self).__init__()

        if 'Simulator' in kwargs:
            if kwargs.get('Simulator'):
                print("Simultating Flight")
                # self.sim = Simulator()
        else:
            # checks for the existance of data feeds on the COM ports (TO DO Change this to
            #  a function that can iterate thtrough all of the COM ports,
            # (recall there is a way to check which ones are connected to))
            try:
                self.ser1 = serial.Serial("COM4",  15500000, timeout=None)
                self.ser1.flush()

            except:

                print("Nothing on port 1")

            try:
                self.ser2 = serial.Serial("COM5",  15500000, timeout=None)
                self.ser2.flush()

            except:

                print("Nothing on port 2")

        # Sets the GUI start time
        self.startTime = time.time()

        # Opens a jpg if it exists (TO DO make this into a try and except like above, also maybe fold into a function for better objectivity)
        if (exists("test.jpg")):
            im = Image.open("test.jpg")
            im = im.rotate(180)
            # When importing an image, the way pyqtgraph represnts the image is weird so just transpose and rotate :(
            im = im.transpose(Image.FLIP_LEFT_RIGHT)
            image = asarray(im)  # make this update when you get the new image

        # Define all data types

        self.receiving = False
        self.counterRec = 0
        self.transData = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # Rocket Data

        self.rocketData = {'logRRRSI': [], 'logRGPS1': [], 'logRGPS2': [
        ], 'logRX': [], 'logRY': [], 'logRZ': [], 'logAlt': [], 'logTime': []}

        # RQ1,RQ2,RQ3,RQ4 = "", "","",""

        # RGPS1,RGPS2 = "",""

        # RRRSI = ""

        # RXR,RYR,RZR = "","",""

        # dataRRRSI = []
        # dataRGPS1 = []
        # dataRGPS2 = []
        # dataRXR = []
        # dataRYR = []
        # dataRZR = []

        # init graphing window
        self.graphWidget = pg.GraphicsView()
        self.l = pg.GraphicsLayout(border=(100, 100, 100))
        self.graphWidget.setCentralItem(self.l)

        text = """
        Telemetry Links<br>
        1. Strength , connected?<br>
        2. Strength , connected?.
        """

        # Top Box

        # can create a layout which we can the arrange labels and buttons into. :)
        self.layoutTop = self.l.addLayout(row=0, col=3)

        self.labelTop = self.l.addLabel(text)
        self.layoutTop.addItem(self.labelTop, rowspan=3, col=0)

        # needx a proxy to get the button to work
        proxy = QtWidgets.QGraphicsProxyWidget()
        button = QtWidgets.QPushButton('Reset Graphs')
        button.setStyleSheet(
            "QPushButton { background-color: grey }" "QPushButton:pressed { background-color: red }")
        button.clicked.connect(Reset)

        proxy.setWidget(button)

        self.layoutTop.addItem(proxy, row=1, col=1)

        # Bottom Box

        self.labelBottom = self.l.addLabel(text, row=3, col=1, colspan=4)

        # image

        self.img = pg.ImageItem(axisOrder='row-major')

        self.img.setImage(image)

        self.vb = self.l.addViewBox(
            lockAspect=True, row=1, col=1, rowspan=2, colspan=4)
        self.vb.addItem(self.img)
        self.vb.autoRange()

        # Initiate Graphs
        if True:
            # Graph 1
            plots = [("plot 1", 0, 0), ("plot 2", 0, 1), ("plot 3", 0, 4),         ("plot 4", 0, 5), ("plot 5", 1, 0),
                     ("plot 6", 1, 5),         ("plot 7", 2, 0), ("plot 8", 2, 5), ("plot 9", 3, 0),         ("plot 10", 3, 5)]

            for i, (title, row, col) in enumerate(plots):
                self.p = self.l.addPlot(title=title, row=row, col=col)
                self.p.showGrid(x=True, y=True)
                self.p.setDownsampling(ds=True, auto=True, mode='mean')

                self.p.x = []
                self.p.y = []

                self.p.data_line = self.p.plot(self.p.x, self.p.y)

        # Update Graphs
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # framerate counter
        self.lastupdate = time.time()
        self.fps = 0.

    def update_plot_data(self):  # UPDATE DATA

        clock = time.time() - self.startTime  # finds the current time from the start

        if hasattr(self, 'sim'):
            # runs the simulation to find the data needed
            OutputData = self.sim.RunSim(clock)
        else:
            OutputData = Decode()

        # Append data to dictionary

        self.rocketData.setdefault('logRRRSI', []).append(10)
        self.rocketData.setdefault('logRGPS1', []).append(OutputData['GPS'][0])
        self.rocketData.setdefault('logRGPS2', []).append(OutputData['GPS'][1])
        rotation = Rot.from_quat(OutputData['QUAT'])
        self.rocketData.setdefault('logRX', []).append(
            rotation.as_euler('xyz', degrees=True)[0])
        self.rocketData.setdefault('logRY', []).append(
            rotation.as_euler('xyz', degrees=True)[1])
        self.rocketData.setdefault('logRZ', []).append(
            rotation.as_euler('xyz', degrees=True)[2])
        self.rocketData.setdefault('logTime', []).append(clock)

        # set data values live
        self.p1.data_line.setData(
            self.rocketData['logTime'], self.rocketData.get('logRX'))
        self.p2.data_line.setData(
            self.rocketData['logTime'], self.rocketData.get('logRY'))
        self.p5.data_line.setData(
            self.rocketData['logTime'], self.rocketData.get('logRZ'))
        self.p7.data_line.setData(self.rocketData.get(
            'logRGPS2'), self.rocketData.get('logRGPS1'))
        self.p9.data_line.setData(self.rocketData['logTime'], self.p1.y)
        self.p6.data_line.setData(self.rocketData['logTime'], self.p1.y)
        self.p3.data_line.setData(self.rocketData['logTime'], self.p1.y)
        self.p8.data_line.setData(self.rocketData['logTime'], self.p1.y)
        self.p4.data_line.setData(self.rocketData['logTime'], self.p1.y)
        self.p10.data_line.setData(self.rocketData['logTime'], self.p1.y)

        # framerate counter
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps)

        text = """
        Telemetry Links<br>
        1. Strength , connected?<br>
        2. Strength , connected?<br>
        """

        # Updates Text

        text = text + tx
        text = text + str(0)
        self.labelTop.setText(text)


def Reset():  # RESET COM PORTS

    global ser1, startTime, dataRGPS1, dataRGPS2, dataRRRSI, dataRXR, dataRYR, dataRZR, timeData

    try:
        ser1 = {}
        ser1 = serial.Serial("COM4", 15500000, timeout=None)
        ser1.flushInput()

        startTime = time.time()

        dataRRRSI = []
        dataRGPS1 = []
        dataRGPS2 = []
        dataRXR = []
        dataRYR = []
        dataRZR = []
        timeData = []

    except:

        print("Nothing on this port")


def Decode(serialPort, DataDictionary):  # DECODE DATA

    serialPort.flush()
    msg = serialPort.readline()
    msg = msg.decode('utf-8')  # removes the endbits and the b''
    msg = msg.strip("\r\n")

    if (str(msg) == "Transmition"):

        counterRec = -1
        receiving = True
        # print("starting")

    while (receiving == True and counterRec != 9):

        serialPort.flush()
        msg = serialPort.readline()
        msg = msg.decode('utf-8')  # removes the endbits and the b''
        msg = msg.strip("\r\n")
        counterRec += 1

        # print(counterRec)

        # transData[int(counterRec)] = float(msg)

# RQ1 = transData[6]
# RQ2 = transData[1]
# RQ3 = transData[2]
# RQ4 = transData[3]
# RGPS1 = transData[4]
# RGPS2 = transData[5]
# RRRSI = transData[0]
# roll_x, roll_y, roll_z = euler_from_quaternion(RQ1, RQ2, RQ3, RQ4)
# RXR = roll_x
# RYR = roll_y
# RZR = roll_z
