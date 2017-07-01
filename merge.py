from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
import math
import snappy
from snappy import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

intensityArray = []
a = [0 for x in range(14)] #Stores textbox variables
coordinateArray=[]
sigma=0
k_VH=[]
filename="0"

# Functions -----------------------------------------------------------------
def display():   #
    t = int(num.get())
    for i in range(0,2*t,2):
        tk.Label(mainframe, text="X"+str((i+2)//2)+" Y"+str((i+2)//2)).grid(column=1,row=i+8,sticky=W)
        a[i] = tk.Entry(mainframe, width=15)
        a[i].grid(column=2, row=(8+i), sticky=(W,E))
        a[i+1] = tk.Entry(mainframe, width=15)
        a[i+1].grid(column=3, row=(8+i), sticky=(W,E))
    tk.Button(mainframe, text="Process Data", command=processData).grid(column=2, row=3+len(a), sticky=W)



# This function creates a new window for computations--------------------------------------------------------------

#Functions: 1) To calculate sigma (Radar Cross Section)
#           2) To start the process to calculate K. Call helper functions.
def processData():
    global a
    global filename
    print("Hello!")
    newframe=tk.Toplevel(root)
    calculateSigma()   #Calculate Radar Cross Section
    createCoordinateArray() #Creates array for X and Y coordinates of reflectors.
    findK(newframe)
    for child in newframe.winfo_children(): child.grid_configure(padx=10, pady=10)



#-------------------------------------------------------------------------------------------------------------------
def createCoordinateArray():
    global coordinateArray
    global a
    k=int(num.get())
    k=int(k)*2
    for i in range(0,k,2):
        coordinateArray.append(((a[i].get()),int(a[i+1].get())))
    print(coordinateArray)

#================================================= Function to do all calculations of K=========================================

def findK(newframe):
    global intensityArray
    n=int(num.get())
    global coordinateArray
    global k_VH
    global filename
    
    for i in range(n):
        #importing product
        p=ProductIO.readProduct('C:/Users/abhishek/Desktop/whole.dim')
        
        BandNames=list(p.getBandNames())#function to create array of BandNames
        
        HashMap = jpy.get_type('java.util.HashMap')
        GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
        parameters = HashMap()
        parameters.put('copyMetadata', True)
        
        
        #creating subset
        a=int(coordinateArray[i][0])-63
        b=int(coordinateArray[i][1])-63
        a=str(a)
        b=str(b)
        parameters.put('region', "%s,%s,128,128"%(a,b) )
        subset = GPF.createProduct('Subset', parameters, p)
        Inty_VH = subset.getBand('Intensity_VH')
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        
        #-----------------------Creating 4 subsets for Background Correction------------------------
        #creating more subset 10 x 10 for background correction
        parameters.put('region', "10,10,10,10")
        subset1 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset1.getBand('Intensity_VH')
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a1=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b1=(arr_sum(a1))
        
        
        parameters.put('region', "10,100,10,10")
        subset2 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset2.getBand('Intensity_VH')
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a2=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b2=(arr_sum(a2))
        
        
        parameters.put('region', "100,10,10,10")
        subset3 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset3.getBand('Intensity_VH')
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a3=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b3=(arr_sum(a3))
        
        
        parameters.put('region', "100,100,10,10")
        subset4 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset4.getBand('Intensity_VH')
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a4=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b4=(arr_sum(a4))
        
        sum_bm=(sum_b1+sum_b2+sum_b3+sum_b4)/400
        print(sum)
        
        #--------------------------------------------------------------------
        
        #creating subset 20 x 20 to calculate Ip
        parameters.put('region', "53,53,20,20")
        subset20 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset20.getBand('Intensity_VH')
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a20=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        
        arr20=[]  #Converting a20 into a 2D array(20*20) for plotting purpose
        for i in range(0,400,20):
            temp=[]
            for j in range(20):
                temp.append(a20[i+j])
            arr20.append(temp)
        
        intensityArray.append(arr20)  #intensityArray is the array of 2D arrays for plotting multiple reflectors

        for i in range(len(a20)):
            a20[i]=a20[i]-sum_bm
        Ip=arr_sum(a20)
        alph=float(alpha.get())
        Pag=float(Pagr.get())
        K_VH=10*math.log10((Ip*Pag*math.sin(alph*math.pi/180))/sigma)
        k_VH.append(K_VH)
    
    i=0
    k=0
    while i<len(k_VH):
        k=k+k_VH[i]
        i=i+1
    print('K_VH= '+str(k/len(k_VH)))
    tk.Label(newframe, text="Calculated K value").grid(column=1, row=1, sticky=W)
    tk.Label(newframe, text=" = " + str(k/len(k_VH))).grid(column=1, row=2, sticky=W)
    addPlotButtons(newframe,len(k_VH))

#==================================================================================================

def addPlotButtons(newframe,length):
    tk.Label(newframe, text="Plots of the corner reflectors").grid(column=2,row=2,sticky=W)
    for i in range(length):
        tk.Button(newframe, text="Reflector ", command=lambda:plotReflector(i)).grid(column=(i)%2+1, row=3+(i)//2, sticky=W)


def plotReflector(i):
    global intensityArray
    i = int(i)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(0, 20, 1)
    X, Y = np.meshgrid(x, y)
    zs = np.array([z[1][x][y] for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)
    surf = ax.plot_surface(X, Y, Z)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap='Reds',linewidth=0.5, antialiased=False)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()



#======================================================================================================


def arr_sum(arr):
    i=0
    sum=0
    while i<len(arr):
        sum=sum+arr[i]
        i=i+1
    return sum

def calculateSigma(*args):
    global sigma
    try:
        freq = float(frequency.get())
        len = float(length.get())
        c=3*(10**8)
        freq=freq*(10**6)
        lambd=c/freq
        num = (4*3.14159)*(len**4)
        den = 3*(lambd**2)
        sigma=(num/den)
        print(sigma)
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
Pagr = StringVar()
alpha = StringVar()
num=StringVar()

#----------------------------------------------------

#Entries-------------TextFields and Grids----------------------
Pagr_entry = tk.Entry(mainframe, width=7, textvariable=Pagr)
length_entry = tk.Entry(mainframe, width=7, textvariable=length)
frequency_entry = tk.Entry(mainframe, width=7, textvariable=frequency)
alpha_entry = tk.Entry(mainframe, width=7, textvariable=alpha)
number_entry = tk.Entry(mainframe, width=7, textvariable=num)

#For snappy--------


#Grids for entries
frequency_entry.grid(column=2, row=3, sticky=(W,E))
Pagr_entry.grid(column=2, row=5, sticky=(W, E))
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

#tk.Button(mainframe, text="Calculate RCS", command=calculate).grid(column=1, row=4, sticky=E)
#tk.Label(mainframe, textvariable=sigma).grid(column=3, row=4, sticky=(W, E))

tk.Label(mainframe, text="Value of Pagr").grid(column=1, row=5, sticky=W)
tk.Label(mainframe, text="in Metres^2").grid(column=3, row=5, sticky=W)

tk.Label(mainframe, text="Alpha").grid(column=1, row=6, sticky=W)
tk.Label(mainframe, text="Degrees").grid(column=3, row=6, sticky=W)

tk.Label(mainframe, text="Number of Ref").grid(column=1, row=7, sticky=W)
tk.Button(mainframe, text="Confirm", command=display).grid(column=3, row=7, sticky=W)


#------------------------------------------------------------------------------------


# Padding for the window.
for child in mainframe.winfo_children(): child.grid_configure(padx=15, pady=15)

length_entry.focus()

#root.bind('<Return>', calculate)

root.mainloop()