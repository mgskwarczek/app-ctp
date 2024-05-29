# L2_FINAL.py

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox

class RealTimePlotAppL2:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Plot App")

        self.frame_controls = tk.Frame(self.root)
        self.frame_controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.frame_plot = tk.Frame(self.root)
        self.frame_plot.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.label_max_voltage = tk.Label(self.frame_controls, text='Enter the maximum voltage (0-10V):')
        self.label_max_voltage.grid(row=0, column=0, padx=5, pady=5)

        self.entry_max_voltage = tk.Entry(self.frame_controls)
        self.entry_max_voltage.grid(row=0, column=1, padx=5, pady=5)

        self.label_max_displacement = tk.Label(self.frame_controls, text='Enter the maximum displacement (0-0.5m):')
        self.label_max_displacement.grid(row=1, column=0, padx=5, pady=5)

        self.entry_max_displacement = tk.Entry(self.frame_controls)
        self.entry_max_displacement.grid(row=1, column=1, padx=5, pady=5)

        self.select_button = tk.Button(self.frame_controls, text='Select File', command=self.select_file)
        self.select_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plot)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.back_button = tk.Button(self.frame_plot, text="Wstecz", command=self.root.destroy)
        self.back_button.pack(side=tk.BOTTOM, pady=10)

    def select_file(self):
        try:
            max_voltage = float(self.entry_max_voltage.get())
            max_displacement = float(self.entry_max_displacement.get())

            if max_voltage <= 0 or max_displacement <= 0:
                raise ValueError("Values must be positive")

            a = max_displacement / max_voltage

            filename = filedialog.askopenfilename(filetypes=[('Excel files', '*.xlsx')])
            if not filename:
                return

            time, U = load_data(filename)
            self.ax.clear()
            self.ax.set_xlim(0, 20)
            self.ax.set_ylim(0, max_displacement)
            self.ani = FuncAnimation(self.fig, update_plot, frames=len(time), fargs=(time, U, a, self.ax), interval=20, repeat=False)
            self.canvas.draw()

        except ValueError as ve:
            messagebox.showerror("Error", f"Invalid input: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def generate_signal(U, a):
    return a * U

def load_data(filename):
    df = pd.read_excel(filename, header=None)
    return df.iloc[:, 0], df.iloc[:, 1]

def update_plot(frame, time, U, a, ax):
    ax.clear()
    ax.set_xlabel('Time')
    ax.set_ylabel('WF(t)')
    ax.set_xlim(max(0, time[frame] - 20), max(20, time[frame]))
    ax.plot(time[:frame], generate_signal(U[:frame], a), color='blue')

# Kod inicjalizacyjny aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlotAppL2(root)
    root.mainloop()
