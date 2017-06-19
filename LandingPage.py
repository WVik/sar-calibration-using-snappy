
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename



a = [0 for x in range(10)] #Stores textbox variables
x = [0 for x in range(5)]  #Stores x coordinates
y = [0 for x in range(5)]  #Stores y coordinates


def printData():
    print(a[2].get())
    print("Hello!")
    f2.tkraise()


def selectFile():
    filename = askopenfilename()
    print(filename)
    ttk.Label(mainframe, text=filename+" selected", width=17).grid(column=2, row=1, sticky=W)



def display():
    t = int(num.get())
    for i in range(0,2*t,2):
        ttk.Label(mainframe, text="X"+str((i+2)//2)+" Y"+str((i+2)//2)).grid(column=1,row=i+4,sticky=W)
        a[i] = ttk.Entry(mainframe, width=7)
        a[i].grid(column=2, row=(4+i), sticky=(W,E))
        a[i+1] = ttk.Entry(mainframe, width=7)
        a[i+1].grid(column=3, row=(4+i), sticky=(W,E))
    ttk.Button(mainframe, text="Process Data", command=printData).grid(column=2, row=3+len(a), sticky=W)




root = Tk()
root.title("Calculation of Calibration Constant")

#Frames
f2 = Frame(root)
f2.grid(row=0,column=0,sticky="nsew")


mainframe = ttk.Frame(root)
mainframe.grid(column=4, row=4, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

#Variables
num = StringVar()


#Entries and Grids
number_entry = ttk.Entry(mainframe, width=10, textvariable=num)
number_entry.grid(column=2, row=3, sticky=(W, E))


#Widgets
ttk.Button(mainframe, text="Select Data File", command=selectFile).grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="Number of Ref").grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="Confirm", command=display).grid(column=3, row=3, sticky=W)

ttk.Button(f2, text="Select Data File", command=selectFile).grid(column=1, row=1, sticky=W)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
#root.bind('<Return>', calculate)
mainframe.tkraise()
root.mainloop()