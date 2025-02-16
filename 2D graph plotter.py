import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GraphPlotter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Interactive Graph Plotter")
        self.geometry("800x600")

        self.func_entry = tk.Entry(self, width=50)
        self.func_entry.pack(pady=10)
        self.func_entry.insert(0, "np.sin(x)")

        self.plot_button = tk.Button(self, text="Plot Graph", command=self.plot_graph)
        self.plot_button.pack(pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.bind("<MouseWheel>", self.zoom)
        self.canvas.mpl_connect("button_press_event", self.on_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        self.pan_active = False
        self.press = None

    def plot_graph(self):
        func_str = self.func_entry.get()
        x = np.linspace(-10, 10, 1000)
        
        try:
            y = eval(func_str)
            self.ax.clear()
            self.ax.plot(x, y)
            self.canvas.draw()
        except Exception as e:
            print(f"Error in function: {e}")

    def zoom(self, event):
        base_scale = 1.1
        cur_xlim = self.ax.get_xlim()
        cur_ylim = self.ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata

        if event.delta > 0:
            scale_factor = 1 / base_scale
        else:
            scale_factor = base_scale

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        self.ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * relx])
        self.ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * rely])

        self.canvas.draw()

    def on_press(self, event):
        if event.button == 1:
            self.pan_active = True
            self.press = event.xdata, event.ydata

    def on_move(self, event):
        if self.pan_active:
            dx = event.xdata - self.press[0]
            dy = event.ydata - self.press[1]
            self.press = event.xdata, event.ydata

            cur_xlim = self.ax.get_xlim()
            cur_ylim = self.ax.get_ylim()

            self.ax.set_xlim(cur_xlim[0] - dx, cur_xlim[1] - dx)
            self.ax.set_ylim(cur_ylim[0] - dy, cur_ylim[1] - dy)
            self.canvas.draw()

    def on_release(self, event):
        self.pan_active = False
        self.press = None

if __name__ == "__main__":
    app = GraphPlotter()
    app.mainloop()
