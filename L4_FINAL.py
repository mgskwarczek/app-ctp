# L4_FINAL.py

import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as messagebox

class RealTimePlotAppL4:
    def __init__(self, root):
        self.root = root
        self.root.title("MATLAB lvm Data Plotter")

        self.current_interval = 1  # Set initial update interval
        self.points_to_update = 30  # Number of points to update per interval
        self.plot_range = 50  # Initial range for x-axis
        self.data = []  # Variable to store data
        self.time = []  # Variable to store time

        # Create plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Time[s]')
        self.ax.set_ylabel('Ni [obr/min]')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.open_button = tk.Button(self.root, text="Open File", command=self.open_file)
        self.open_button.pack(pady=10)

        self.interval_frame = tk.Frame(self.root)
        self.interval_frame.pack(pady=10)

        self.interval_label = tk.Label(self.interval_frame, text="Update Interval (ms):")
        self.interval_label.pack(side=tk.LEFT)

        self.interval_entry = tk.Entry(self.interval_frame, width=10)
        self.interval_entry.pack(side=tk.LEFT)
        self.interval_entry.insert(0, str(self.current_interval))  # Set default value

        self.interval_button = tk.Button(self.interval_frame, text="Change Interval", command=self.change_interval)
        self.interval_button.pack(side=tk.LEFT, padx=5)

        self.points_frame = tk.Frame(self.root)
        self.points_frame.pack(pady=10)

        self.points_label = tk.Label(self.points_frame, text="Points to Update:")
        self.points_label.pack(side=tk.LEFT)

        self.points_entry = tk.Entry(self.points_frame, width=10)
        self.points_entry.pack(side=tk.LEFT)
        self.points_entry.insert(0, str(self.points_to_update))  # Set default value

        self.points_button = tk.Button(self.points_frame, text="Change Points", command=self.change_points_to_update)
        self.points_button.pack(side=tk.LEFT, padx=5)

        self.range_frame = tk.Frame(self.root)
        self.range_frame.pack(pady=10)

        self.range_label = tk.Label(self.range_frame, text="X-axis Range:")
        self.range_label.pack(side=tk.LEFT)

        self.range_entry = tk.Entry(self.range_frame, width=10)
        self.range_entry.pack(side=tk.LEFT)
        self.range_entry.insert(0, str(self.plot_range))  # Set default value

        self.range_button = tk.Button(self.range_frame, text="Change Range", command=self.update_plot_range)
        self.range_button.pack(side=tk.LEFT, padx=5)

        self.back_button = tk.Button(self.root, text="Wstecz", command=self.back_to_main)
        self.back_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def read_lvm_data(self, filepath):
        self.data = []
        self.time = []

        print(f"Reading file: {filepath}")

        with open(filepath, 'r') as file:
            next(file)  # Skip the header line
            for line in file:
                line = line.strip()  # Remove whitespace
                if not line:
                    continue  # Skip empty lines
                line = line.replace(',', '.')  # Replace commas with periods

                columns = line.split()
                if len(columns) == 6:
                    self.time.append(float(columns[0]))
                    self.data.append([float(val) for val in columns[1:]])
        print("Data read successfully")

    def update_plot(self, index):
        self.ax.clear()  # Clear the previous plot
        if len(self.data[0]) >= 5:  # Check if there are at least 5 series
            series = [point[4] for point in self.data[:index]]  # 5th series
            self.ax.plot(self.time[:index], series, label='Ni', color='b')

        self.ax.set_xlabel('Time[s]')
        self.ax.set_ylabel('Ni[obr/min]')
        self.ax.legend(loc='upper left')

        current_time = self.time[index - 1]

        start_x = max(0, current_time - 0.9 * self.plot_range)
        end_x = start_x + self.plot_range

        if end_x > self.time[-1]:  # Adjust end_x if it exceeds the max time
            end_x = self.time[-1]
            start_x = max(0, end_x - self.plot_range)  # Adjust start_x accordingly

        self.ax.set_xlim(start_x, end_x)

        # y scaling
        visible_series = [point[4] for point in self.data if start_x <= point[0] <= end_x]
        if visible_series:
            min_y = min(visible_series)
            max_y = max(visible_series)
            margin_y = (max_y - min_y) * 0.1  # Add 10% margin
            self.ax.set_ylim(min_y - margin_y, max_y + margin_y)

        self.canvas.draw()

    def start_plotting(self):
        if self.data and self.time:
            def update(index):
                if index <= len(self.time):
                    self.update_plot(index)
                    self.root.after(self.current_interval, update, index + self.points_to_update)
                else:
                    # Start again
                    self.root.after(1, self.start_plotting)

            update(0)

    def open_file(self):
        filepath = filedialog.askopenfilename(title="Select MATLAB lvm file")
        if filepath:
            self.read_lvm_data(filepath)
            self.start_plotting()

    def change_interval(self):
        try:
            new_interval = int(self.interval_entry.get())
            if new_interval > 0:
                self.current_interval = new_interval
                print(f"Interval changed to {new_interval} ms")
            else:
                messagebox.showerror("Error", "Interval value must be a positive integer.")
        except ValueError:
            messagebox.showerror("Error", "Invalid interval value. Please enter a valid integer.")

    def change_points_to_update(self):
        try:
            new_points_to_update = int(self.points_entry.get())
            if 0 < new_points_to_update < 30000:
                self.points_to_update = new_points_to_update
                print(f"Points to update changed to {new_points_to_update}")
            else:
                messagebox.showerror("Error", "Points value must be a positive integer and less than 30000.")
        except ValueError:
            messagebox.showerror("Error", "Invalid points value. Please enter a valid integer.")

    def update_plot_range(self):
        try:
            new_range = float(self.range_entry.get())
            if new_range > 0:
                self.plot_range = new_range
                print(f"X-axis range changed to {new_range}")
                self.update_plot(len(self.time))
            else:
                messagebox.showerror("Error", "Range value must be a positive number.")
        except ValueError:
            messagebox.showerror("Error", "Invalid range value. Please enter a valid number.")

    def back_to_main(self):
        self.root.destroy()
        # Usunięto referencję do MainApp

    def on_closing(self):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlotAppL4(root)
    root.mainloop()
