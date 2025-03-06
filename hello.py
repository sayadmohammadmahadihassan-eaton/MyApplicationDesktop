import tkinter as tk
import subprocess
from PrepareEepFileTool import PrepareEepFileTool
from CompareFilesWithGivenKeys import CompareFilesWithGivenKeys
from MyLibrary import MyLibrary




# Create object
myLibrary = MyLibrary()
prepareEepFileTool = PrepareEepFileTool()
compareFilesWithGivenKeys = CompareFilesWithGivenKeys()

# Integrate your application into Application 1 frame
def prepare_eep_file_tool():
    '''
    blah
    '''
    global result_text
    app_window = tk.Toplevel(root)
    app_window.title('EEP Comparison Tool')

    tk.Label(app_window, text='File 1:').grid(row=1, column=0, padx=10, pady=5)
    file1_entry = tk.Entry(app_window, width=50)
    file1_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(app_window, text='Browse', command=lambda: prepareEepFileTool.upload_file(file1_entry)).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(app_window, text='File 2:').grid(row=2, column=0, padx=10, pady=5)
    file2_entry = tk.Entry(app_window, width=50)
    file2_entry.grid(row=2, column=1, padx=10, pady=5)
    tk.Button(app_window, text='Browse', command=lambda: prepareEepFileTool.upload_file(file2_entry)).grid(row=2, column=2, padx=10, pady=5)

    tk.Button(app_window, text='Create File', command=lambda:prepareEepFileTool.prepare_eep_file_tool(result_text)).grid(row=3, columnspan=3, pady=20)

    result_text = tk.Text(app_window)
    result_text.grid(row=6, columnspan=3, padx=10, pady=10)

# Integrate your application into Application 1 frame
def com_files_with_given_keys_tool():
    '''
    blah
    '''
    global result_text
    app_window = tk.Toplevel(root)
    app_window.title("Tool: EEP Comparison with Given Keys")

    tk.Label(app_window, text="*Key File:").grid(row=0, column=0, padx=10, pady=5)
    key_file_entry = tk.Entry(root, width=50)
    key_file_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Button(app_window, text='Browse', command=lambda:
            compareFilesWithGivenKeys.upload_file(key_file_entry)).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(app_window, text="File 1:").grid(row=1, column=0, padx=10, pady=5)
    file1_entry = tk.Entry(app_window, width=50)
    file1_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(app_window, text='Browse', command=lambda: 
            compareFilesWithGivenKeys.upload_file(file1_entry)).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(app_window, text="File 2:").grid(row=2, column=0, padx=10, pady=5)
    file2_entry = tk.Entry(app_window, width=50)
    file2_entry.grid(row=2, column=1, padx=10, pady=5)
    tk.Button(app_window, text='Browse', command=lambda: 
            compareFilesWithGivenKeys.upload_file(file2_entry)).grid(row=2, column=2, padx=10, pady=5)

    tk.Label(app_window, text="File 3:").grid(row=3, column=0, padx=10, pady=5)
    file3_entry = tk.Entry(app_window, width=50)
    file3_entry.grid(row=3, column=1, padx=10, pady=5)
    tk.Button(app_window, text='Browse', command=lambda: 
            compareFilesWithGivenKeys.upload_file(file3_entry)).grid(row=3, column=2, padx=10, pady=5)

    tk.Label(app_window, text="File 4:").grid(row=4, column=0, padx=10, pady=5)
    file4_entry = tk.Entry(app_window, width=50)
    file4_entry.grid(row=4, column=1, padx=10, pady=5)
    tk.Button(app_window, text='Browse', command=lambda: 
            compareFilesWithGivenKeys.upload_file(file4_entry)).grid(row=4, column=2, padx=10, pady=5)

    tk.Button(app_window, text="Compare Files", 
            command=lambda: compareFilesWithGivenKeys.compare_files_with_given_keys(result_text)).grid(row=5, columnspan=3, pady=20)

    #tk.Button(root, text="Reset",command=reset(key_file_entry)).grid(row=5, columnspan=1, pady=20)

    result_text = tk.Text(app_window)
    result_text.grid(row=6, columnspan=3, padx=10, pady=10)

def open_app_top(command):
    subprocess.Popen(command)

# Function to open applications
def open_app_bottom(command):
    if command.endswith('.exe'):
        #encoded_path = quote(command)
        subprocess.Popen(command)
    else:
        subprocess.Popen(['cmd', '/c', 'start', command])

# Create the main window
root = tk.Tk()
root.title('My Applications')

# Number of buttons
num_buttons_per_row = 6

# Get screen width and height

root.geometry('800x200')



# Bind the Escape key to exit full screen mode
root.bind('<Escape>', lambda event: root.attributes('-fullscreen', False))

# Create a single frame
frame = tk.Frame(root, bg='lightgray')
frame.pack(expand=True, fill=tk.BOTH)


# Create frames for each row
top_frame = tk.Frame(frame)
middle_frame = tk.Frame(frame)
bottom_frame = tk.Frame(frame)

# Pack the frames
top_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
middle_frame.pack(expand=True, fill=tk.BOTH)
bottom_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

# Configure grid layout for each frame
for i in range(num_buttons_per_row):
    top_frame.columnconfigure(i, weight=1)
    middle_frame.columnconfigure(i, weight=1)
    bottom_frame.columnconfigure(i, weight=1)

top_frame.rowconfigure(0, weight=1)
middle_frame.rowconfigure(0, weight=1)
bottom_frame.rowconfigure(0, weight=1)


# Read links from app.txt
exe_app_links = myLibrary.read_links()

app_list_top = [prepare_eep_file_tool, com_files_with_given_keys_tool]
exe_app_links.extend(app_list_top)

app_list_top_name = ['Panda XCP', 'Pletc', 'Panda VAR Logger', 'Teraterm', 'Eflash', 'ELL', 'MX', 'MX Sequencer', 'Create EEP File', 'Compare EEP', 'HMI','HMI']
app_list_bottom = ['notepad', 'calc', 'ms-clock:', 'cmd', 'onenote', 'excel']
app_list_bottom_name = ['Notepad', 'Calculator', 'Clock', 'Command Prompt', 'OneNote', 'Excel']


for i, app_top in enumerate(exe_app_links[0:6]):
    button_top = tk.Button(top_frame, text=app_list_top_name[i], width=15, command=lambda app=app_top: open_app_top(app))
    button_top.pack(side='left', expand=True, fill='both')

for i, app_top in enumerate(exe_app_links[6:]):
    button_top = tk.Button(middle_frame, text=app_list_top_name[i+6], width=15, command=lambda app=app_top: open_app_top(app))
    button_top.pack(side='left', expand=True, fill='both')

for i, app_bottom in enumerate(app_list_bottom): 
    button_bottom = tk.Button(bottom_frame, text=app_list_bottom_name[i], width=15, command=lambda app=app_bottom: open_app_bottom(app))
    button_bottom.pack(side='left', expand=True, fill='both')


# Run the application
root.mainloop()
