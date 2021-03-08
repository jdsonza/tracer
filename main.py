from pathlib import Path
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
from tkcalendar import DateEntry

import pandas as pd 
from pandastable import Table, TableModel


class Window:
    def __init__(self, root, n_prior_days):
        self.n_prior_days = n_prior_days
        self.root = root
        root.title("Contact Tracing")
        root.geometry()

        self.top_frame = tk.Frame(root)
        self.bottom_frame = tk.Frame(root)

        self.top_frame.grid(row=0, sticky='nw')
        self.bottom_frame.grid(row=1)

        self.selected_files_label = tk.Message(
            self.top_frame,
            text="Select course register sheets:",
            width=180
        )

        browse_button = tk.Button(
            self.top_frame, 
            text="Browse files", 
            command=self.browse_files
        )

        execute_button = tk.Button(
            self.top_frame,
            text="Begin Contact Tracing",
            command=self.contact_tracing
        )
        
        positive_attendee_label = tk.Label(
            self.top_frame, 
            text='Campus ID of positive member:'
        )
        self.positive_attendee_id_entry = tk.Entry(self.top_frame)
        self.positive_attendee_id_entry.insert(0, 'INFECT001')

        positive_confirmed_date_label = tk.Label(
            self.top_frame, 
            text='Date of confirmed infection:'
        )
        self.positive_confirmed_date = DateEntry(self.top_frame)
        
        self.filter_unique_var = tk.IntVar(value=1)
        filter_unique_button = tk.Checkbutton(
            self.top_frame,
            text='Show unique contacts',
            variable=self.filter_unique_var
        )

        self.export_button = tk.Button(
            self.top_frame,
            text='Export',
            command=self.export_df,
            state='disabled'
        )

        #Widget layout
        
        self.selected_files_label.grid(row=0, column=0, sticky='w', 
            padx=(5,5), pady=(5,5))
        browse_button.grid(row=0, column=1, sticky='w', 
            padx=(5,5), pady=(5,5))
        positive_attendee_label.grid(row=1, column=0, sticky='w', 
            padx=(5,5), pady=(5,5))
        self.positive_attendee_id_entry.grid(row=1, column=1, sticky='w', 
            padx=(5,5), pady=(5,5))
        positive_confirmed_date_label.grid(row=2, column=0, sticky='w', 
            padx=(5,5), pady=(5,5))
        self.positive_confirmed_date.grid(row=2, column=1, sticky='w', 
            padx=(5,5), pady=(5,5))
        filter_unique_button.grid(row=3, column=0, sticky='w', 
            padx=(5,5), pady=(5,5))
        execute_button.grid(row=4, column=0, sticky='w', 
            padx=(5,5), pady=(5,5))
        self.export_button.grid(row=4, column=1, sticky='w', 
            padx=(5,5), pady=(5,5))

        
    def browse_files(self):
        self.filenames = tk.filedialog.askopenfilenames(
            initialdir = str(Path.cwd()),
            title = "Select Files",
            filetypes = (("Excel Files", ".xlsx .xls"), ("all files","*.*"))
        )

        short_names = []
        for filename in self.filenames:
            short_names.append(str(Path(filename).name + ','))

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

        self.recent_contact_events = all_contact_events[
            all_contact_events.Appointment_Time 
            > contact_trace_start_date
        ]
        
        if self.filter_unique_var.get():
            self.recent_contact_events = self.recent_contact_events.drop_duplicates(
                subset=["Attendees_User_ID"]
            )

        self.display_table(self.recent_contact_events)
        self.export_button.config(state='normal')
    
    
    def display_table(self, df):
        self.table = pt = Table(
            self.bottom_frame, 
            dataframe=df,
            width=500, 
            height=200,
            showtoolbar=True, 
            showstatusbar=True
        )
        pt.show()


    def export_df(self):
        #export dataframe
        save_filename = tk.filedialog.asksaveasfilename(
            defaultextension='*.', 
            filetypes=(
                ('Excel files', '*.xlsx'), 
                ('CSV files', '*.csv'), 
                ('Pickle files', '*.pkl')
            )
        )
        
        if save_filename != '':
            try:
                if (Path(save_filename).suffix == '.xlsx'):
                    self.recent_contact_events.to_excel(save_filename, index=False)      
                elif (Path(save_filename).suffix == '.csv'):
                    self.recent_contact_events.to_csv(save_filename, index=False)
                elif (Path(save_filename).suffix == '.pkl'):
                    self.recent_contact_events.to_pickle(save_filename)
            except Exception as err:
                tk.messagebox.showerror(title='Error', message='Unexpected error: ' + str(err))
            else:     
                tk.messagebox.showinfo(title='File Saved', message='File exported') 


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


