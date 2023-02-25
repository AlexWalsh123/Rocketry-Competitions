import pandas as pd
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
    
class Graph(tk.Frame):
    def __init__(self, master=None, title="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.fig = Figure(figsize=(4, 3))
        ax = self.fig.add_subplot(111)
        df = pd.DataFrame({"values": np.random.randint(0, 50, 10)}) #dummy data
        df.plot(ax=ax)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        tk.Label(self, text=f"Graph {title}").grid(row=0)
        self.canvas.get_tk_widget().grid(row=1, sticky="nesw")

root = tk.Tk()

for num, i in enumerate(list("ABCDEFGHI")):
    Graph(root, title=i, width=200).grid(row=num//2, column=num%2)

text_box = tk.Text(root, width=50, height=10, wrap=tk.WORD)
text_box.grid(row=1, column=1, sticky="nesw")
text_box.delete(0.0, "end")
text_box.insert(0.0, 'My message will be here.')

root.mainloop()