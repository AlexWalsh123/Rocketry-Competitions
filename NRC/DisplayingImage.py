from tkinter import Y
from PIL import Image
from numpy import asarray
from pyqtgraph.Qt import QtCore, QtGui 
import pyqtgraph as pg
import numpy as np

im = Image.open("test.jpg")
im = im.rotate(180)
im = im.transpose(Image.FLIP_LEFT_RIGHT)     #When importing an image, the way pyqtgraph represnts the image is weird so just transpose and rotate :(
image = asarray(im)





win = pg.GraphicsLayoutWidget()
win.show()  ## show widget alone in its own window
win.setWindowTitle('pyqtgraph example: ImageItem')
view = win.addViewBox()

## lock the aspect ratio so pixels are always square
view.setAspectLocked(True)


## Create image item
img = pg.ImageItem(axisOrder='row-major')
view.addItem(img)

img.setImage(image)

pg.exec()