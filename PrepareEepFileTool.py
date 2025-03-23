''' 
This tool create restore eep file from integers.
'''
import tkinter as tk
from tkinter import filedialog
from prettytable import PrettyTable
import MyLibrary

# Create object
MyLibrary = MyLibrary.MyLibrary()
table = PrettyTable()


class PrepareEepFileTool:
    ''' 
    This tool create restore eep file from integers.
    '''
    def __init__(self):
        self.uploaded_file = []

    def get_file(self, entry):
        '''
        Get file in list for use.
        '''
        self.uploaded_file.append(entry)

    def upload_file(self, entry):
        '''
        upload file from gui to compare.
        '''
        file_path = filedialog.askopenfilename()
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        self.get_file(file_path)

    def prepare_eep_file_tool(self, result):
        '''
        create restore eep file from integers like 100 : 100
        '''
        _integer_1 = MyLibrary.read_integer(self.uploaded_file[0])
        _integer_2 = MyLibrary.read_integer(self.uploaded_file[1])

        if len(_integer_1) == len(_integer_2):
            for i, value in enumerate (_integer_1):
                result.insert(tk.END, f'{_integer_1[i]} : {_integer_2[i]}\n')
        else:
            print('Number of integers are not equal.')

    