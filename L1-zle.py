import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RealTimePlotApp:
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

        self.animation = FuncAnimation(self.fig, self.update_plot, interval=100)

        # Dodajemy zmienne do przechowywania danych ?????????
        self.data = None

        self.label_max_voltage = tk.Label(self.root, text='Enter the maximum voltage (0-10V):')
        self.label_max_voltage.pack()

        self.entry_max_voltage = tk.Entry(self.root)
        self.entry_max_voltage.pack()

        # Przycisk do wyboru pliku
        self.select_button = tk.Button(self.root, text='Select File', command=self.select_file)
        self.select_button.pack()

    # Funkcja do wczytywania danych z pliku .xlsx
    def load_data(self,filename):
        df = pd.read_excel(filename, header=None)  # Wczytaj dane bez uwzględniania nagłówków kolumn
        return df.iloc[:, 0], df.iloc[:, 1],df.iloc[:, 2]  # Wczytaj pierwszą,drugą,trzecią kolumnę

    def init_plot(self,max_voltage):
        fig, ax = plt.subplots()
        ax.set_xlabel('Time')
        ax.set_ylabel('U(t)')
        ax.set_xlim(0, 50)  # Ustaw zakres osi x od 0 do 50 sekund
        ax.set_ylim(0, max_voltage)
        return fig, ax

    def update_plot(self, frame):
        if self.data is not None and not self.pause:
            self.line1.set_data(self.data[0], self.data[1])
            self.line2.set_data(self.data[0], self.data[2])
            self.ax.relim()
            self.ax.autoscale_view()
            return self.line1, self.line2

    def toggle_pause(self):
        self.pause = not self.pause
        if self.pause:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")

    def load_file(self):
        filename = filedialog.askopenfilename(filetypes=[('Excel files', '*.xlsx')])
        if filename:
            self.data = self.load_data(filename)

    # Funkcja do obsługi przycisku wyboru pliku
    def select_file(self):
        try:
            # Pobranie wartości maksymalnego napięcia z pola Entry i konwersja na float
            max_voltage = float(self.entry_max_voltage.get())

            # Sprawdzenie, czy wartość maksymalnego napięcia mieści się w zakresie (0-10 V)
            if max_voltage < 0 or max_voltage > 10:
                raise ValueError("Voltage value must be between 0 and 10 V")

            # Wyświetlenie komunikatu z wybraną wartością maksymalnego napięcia
            messagebox.showinfo("Info", f"Selected maximum voltage: {max_voltage} V")


        except ValueError as ve:
            # Obsługa wyjątku związanego z nieprawidłowymi danymi wprowadzonymi przez użytkownika
            messagebox.showerror("Error", f"Invalid input: {ve}")



if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlotApp(root)
    root.mainloop()
