import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog, messagebox

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


# Funkcja do generowania sygnału WF
def generate_signal(U, a):
    return a * U


# Funkcja do wczytywania danych z pliku .xlsx
def load_data(filename):
    df = pd.read_excel(filename, header=None)  # Wczytaj dane bez uwzględniania nagłówków kolumn
    return df.iloc[:, 0], df.iloc[:, 1]  # Wczytaj pierwszą i drugą kolumnę


# Funkcja do inicjalizacji wykresu
def init_plot(max_displacement):
    fig, ax = plt.subplots()
    ax.set_xlabel('Time')
    ax.set_ylabel('WF(t)')
    ax.set_xlim(0, 20)  # Ustaw zakres osi x od 0 do 20 sekund
    ax.set_ylim(0, max_displacement)  # Ustaw zakres osi y zgodnie z podanym zakresem przesunięcia
    return fig, ax


# Funkcja do aktualizacji wykresu
def update_plot(frame, time, U, a, ax):
    ax.clear()
    ax.set_xlabel('Time')
    ax.set_ylabel('WF(t)')

    ax.set_xlim(max(0, time[frame] - 20), max(20, time[frame]))  # Przesuwamy okno, aby wyświetlić 20 ostatnich sekund

    # Rysowanie wykresu
    ax.plot(time[:frame], generate_signal(U[:frame], a), color='blue')


# Funkcja do obsługi przycisku wyboru pliku
def select_file():
    try:
        max_voltage = float(entry_max_voltage.get())  # Pobierz maksymalne napięcie z pola Entry i konwertuj na float
        max_displacement = float(
            entry_max_displacement.get())  # Pobierz maksymalne wysunięcie z pola Entry i konwertuj na float

        if max_voltage <= 0 or max_displacement <= 0:
            raise ValueError("Values must be positive")

        a = max_displacement / max_voltage  # Oblicz współczynnik 'a'

        filename = filedialog.askopenfilename(filetypes=[('Excel files', '*.xlsx')])
        if not filename:
            return

        time, U = load_data(filename)
        fig, ax = init_plot(max_displacement)

        canvas = FigureCanvasTkAgg(fig, master=root)  # Utwórz canvas z wykresem
        canvas.get_tk_widget().pack()

        ani = FuncAnimation(fig, update_plot, frames=len(time), fargs=(time, U, a, ax), interval=20, repeat=False)
        canvas.draw()

    except ValueError as ve:
        messagebox.showerror("Error", f"Invalid input: {ve}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Interfejs użytkownika
root = tk.Tk()
root.title('Real-time WF(t) Plot')

label_max_voltage = tk.Label(root, text='Enter the maximum voltage (0-10V):')
label_max_voltage.pack()

entry_max_voltage = tk.Entry(root)
entry_max_voltage.pack()

label_max_displacement = tk.Label(root, text='Enter the maximum displacement (0-0.5m):')
label_max_displacement.pack()

entry_max_displacement = tk.Entry(root)
entry_max_displacement.pack()

select_button = tk.Button(root, text='Select File', command=select_file)
select_button.pack()

root.mainloop()


