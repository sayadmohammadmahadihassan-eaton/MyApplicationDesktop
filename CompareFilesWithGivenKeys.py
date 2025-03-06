''' 
This tool compare file with gien key values
Useful to pick eep values.
'''
import tkinter as tk
from tkinter import filedialog
from prettytable import PrettyTable
import MyLibrary

# Create object
MyLibrary = MyLibrary.MyLibrary()
table = PrettyTable()




class CompareFilesWithGivenKeys:
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


    def compare_files_with_given_keys(self, result):
        '''
        compare key with other file value.
        '''
        keys, key_value_pair = MyLibrary.read_keys(self.uploaded_file[0])
        table.add_column('Key File', key_value_pair)

        for fl in self.uploaded_file[1:]:
            pair = MyLibrary.read_key_value_pairs(fl)
            list_of_pair = []

            for key in keys:
                if key in pair:
                    list_of_pair.append(f"{key} : {pair[key]}")

            # Add columns to the table
            title = fl.rsplit('/', maxsplit=1)[-1].rsplit('.', maxsplit=1)[0]
            table.add_column(title, list_of_pair)

        table.align = 'l'
        result.delete(1.0, tk.END)
        result.insert(tk.END, table.get_string())
