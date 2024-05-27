import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox

class RealTimePlotAppL1:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Plot App")

        self.fig, self.ax = plt.subplots()
        self.line1, = self.ax.plot([], [], label='V1')
        self.line2, = self.ax.plot([], [], label='V2')
        self.ax.legend()

        self.pause = False

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack()

        self.load_button = tk.Button(self.root, text="Load File", command=self.load_file)
        self.load_button.pack()

        self.time = []
        self.v1 = []
        self.v2 = []
        self.animation = None

    def toggle_pause(self):
        self.pause = not self.pause

    def load_file(self):
        try:
            max_voltage = float(entry_max_voltage.get())
            if not (0 < max_voltage <= 10):
                raise ValueError("Voltage must be in the range (0, 10].")

            filename = filedialog.askopenfilename(filetypes=[('Excel files', '*.xlsx')])
            if not filename:
                return

            self.time, self.v1, self.v2 = load_data(filename)
            self.ax.set_xlim(0, 20)
            self.ax.set_ylim(0, max_voltage)

            if self.animation:
                self.animation.event_source.stop()

            self.animation = FuncAnimation(self.fig, self.update_plot, frames=len(self.time), interval=20, blit=True, repeat=False)
            self.canvas.draw()
        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_plot(self, frame):
        if not self.pause and frame < len(self.time):
            self.line1.set_data(self.time[:frame], self.v1[:frame])
            self.line2.set_data(self.time[:frame], self.v2[:frame])
            self.ax.set_xlim(max(0, self.time[frame] - 20), self.time[frame])
        return self.line1, self.line2


def load_data(filename):
    df = pd.read_excel(filename, header=None)
    return df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2]


root = tk.Tk()
root.title('Real-time U(t) Plot')

label_max_voltage = tk.Label(root, text='Enter the maximum voltage (0-10V):')
label_max_voltage.pack()

entry_max_voltage = tk.Entry(root)
entry_max_voltage.pack()

select_button = tk.Button(root, text='Select File', command=lambda: RealTimePlotApp(root).load_file())
select_button.pack()

root.mainloop()
