import tkinter as tk
from tkinter import filedialog
from prettytable import PrettyTable
import MyLibrary
import subprocess
import os

# Create object
MyLibrary = MyLibrary.MyLibrary()
table = PrettyTable()

uploaded_file = []

def get_file(entry):
    '''
    Get file in list for use.
    '''
    uploaded_file.append(entry)

def upload_file(entry):
    '''
    upload file from gui to compare.
    '''
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
    get_file(file_path)

def prepare_eep_restore_file():
    '''
    create restore eep file from integers like 100 : 100
    '''
    _integer_1 = MyLibrary.read_integer(uploaded_file[0])
    _integer_2 = MyLibrary.read_integer(uploaded_file[1])

    if len(_integer_1) == len(_integer_2):
        for i, value in enumerate (_integer_1):
            result_text.insert(tk.END, f'{_integer_1[i]} : {_integer_2[i]}\n')
    else:
        print('Number of integers are not equal.')

# Function to exit full screen mode
def exit_fullscreen(event=None):
    root.attributes('-fullscreen', False)

# Function to open an application
def open_app(command):
    subprocess.Popen(command)

# Create the main window
root = tk.Tk()
root.title("Four Applications Side by Side")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the main window size to 80% of the screen size
window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
root.geometry(f"{window_width}x{window_height}+{int(screen_width*0.1)}+{int(screen_height*0.1)}")

# Bind the Escape key to exit full screen mode
root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))

# Create four frames
frame1 = tk.Frame(root, bg="red")
frame2 = tk.Frame(root, bg="blue")
frame3 = tk.Frame(root, bg="green")
frame4 = tk.Frame(root, bg="yellow")

# Use grid to place the frames in a 2x2 layout
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew")
frame4.grid(row=1, column=1, sticky="nsew")

# Configure the grid to make the frames expand equally
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Integrate your application into Application 1 frame
def open_app1():
    exe_path = os.path.join("subfolder", "WT_DataExtractor_v1.5.exe")
    subprocess.Popen([exe_path])

# Example application GUI for other frames
def create_demo_app_gui(frame):
    label = tk.Label(frame, text="Demo Application", font=("Arial", 24))
    label.pack(expand=True)

create_demo_app_gui(frame2)
create_demo_app_gui(frame3)

# Create GUI for Application 4 with six buttons (three on top and three on bottom)
def create_app4_gui(frame):
    top_frame = tk.Frame(frame)
    bottom_frame = tk.Frame(frame)
    
    top_frame.pack(expand=True, fill='both')
    bottom_frame.pack(expand=True, fill='both')
    
    app_list_top = [open_app1] * 3
    app_list_bottom = ["notepad", "calc", "teraterm"]
    
    for i in range(3):
        button_top = tk.Button(top_frame, text=f"Open App {i+1}", command=app_list_top[i])
        button_top.pack(side='left', expand=True, fill='both')
        
        button_bottom = tk.Button(bottom_frame, text=f"Open {app_list_bottom[i]}", command=lambda i=i: open_app([app_list_bottom[i]]))
        button_bottom.pack(side='left', expand=True, fill='both')

create_app4_gui(frame4)

# Run the application
root.mainloop()

# these are for test
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
