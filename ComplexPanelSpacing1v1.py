#To Do: add new functions: - VocMax Calculator
#                           - Including Machine learning to retrieve required/all data from various panel manufacturers datasheets
#                         - Earth Size Calculator
#                         - Tensioning Guide
#                         - Clamp Zone Guide
# - Make into a webapp or phone app - streamable




#Import the required Libraries
from tkinter import *
from tkinter import ttk
import math
import numpy as np
import pandas as pd
import pvlib
from pvlib.location import Location, solarposition
from timezonefinder import TimezoneFinder
import pgeocode

obj = TimezoneFinder()
#define country code for postcode-co-ords lookup
nomi = pgeocode.Nominatim('au')
#Create an instance of Tkinter frame
win = Tk()
win.title('Solar Panel Tilt Spacing Finder by Ryan Akers')
#Set the geometry of Tkinter frame
win.geometry("550x150")

def display_text():
   global LG
   global PA
   global RA
   global PC
   #global Azi
   #global Alt
   LG = entry1.get()
   PA = entry2.get()
   RA = entry3.get()
   PC = entry4.get()
   lat = nomi.query_postal_code(PC)[9]
   print('Latitude: ' + str(lat))
   lon = nomi.query_postal_code(PC)[10]
   print('Longitude: ' + str(lon))
   tz = obj.timezone_at(lng=lon, lat=lat)
   time = '2022-06-21 10:00:00'
   print('Time: '+ str(time))
   Simtime = pd.date_range(time,time, tz=tz)
   solpos = pvlib.solarposition.get_solarposition(Simtime, lat, lon)
   Azi = np.abs(solpos['azimuth']).max()
   print('Azimuth: ' + str(Azi))
   Alt = np.abs(solpos['elevation']).max()
   print('Altitude: ' + str(Alt))
   A = math.cos(math.radians(int(Azi)))
   B = math.tan(math.radians(int(Alt)+int(RA)))
   C = A/B
   D = math.sin(math.radians(int(PA)-int(RA)))*int(LG)
   Spacing = str(int(D*C)) + "mm"
   label.configure(text=Spacing)

#Create an Entry widget to get panel length
l1=Label(win, text="Enter Panel Length (mm): ")
l1.grid(sticky="E",row=1,column=1)
entry1= Entry(win, width= 40)
entry1.focus_set()
entry1.grid(row=1,column=2)

#Create an Entry widget to get panel installation angle
l2=Label(win, text="Enter Panel Angle (from Horizontal) (deg): ")
l2.grid(sticky="E",row=2,column=1)
entry2= Entry(win, width= 40)
entry2.grid(row=2,column=2)

#Create an Entry widget to get Roof Angle
l3=Label(win, text="Enter Roof Angle (deg): ")
l3.grid(sticky="E",row=3,column=1)
entry3= Entry(win, width= 40)
entry3.grid(row=3,column=2)

# Create an Entry widget to get Postcode
l4=Label(win, text="Enter Installation Location Postcode: ")
l4.grid(sticky="E",row=4,column=1)
entry4 = Entry( win , width=40)
entry4.grid(row=4, column=2)

#Initialize a Label to display the User Input
label=Label(win, text="", font=("Courier 22 bold"))
label.grid(row=5,column=2)

#Create a Button to validate Entry Widget
ttk.Button(win, text= "Calculate",width= 20, command= display_text).grid(sticky="E",row=5,column=1)

#Initialize a Label to display the version number
version=Label(win, text="v1.1", font=("Arial 6"))
version.grid(sticky ="E", row=6, column=3)

win.mainloop()
