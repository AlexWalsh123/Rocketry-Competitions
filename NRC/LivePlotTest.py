import random
from itertools import count
from matplotlib.figure import Figure
#import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.geometry('1200x700+200+100')
root.title('This is my root window')
root.state('zoomed')
root.config(background='#fafafa')

plt.style.use('dark_background')

x = []
y1 = []

index = count()

fig = Figure(figsize=(6,6))
a = fig.add_subplot(111)
a.plot(x, y1, color='white')
#a.ylim([0, 4500])
#a.xlim([0, 100])
#a.ylabel("Altitude(m)")
#a.xlabel("Time(s)")

while True:
    def animate(i):
        data = pd.read_csv('data.csv')
        x = data['x_value']
        y1 = data['total_1']
        y2 = data['total_2']

        


        #a.tight_layout()

        #canvas = FigureCanvasTkAgg(fig, master = self.window)
        #canvas.get_tk_widget().pack()
        #canvas.draw()



        #  plt.cla()

        #  plt.plot(x, y1, color='white')
        #  plt.plot(x, y2, label='Channel 2')
        #  plt.ylim([0, 4500])
        #  plt.xlim([0, 100])
        #  plt.ylabel("Altitude(m)")
        #  plt.xlabel("Time(s)")
        #  plt.tight_layout()

    plotcanvas = FigureCanvasTkAgg(fig, root)
    plotcanvas.get_tk_widget().grid(column=1, row=1)
    ani = FuncAnimation(fig, animate, interval=1000, blit=False)

    root.mainloop()

    #ani = FuncAnimation(plt.gcf(), animate, interval=10)

    #window= Tk()
    #start= mclass (window)
    #window.mainloop()

    #plt.tight_layout()
