import tkinter as Tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import style
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


#setting graphing 
style.use('dark_background')


fig, ax = plt.subplots()

#reate window
root = Tk.Tk() #create root as a tkinter window
root.title("Ground Control")#rename the window
root.state('zoomed') # fullscreen window

Tk.mainloop()