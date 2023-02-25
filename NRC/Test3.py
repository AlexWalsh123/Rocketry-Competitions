from sqlite3 import Row
from matplotlib.pyplot import title
from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import random
import time
import pandas as pd
import os
import serial
from PIL import Image
from numpy import asarray
import numpy as np

ser1 = serial.Serial("COM5",  15500000, timeout=None)

while True:

    ser1.flush()
    msg = ser1.readline()
    msg = msg.decode('utf-8') #removes the endbits and the b''
    print(msg)
    #print(msg[0:2])  # idetify with first position and the one after the last position.

    if(msg[0:2] == "AGGA"):

        Q1 = msg[2:10]
        Q2 = msg[10:18]
        Q3 = msg[18:26]
        Q4 = msg[26:34]

        print(Q1)
        print(Q2)
        print(Q3)
        print(Q4)

    



