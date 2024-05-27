import tkinter as tk
from L1_FINAL import RealTimePlotAppL1
from L2_FINAL import RealTimePlotAppL2


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")

        self.label = tk.Label(root, text="Select the application to run:")
        self.label.pack(pady=10)

        self.button_l1 = tk.Button(root, text="Run L1 Application", command=self.run_l1)
        self.button_l1.pack(pady=5)

        self.button_l2 = tk.Button(root, text="Run L2 Application", command=self.run_l2)
        self.button_l2.pack(pady=5)

        self.button_l4 = tk.Button(root, text="Run L4 Application", command=self.run_l4)
        self.button_l4.pack(pady=5)

    def run_l1(self):
        self.root.destroy()  # Close the main menu window
        root_l1 = tk.Tk()
        RealTimePlotAppL1(root_l1)
        root_l1.mainloop()

    def run_l2(self):
        self.root.destroy()  # Close the main menu window
        root_l2 = tk.Tk()
        RealTimePlotAppL2(root_l2)
        root_l2.mainloop()

    def run_l4(self):
        self.root.destroy()
        root_l4 =tk.Tk()
        from L4_FINAL import RealTimePlotAppL4
        RealTimePlotAppL4(root_l4)
        root_l4.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
