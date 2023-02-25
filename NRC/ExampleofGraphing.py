from pyqtgraph.Qt import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import random
import time
import pandas as pd
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        #self.Title = QtWidgets.QTitle()
        self.graphWidget.setTitle("")

        self.graphWidget.showGrid(x=True, y=True)

        self.graphWidget.autoRange

        self.x = list(range(100))  # 100 time points
        self.y = [random.randint(0,100) for _ in range(100)]  # 100 data points

        # plot data: x, y values
        self.data_line = self.graphWidget.plot(self.x, self.y)

        self.timer = QtCore.QTimer()
        #self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        #framerate counter
        self.lastupdate = time.time()
        self.fps = 0.
        
    def update_plot_data(self):

        data = pd.read_csv('data.csv')
        self.x = data['x_value']
        self.y = data['total_1']

        self.data_line.setData(self.x, self.y)

        #framerate counter
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.graphWidget.setTitle(tx)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    #main.setCentralWidget(main.graphWidget)
    main.show()
    main.setWindowTitle("Ground Control")
    sys.exit(app.exec())


if __name__ == '__main__':
    main()