import tkinter as tk
from L1_FINAL import RealTimePlotAppL1
from L2_FINAL import RealTimePlotAppL2
from L3_FINAL import DataPlotterApp
from L4_FINAL import RealTimePlotAppL4

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")

        self.label = tk.Label(root, text="Wybierz aplikację do uruchomienia:")
        self.label.pack(pady=20)

        self.button1 = tk.Button(root, text="Aplikacja L1", command=self.run_l1)
        self.button1.pack(pady=10)

        self.button2 = tk.Button(root, text="Aplikacja L2", command=self.run_l2)
        self.button2.pack(pady=10)

        self.button3 = tk.Button(root, text="Aplikacja L3", command=self.run_l3)
        self.button3.pack(pady=10)

        self.button4 = tk.Button(root, text="Aplikacja L4", command=self.run_l4)
        self.button4.pack(pady=10)

    def run_l1(self):
        self.new_window()
        RealTimePlotAppL1(self.new_root)

    def run_l2(self):
        self.new_window()
        RealTimePlotAppL2(self.new_root)

    def run_l3(self):
        self.new_window()
        DataPlotterApp(self.new_root)

    def run_l4(self):
        self.new_window()
        RealTimePlotAppL4(self.new_root)

    def new_window(self):
        self.new_root = tk.Toplevel(self.root)
        self.new_root.protocol("WM_DELETE_WINDOW", self.new_root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
