import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation


class DataPlotterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Excel Data Plotter")

        # Przyciski do interfejsu
        self.load_button = tk.Button(master, text="Load Excel File", command=self.load_data)
        self.load_button.pack()

        self.plot_button1 = tk.Button(master, text="Plot Column 4", command=lambda: self.setup_animation(3))
        self.plot_button1.pack()

        self.plot_button2 = tk.Button(master, text="Plot Column 5", command=lambda: self.setup_animation(4))
        self.plot_button2.pack()

        # Slider do regulacji prędkości animacji
        self.speed_label = tk.Label(master, text="Animation Speed:")
        self.speed_label.pack()
        self.speed_slider = tk.Scale(master, from_=1, to=100, orient="horizontal")
        self.speed_slider.set(50)  # Domyślna wartość prędkości
        self.speed_slider.pack()

        # Obszar na wykres
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().pack()
        self.line, = self.ax.plot([], [], lw=2)  # Inicjalizacja linii tutaj

        self.ani = None
        self.xdata = []
        self.ydata = []

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.data = pd.read_excel(file_path)
            self.plot_button1.config(state="normal")
            self.plot_button2.config(state="normal")

    def setup_animation(self, column_index):
        if hasattr(self, 'data'):
            if self.ani is not None:
                self.ani.event_source.stop()  # Zatrzymaj bieżącą animację
            self.xdata, self.ydata = [], []  # Reset danych wykresu
            self.animate_data(column_index)
        else:
            print("Please load the data first.")

    def animate_data(self, column_index):
        self.ax.clear()
        self.line, = self.ax.plot([], [], lw=2)  # Ponowna inicjalizacja linii w każdym nowym wywołaniu
        y_min = self.data.iloc[:, column_index].min()
        y_max = self.data.iloc[:, column_index].max()
        self.ax.set_ylim(y_min - (y_max - y_min) * 0.1, y_max + (y_max - y_min) * 0.1)  # Zwiększony zakres osi Y
        self.ax.set_title(f'Animated Plot of Column {column_index + 1}')
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Value')

        def init():
            self.line.set_data([], [])
            return self.line,

        def update(frame):
            if len(self.xdata) > len(self.data):  # Przechowuje tylko ostatnie len(data) punktów
                self.xdata.pop(0)
                self.ydata.pop(0)
            self.xdata.append(frame)
            self.ydata.append(self.data.iloc[frame % len(self.data), column_index])
            self.line.set_data(self.xdata, self.ydata)
            self.ax.set_xlim(max(0, frame - len(self.data)), frame + 1)  # Dynamicznie aktualizowany zakres osi X
            return self.line,

        self.ani = FuncAnimation(self.figure, update, frames=range(1000000),
                                 init_func=init, blit=True, interval=1000 // self.speed_slider.get(), repeat=False)
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DataPlotterApp(root)
    root.mainloop()
