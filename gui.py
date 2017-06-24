from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename

a = [0 for x in range(14)] #Stores textbox variables for x and y coordinates of reflectors


# Functions -----------------------------------------------------------------
def display():   #
    t = int(num.get())
    for i in range(0,2*t,2):
        tk.Label(mainframe, text="X"+str((i+2)//2)+" Y"+str((i+2)//2)).grid(column=1,row=i+8,sticky=W)
        a[i] = tk.Entry(mainframe, width=7)
        a[i].grid(column=2, row=(8+i), sticky=(W,E))
        a[i+1] = tk.Entry(mainframe, width=7)
        a[i+1].grid(column=3, row=(8+i), sticky=(W,E))
    tk.Button(mainframe, text="Process Data", command=processData).grid(column=2, row=3+len(a), sticky=W)


def processData():
    global a
    global filename
    #Add function here to do further processing of data (Calculation of Calibration Constant)


def calculate(*args):
    try:
        freq = float(frequency.get())
        len = float(length.get())
        c=3*(10**8)
        freq=freq*(10**6)
        lambd=c/freq
        num = (4*3.14)*(len**4)
        den = 3*(lambd**2)
        sigma.set(num/den)
    except ValueError:
        pass


def selectFile():
    global filename
    #print(filename)
    filename = askopenfilename()
    print(filename)
    tk.Label(mainframe, text=filename+" selected", width=15).grid(column=2, row=1, sticky=W)

#-----------------------------------------------------------------------------------------------------------

#----------------Headers------------------------

root = Tk()
root.title("Calculation of Calibration Constant")
mainframe = tk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#----------------------------------------------------

#---------------Variables----------------------------

feet = StringVar()
meters = StringVar()
length = StringVar()
frequency = StringVar()
sigma = StringVar()
pagr = StringVar()
alpha = StringVar()
num=StringVar()

#----------------------------------------------------

#Entries-------------TextFields and Grids----------------------
pagr_entry = tk.Entry(mainframe, width=7, textvariable=pagr)
length_entry = tk.Entry(mainframe, width=7, textvariable=length)
frequency_entry = tk.Entry(mainframe, width=7, textvariable=frequency)
alpha_entry = tk.Entry(mainframe, width=7, textvariable=alpha)
number_entry = tk.Entry(mainframe, width=7, textvariable=num)

#Grids for entries
frequency_entry.grid(column=2, row=3, sticky=(W,E))
pagr_entry.grid(column=2, row=5, sticky=(W, E))
alpha_entry.grid(column=2, row=6, sticky=(W, E))
length_entry.grid(column=2, row=2, sticky=(W, E))
number_entry.grid(column=2, row=7, sticky=(W,E))

#---------------------------------------------------------


#Widgets------------Contains Labels and Buttons------------------------------------
tk.Button(mainframe, text="Select Dataset", command=selectFile).grid(column=1, row=1, sticky=W)

tk.Label(mainframe, text="Length of Side").grid(column=1, row=2, sticky=W)
tk.Label(mainframe, text="Meters").grid(column=3, row=2, sticky=W)

tk.Label(mainframe, text="Frequency in MHz").grid(column=1, row=3, sticky=W)
tk.Label(mainframe, text="MHz").grid(column=3, row=3, sticky=W)

tk.Button(mainframe, text="Calculate RCS", command=calculate).grid(column=1, row=4, sticky=E)
tk.Label(mainframe, textvariable=sigma).grid(column=3, row=4, sticky=(W, E))

tk.Label(mainframe, text="Value of Pagr").grid(column=1, row=5, sticky=W)
tk.Label(mainframe, text="in Metres^2").grid(column=3, row=5, sticky=W)

tk.Label(mainframe, text="Alpha").grid(column=1, row=6, sticky=W)
tk.Label(mainframe, text="Degrees").grid(column=3, row=6, sticky=W)

tk.Label(mainframe, text="Number of Ref").grid(column=1, row=7, sticky=W)
tk.Button(mainframe, text="Confirm", command=display).grid(column=3, row=7, sticky=W)


#------------------------------------------------------------------------------------


# Padding for the window.
for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

length_entry.focus()

root.bind('<Return>', calculate)

root.mainloop()