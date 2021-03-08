from pathlib import Path
import tkinter as tk
import tkinter.filedialog
from tkcalendar import DateEntry

import pandas as pd 
from pandastable import Table, TableModel


class Window:
    def __init__(self, root, n_prior_days):
        self.n_prior_days = n_prior_days
        self.root = root
        root.title("Contact Tracing")
        root.geometry()

        self.selected_files_label = tk.Label(
            root,
            text="Select course register sheets"
        )

        browse_button = tk.Button(
            root, 
            text="Browse files", 
            command=self.browse_files
        )

        execute_button = tk.Button(
            root,
            text="Begin Contact Tracing",
            command=self.contact_tracing
        )
        
        positive_attendee_label = tk.Label(
            root, 
            text='Campus ID of positive member:'
        )
        self.positive_attendee_id_entry = tk.Entry(root)
        self.positive_attendee_id_entry.insert(0, 'INFECT001')

        positive_confirmed_date_label = tk.Label(
            root, 
            text='Date of confirmed infection:'
        )
        self.positive_confirmed_date = DateEntry(master=root)
        
        self.filter_unique_var = tk.IntVar(value=1)
        filter_unique_button = tk.Checkbutton(
            root,
            text='Show unique contacts',
            variable=self.filter_unique_var
        )

        #Widget layout
        
        self.selected_files_label.grid(row=0, column=0, sticky='W', 
            padx=(5,5), pady=(5,5))
        browse_button.grid(row=0, column=1, sticky='W', 
            padx=(5,5), pady=(5,5))
        positive_attendee_label.grid(row=1, column=0, sticky='W', 
            padx=(5,5), pady=(5,5))
        self.positive_attendee_id_entry.grid(row=1, column=1, sticky='W', 
            padx=(5,5), pady=(5,5))
        positive_confirmed_date_label.grid(row=2, column=0, sticky='W',     
            padx=(5,5), pady=(5,5))
        self.positive_confirmed_date.grid(row=2, column=1, sticky='W', 
            padx=(5,5), pady=(5,5))
        filter_unique_button.grid(row=3, column=0, sticky='W', 
            padx=(5,5), pady=(5,5))
        execute_button.grid(row=4, column=0, sticky='W,S', 
            padx=(5,5), pady=(5,5))

        
    def browse_files(self):
        self.filenames = tk.filedialog.askopenfilenames(
            initialdir = str(Path.cwd()),
            title = "Select Files",
            filetypes = (("Excel Files", ".xlsx .xls"), ("all files","*.*"))
        )

        short_names = []
        for filename in self.filenames:
            short_names.append(str(Path(filename).name))

        self.selected_files_label.config(text=short_names)
    

    def contact_tracing(self):
        self.df = read_excel(self.filenames)
        self.df = data_cleaning(self.df)

        positive_attendee_id = self.positive_attendee_id_entry.get() 
        positive_attendee_appointments = self.df.query(
            "Attendees_User_ID == @positive_attendee_id"
        )

        contact_conditions = positive_attendee_appointments[
            ['Appointment_Time', 'Location']
        ]
        
        all_contact_events = self.df[
                        self.df['Appointment_Time'].isin(
                            contact_conditions.values[:, 0]
                        ) 
                        & self.df['Location'].isin(
                            contact_conditions.values[:, 1]
                        )
        ]

        contact_trace_start_date = pd.Timestamp(
            self.positive_confirmed_date.get_date()) \
            - pd.Timedelta(self.n_prior_days)

        recent_contact_events = all_contact_events[
            all_contact_events.Appointment_Time 
            > contact_trace_start_date
        ]
        
        if self.filter_unique_var.get():
            recent_contact_events = recent_contact_events.drop_duplicates(
                subset=["Attendees_User_ID"]
            )

        self.display_table(recent_contact_events)
    
    
    def display_table(self, df):
        f = tk.Frame(self.root)
        f.grid(row=5, column=1, rowspan=3, sticky='s')
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


def data_cleaning(df):
    df.columns = df.columns.str.replace(" ","_")
    df.columns = df.columns.str.replace("'","")
    df.Appointment_Time = pd.to_datetime(df["Appointment_Time"])

    return df

      
if __name__ == "__main__":
    root = tk.Tk()   
    Window(root, n_prior_days=14)
    root.mainloop()                                                                                              


