import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox as messagebox


current_interval = 1  # Set initial update interval
points_to_update = 30  # Number of points to update per interval
plot_range = 50  # Initial range for x-axis
data = []  # Variable to store data
time = []  # Variable to store time


def read_lvm_data(filepath):
    global data, time
    data = []
    time = []

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
                time.append(float(columns[0]))
                data.append([float(val) for val in columns[1:]])
    print("Data read successfully")


def update_plot(data, time, index):
    ax.clear()  # Clear the previous plot
    if len(data[0]) >= 5:  # Check if there are at least 5 series
        series = [point[4] for point in data[:index]]  # 5th series
        ax.plot(time[:index], series, label='Series 5', color='b')

    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.legend(loc='upper left')

    current_time = time[index - 1]

    start_x = max(0, current_time - 0.9 * plot_range)
    end_x = start_x + plot_range

    if end_x > time[-1]:  # Adjust end_x if it exceeds the max time
        end_x = time[-1]
        start_x = max(0, end_x - plot_range)  # Adjust start_x accordingly

    ax.set_xlim(start_x, end_x)

    # y scaling
    visible_series = [point[4] for point in data if start_x <= point[0] <= end_x]
    if visible_series:
        min_y = min(visible_series)
        max_y = max(visible_series)
        margin_y = (max_y - min_y) * 0.1  # Add 10% margin
        ax.set_ylim(min_y - margin_y, max_y + margin_y)

    canvas.draw()

def start_plotting():
    global data, time
    if data and time:
        def update(index):
            if index <= len(time):
                update_plot(data, time, index)
                window.after(current_interval, update, index + points_to_update)
            else:
                # Start again
                window.after(1, start_plotting)

        update(0)


def open_file():
    global data, time
    filepath = filedialog.askopenfilename(title="Select MATLAB lvm file")
    if filepath:
        read_lvm_data(filepath)
        start_plotting()


def change_interval():
    global current_interval
    try:
        new_interval = int(interval_entry.get())
        if new_interval > 0:
            current_interval = new_interval
            print(f"Interval changed to {new_interval} ms")
        else:
            messagebox.showerror("Error", "Interval value must be a positive integer.")
    except ValueError:
        messagebox.showerror("Error", "Invalid interval value. Please enter a valid integer.")


def change_points_to_update():
    global points_to_update
    try:
        new_points_to_update = int(points_entry.get())
        if 0<new_points_to_update  < 30000:
            points_to_update = new_points_to_update
            print(f"Points to update changed to {new_points_to_update}")
        else:
            messagebox.showerror("Error", "Points value must be a positive integer. and less than 30000")
    except ValueError:
        messagebox.showerror("Error", "Invalid points value. Please enter a valid integer.")


def update_plot_range():
    global plot_range
    try:
        new_range = float(range_entry.get())
        if new_range > 0:
            plot_range = new_range
            print(f"X-axis range changed to {new_range}")
            update_plot(data, time, len(time))
        else:
            messagebox.showerror("Error", "Range value must be a positive number.")
    except ValueError:
        messagebox.showerror("Error", "Invalid range value. Please enter a valid number.")

def on_closing():
    window.quit()

# Create the main window
window = tk.Tk()
window.title("MATLAB lvm Data Plotter")

# Create the plot
fig, ax = plt.subplots()
ax.set_xlabel('Time')
ax.set_ylabel('Value')

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

open_button = tk.Button(window, text="Open File", command=open_file)
open_button.pack(pady=10)

interval_frame = tk.Frame(window)
interval_frame.pack(pady=10)

interval_label = tk.Label(interval_frame, text="Update Interval (ms):")
interval_label.pack(side=tk.LEFT)

interval_entry = tk.Entry(interval_frame, width=10)
interval_entry.pack(side=tk.LEFT)
interval_entry.insert(0, str(current_interval))  # Set default value

interval_button = tk.Button(interval_frame, text="Change Interval", command=change_interval)
interval_button.pack(side=tk.LEFT, padx=5)

points_frame = tk.Frame(window)
points_frame.pack(pady=10)

points_label = tk.Label(points_frame, text="Points to Update:")
points_label.pack(side=tk.LEFT)

points_entry = tk.Entry(points_frame, width=10)
points_entry.pack(side=tk.LEFT)
points_entry.insert(0, str(points_to_update))  # Set default value

points_button = tk.Button(points_frame, text="Change Points", command=change_points_to_update)
points_button.pack(side=tk.LEFT, padx=5)

range_frame = tk.Frame(window)
range_frame.pack(pady=10)

range_label = tk.Label(range_frame, text="X-axis Range:")
range_label.pack(side=tk.LEFT)

range_entry = tk.Entry(range_frame, width=10)
range_entry.pack(side=tk.LEFT)
range_entry.insert(0, str(plot_range))  # RESET VALUE

range_button = tk.Button(range_frame, text="Change Range", command=update_plot_range)
range_button.pack(side=tk.LEFT, padx=5)
window.protocol("WM_DELETE_WINDOW", on_closing)


print("Starting Tkinter main loop")
window.mainloop()
print("Tkinter main loop ended")
