from pathlib import Path
import tkinter as tk
import tkinter.filedialog
from tkcalendar import DateEntry

import pandas as pd 
from pandastable import Table, TableModel


class Window:
    def __init__(self, root):
        self.root = root
        root.title("Contact Tracing")
        root.geometry()
        self.browse_button = tk.Button(
            master=root, 
            text="Browse files", 
            command=self.browse_files
        )
        self.execute_button = tk.Button(
            master=root,
            text="Begin Contact Tracing",
            command=self.contact_tracing
        )
        self.positive_attendee_id_entry = tk.Entry(
            master=root
        )
        self.positive_attendee_id_entry.insert(0, 'INFECT001')
        self.positive_confirmed_date = DateEntry(master=root)


        self.browse_button.pack()
        self.positive_attendee_id_entry.pack()
        self.positive_confirmed_date.pack()
        self.execute_button.pack()
    
    def browse_files(self):
        self.filenames = tk.filedialog.askopenfilenames(
            initialdir = str(Path.cwd()),
            title = "Select a File",
            filetypes = (("Excel Files",
            ".xlsx .xls"),
            ("all files",
            "*.*"))
        )
    
    def contact_tracing(self):
        self.df = read_excel(self.filenames)
        self.df = data_preprocessing(self.df)
        positive_attendee_id = self.positive_attendee_id_entry.get() 
        positive_attendee_appointments = self.df.query(
            "Attendees_User_ID == @positiveAttendeeID"
        )
        contact_conditions = positive_attendee_appointments.filter(
            items=['Appointment_Time', 'Location']
        )

        self.display_table(positive_attendee_appointments)
    
    
    def display_table(self, df):
        f = tk.Frame(self.root)
        f.pack()
        self.table = pt = Table(f, dataframe=df,
            showtoolbar=True, showstatusbar=True
        )
        pt.show()
            

def read_excel(filenames):
    df = pd.DataFrame()
    for file in filenames:
        data = pd.read_excel(file)
        df = df.append(data)
    
    return df

def data_preprocessing(df):
    df.columns = df.columns.str.replace(" ","_")
    df.columns = df.columns.str.replace("'","")
    df.Appointment_Time = pd.to_datetime(df["Appointment_Time"])

    return df

      

if __name__ == "__main__":
    root = tk.Tk()   
    Window(root)
    root.mainloop()                                                                                              


