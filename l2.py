import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MeasurementAppL2:
    def __init__(self, master):
        self.master = master
        self.master.title("Cyfrowe Techniki Pomiarowe - L2")

        self.load_button = tk.Button(self.master, text="Wczytaj plik Excel", command=self.load_excel)
        self.load_button.pack()

        self.figure = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack()

    def load_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            data = pd.read_excel(file_path)

            # Zakres danych
            x_min = 0
            x_max = 500
            y_min = 0
            y_max = 10

            # Przeprowadzanie kalibracji
            a = 2  # Przykładowa wartość nachylenia
            b = 1  # Przykładowa wartość przesunięcia
            data['X'] = a * data['U'] + b

            # Generowanie wykresu XY
            plt.clf()
            plt.plot(data['U'], label='u(t)')
            plt.plot(data['X'], label='x(t) po kalibracji')
            plt.xlabel('Czas')
            plt.ylabel('Wartość')
            plt.xlim(x_min, x_max)
            plt.ylim(y_min, y_max)
            plt.legend()
            self.canvas.draw()

def main():
    root = tk.Tk()
    app = MeasurementAppL2(root)
    root.mainloop()

if __name__ == "__main__":
    main()
