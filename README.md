# Tracer
The Tracer application allows for automated contact tracing from spreadsheet attendance registers. The current implementation assumes a standard format that is exported by the Vula sign-up tool. 

The standard format appears as follows  (highlights have been manually added and some unimportant columns hidden):
![](https://github.com/jdsonza/tracer/blob/main/docs/images/test_sheet_screenshot.png)
  
You should note the infected person highlighted red, person's in contact with a probable or confirmed case highlighted orange, and person's with no recorded contact highlighted in green.

According to the World Health Organization ([source](https://www.who.int/publications/i/item/contact-tracing-in-the-context-of-covid-19)):  
A contact is a person who has had any one of the following exposures to a probable or confirmed case:
1. face-to-face contact with a probable or confirmed case within 1 meter and for at least 15 minutes;
2. direct physical contact with a probable or confirmed case;
3. direct care for a patient with probable or confirmed COVID-19 disease without the use of recommended PPE; or
4. other situations as indicated by local risk assessments

The Tracer tool will collected the details for individuals that have been in contact with an infected person 14 days before the start of symptoms (or date of diagnosis for asymptomatic cases). You can then export the data to .csv, .xlsx or .pickle files for further analysis.

# Requirements
* This release requires the Windows operating system.
* At the moment you will also need attendance schedules in the same format as the Vula Sign-up tool. Documentation for how to set that up is [here](https://github.com/jdsonza/tracer/blob/main/docs/Setting%20up%20the%20Vula%20Sign-up%20Tool.pdf). Updates will be made to allow for other spreadsheet formatting.

# Setup
1. Download the `tracer.exe` file ![here](https://github.com/jdsonza/tracer/releases). See the screenshot below for an example.
   ![](https://github.com/jdsonza/tracer/blob/main/docs/images/exe_location.png)
2. Double-click the downloaded file to launch it. *It takes a while to load as you can see in the GIF further down. 

# Usage
1. Click the "Browse Files" button and select all of the attendance schedule spreadsheets you wish to perform the contact tracing on. e.g. You should know which courses a particular student takes and would only need to use the attendance schedules from those select courses. 
2. Enter the Campus ID of the infected person (probable or confirmed)
3. Enter the date on which the infected person first started showing symptoms (or from the date of diagnosis for asymptomatic cases)
4. You may uncheck the "Show unique contacts" checkbox if you wish export all contact events.
5. Click "Begin contact tracing" to start the process.
6. Once the contact tracing process is complete you will be allowed to export the data. You may choose .xlsx, .csv or .pickle filetypes. 
7. You can analyse the data further in spreadsheet tools such as Excel.

# Demonstration
Here's a GIF of performing contact tracing:

![](https://github.com/jdsonza/tracer/blob/main/docs/images/tracer_use_gif.gif)

Viewing the exported data:

![](https://github.com/jdsonza/tracer/blob/main/docs/images/results_open_gif.gif)
