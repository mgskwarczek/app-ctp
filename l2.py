import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MeasurementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cyfrowe Techniki Pomiarowe")

        self.load_button = tk.Button(self.master, text="Wczytaj plik Excel", command=self.load_excel)
        self.load_button.pack()

        self.figure = plt.figure()

        #subplot L1 i L2
        self.ax1 = self.figure.add_subplot(211)
        self.ax1 = self.figure.add_subplot(212)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

    def load_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            data = pd.read_excel(file_path)

    def plot_data(self, data):
        # Wykres L1 - U(t) w czasie rzeczywistym
        self.ax1.clear()
        self.ax1.plot(data['Time'], data['U'], label='U(t)')
        self.ax1.set_ylabel('U(t)')
        self.ax1.set_title('Wykres U(t) w czasie rzeczywistym')
        self.ax1.set_xlim(0, 500)  # Zakres X: 0-500
        self.ax1.set_ylim(0, 10)  # Zakres Y: 0-10
        self.ax1.legend()

        # Wykres L2 - WF(t) w czasie rzeczywistym po kalibracji
        self.ax2.clear()
        a = 2  # Przykładowa wartość nachylenia
        b = 1  # Przykładowa wartość przesunięcia
        data['X'] = a * data['U'] + b
        self.ax2.plot(data['Time'], data['X'], label='WF(t)')
        self.ax2.set_ylabel('WF(t)')
        self.ax2.set_xlabel('Czas')
        self.ax2.set_title('Wykres WF(t) w czasie rzeczywistym po kalibracji')
        self.ax2.set_xlim(0, 500)  # Zakres X: 0-500
        self.ax2.set_ylim(0, 500)  # Zakres Y: 0-500
        self.ax2.legend()

        # Dodanie opisów osi
        self.ax1.set_xlabel('Czas')
        self.ax1.set_ylabel('Wartość')
        self.ax2.set_xlabel('Czas')
        self.ax2.set_ylabel('Wartość')

        self.canvas.draw()

def main():
    root = tk.Tk()
    app = MeasurementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
