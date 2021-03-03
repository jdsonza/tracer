from pathlib import Path
import tkinter as tk
import tkinter.filedialog

import pandas as pd 
from pandastable import Table, TableModel


class Window:
    def __init__(self, root):
        self.root = root
        root.title("Contact Tracing")
        root.geometry()
        self.browseButton = tk.Button(
            master=root, 
            text="Browse files", 
            command=self.browseFiles
        )
        self.executeButton = tk.Button(
            master=root,
            text="Begin Contact Tracing",
            command=self.contactTracing
        )
        self.positiveAttendeeIdEntry = tk.Entry(
            master=root
        )
        self.positiveAttendeeIdEntry.insert(0, 'INFECT001')

        self.browseButton.pack()
        self.positiveAttendeeIdEntry.pack()
        self.executeButton.pack()
    
    def browseFiles(self):
        self.filenames = tk.filedialog.askopenfilenames(
            initialdir = str(Path.cwd()),
            title = "Select a File",
            filetypes = (("Excel Files",
            ".xlsx .xls"),
            ("all files",
            "*.*"))
        )
    
    def contactTracing(self):
        self.df = readExcel(self.filenames)
        self.df = dataPreprocessing(self.df)
        positiveAttendeeID = self.positiveAttendeeIdEntry.get() 
        print(self.df.query("Attendees_User_ID == @positiveAttendeeID").filter(items=[
            'Event_Name',"Attendees_User_ID",'Appointment_Time', 'Location']))
        f = tk.Frame(self.root)
        f.pack()
        self.table = pt = Table(f, dataframe=self.df,
                                showtoolbar=True, showstatusbar=True)
        pt.show()
            

def readExcel(filenames):
    df = pd.DataFrame()
    for file in filenames:
        data = pd.read_excel(file)
        df = df.append(data)
    
    return df

def dataPreprocessing(df):
    df.columns = df.columns.str.replace(" ","_")
    df.columns = df.columns.str.replace("'","")
    df.Appointment_Time = pd.to_datetime(df["Appointment_Time"])

    return df

      

if __name__ == "__main__":
    root = tk.Tk()   
    Window(root)
    root.mainloop()                                                                                              


