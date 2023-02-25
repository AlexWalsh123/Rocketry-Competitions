from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
import sys
import random
import numpy as np
import pyqtgraph as pg
import serial


class PlotData:
    def __init__(self, parent, title, xlabel, ylabel, Row, Col):
        self.plot = parent.addPlot(title=title, row=Row, col=Col)
        self.data_line = self.plot.plot(pen='y')
        self.title = title


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Defines title and location of multiple plots to be populated onto the display

        self.plotPlace = [('logRX', 0, 0), ('logRY', 1, 0),
                          ('logRZ', 1, 1), ('Altitude', 1, 2)]

        # Defines intial data, Probably want to find a way to not initilise this as zero
        self.rocketData = {

            'logTime': [0],
            'logRX': [0],
            'logRY': [0],
            'logRZ': [0],
            'Altitude': [0]

        }

        # Creates the window to display the plots on
        self.graphWidget = pg.GraphicsView()
        self.l = pg.GraphicsLayout(border=(100, 100, 100))
        self.graphWidget.setCentralItem(self.l)

        # Generate plots and create plot objects to be minipulated
        self.plots = []

        for i, (key, Row, Col) in enumerate(self.plotPlace):
            self.plots.append(PlotData(self.l, key, 'Time', key, Row, Col))

        #Adds a label item to the window 

        ##TODO Try and fix the formatting of this to align left and look a little better

        self.labelTop = self.l.addLabel(row=0, col=1, rowspan=1, colspan=2)
        self.labelTop.setText(
            "<div style='text-align: left;'>Data</div>")

        # Starts window time and tells it how often to call data update function
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(1000)  # update every second

    def update_plot_data(self):
        print("DATA Update")

        # Insert new data Add here data ingest

        self.rocketData['logTime'].append(
            self.rocketData['logTime'][-1] + 1)  # Delete This assignment
        self.rocketData['logRX'].append(random.randint(0, 10))
        self.rocketData['logRY'].append(random.randint(0, 10))
        self.rocketData['logRZ'].append(random.randint(0, 10))
        self.rocketData['Altitude'].append(random.randint(0, 10))

        # Update Plots to correct data using plot objects that exist in list

        for plot in self.plots:
            plot.data_line.setData(
                self.rocketData['logTime'], self.rocketData.get(plot.title))

        #Update Label Values

        latestLogRX = "Rocket X position: %s" % self.rocketData['logRX'][-1]
        latestLogRY = "Rocket Y position: %s" % self.rocketData['logRY'][-1]
        latestLogRZ = "Rocket Z position: %s" % self.rocketData['logRZ'][-1]

        text = ["========================================================",latestLogRX, latestLogRY, latestLogRZ,"========================================================"]

        text = "<br>".join(text)

        self.labelTop.setText(text)


class DataIngest:
    def __init__(self):

        self.data = {}  # data fed to grapher
        self.ports = ['COM4', 'COM5']  # Serial ports to grab data from
        self.activePorts = []  # which of these ports are actually open

    def checkPorts(self):

        for i, key in enumerate(self.ports):

            try:

                self.key = serial.Serial(key,  15500000, timeout=None)
                self.key.flush()

            except:

                print("Nothing on port", key)

    def decode(self):

        for i, key in enumerate(self.activePorts):

            data = self.key.flush().readline().decode('utf-8').strip("\r\n")
            self.data.update({key, data})


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setCentralWidget(window.graphWidget)
    window.show()
    sys.exit(app.exec())
