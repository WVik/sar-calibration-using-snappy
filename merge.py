from tkinter import *
import datetime
import tkinter as tk
from tkinter.filedialog import askopenfilename
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
import os
import snappy
from snappy import jpy
from snappy import GPF
from snappy import ProductIO


desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
curr_time = str(datetime.datetime.now())
curr_time = curr_time.replace(':','_')
new_time=curr_time.split()
newtime = new_time[0]+new_time[1]
savefile=open('%s\log_%s.txt'%(desktop,str(newtime)),'w')
selectedBand=" "
#savefile=open("%s\log_"+str(newtime)+'.txt','w')

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
        tk.Label(mainframe, text="X"+str((i+2)//2)+" Y"+str((i+2)//2)).grid(column=1,row=i+9,sticky=W)
        a[i] = tk.Entry(mainframe, width=15)
        a[i].grid(column=2, row=(9+i), sticky=(W,E))
        a[i+1] = tk.Entry(mainframe, width=15)
        a[i+1].grid(column=3, row=(9+i), sticky=(W,E))
    tk.Button(mainframe, text="Process Data", command=processData).grid(column=2, row=3+len(a), sticky=W)
    for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)



# This function creates a new window for computations--------------------------------------------------------------

#Functions: 1) To calculate sigma (Radar Cross Section)
#           2) To start the process to calculate K. Call helper functions.
def processData():
    global a
    global filename
    newframe=tk.Toplevel(root)
    calculateSigma()   #Calculate Radar Cross Section
    createCoordinateArray() #Creates array for X and Y coordinates of reflectors.
    findK(newframe)
    for child in newframe.winfo_children(): child.grid_configure(padx=10, pady=10)



#-------------------------------------------------------------------------------------------------------------------
def createCoordinateArray():
    global coordinateArray
    coordinateArray=[]
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
    global OpMenu
    for i in range(n):
        #importing product
        if(i==0):
            k_VH=[]
        p=ProductIO.readProduct(filename)
        selectedBand= str(OpMenu.get())
        BandNames=list(p.getBandNames())#function to create array of BandNames
        
        HashMap = jpy.get_type('java.util.HashMap')
        GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
        parameters = HashMap()
        parameters.put('copyMetadata', True)
        
        savefile.write('coordinate'+str(i+1)+' is'+" ("+str(coordinateArray[i][0]+","+str(coordinateArray[i][1])+")\n\n"))
        #creating subset
        a=int(coordinateArray[i][0])-63
        b=int(coordinateArray[i][1])-63
        a=str(a)
        b=str(b)
        parameters.put('region', "%s,%s,128,128"%(a,b) )
        subset = GPF.createProduct('Subset', parameters, p)
        
        Inty_VH = subset.getBand(selectedBand)
        print(OpMenu.get())
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        

        #creating subset 20 x 20 to calculate Ip
        parameters.put('region', "53,53,20,20")
        subset20 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset20.getBand(selectedBand)
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a20=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        savefile.write('20x20 subset around coordinate'+str(i+1)+" without background intensity correction\n")
        savefile.write('[\n')
        arr20=arr12(a20,20,20)
        savefile.writelines(["%s\n" % item  for item in arr20])
        savefile.write(']\n\n')
        
        #-----------------------Creating 4 subsets for Background Correction------------------------
        #creating more subset 10 x 10 for background correction
        parameters.put('region', "10,10,10,10")
        subset1 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset1.getBand(selectedBand)
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a1=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b1=(arr_sum(a1))
        savefile.write('first 10x10 subset of background\n')
        writef(a1,10,10)
        savefile.write('sum_b1= '+str(sum_b1)+'\n')
        savefile.write('\n')
        
        parameters.put('region', "10,100,10,10")
        subset2 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset2.getBand(selectedBand)
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a2=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b2=(arr_sum(a2))
        savefile.write('second 10x10 subset of background\n')
        writef(a2,10,10)
        savefile.write('sum_b2= '+str(sum_b2)+'\n')
        savefile.write('\n')
        
        parameters.put('region', "100,10,10,10")
        subset3 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset3.getBand(selectedBand)
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a3=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b3=(arr_sum(a3))
        savefile.write('third 10x10 subset of background\n')
        writef(a3,10,10)
        savefile.write('sum_b3= '+str(sum_b3)+'\n')
        savefile.write('\n')

        
        parameters.put('region', "100,100,10,10")
        subset4 = GPF.createProduct('Subset', parameters, subset)
        Inty_VH = subset4.getBand(selectedBand)
        w = Inty_VH.getRasterWidth()
        h = Inty_VH.getRasterHeight()
        Inty_VH_data = np.zeros(w * h, np.float32)
        a4=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
        sum_b4=(arr_sum(a4))
        savefile.write('fourth 10x10 subset of background\n')
        writef(a4,10,10)
        savefile.write('sum_b4= '+str(sum_b4)+'\n')
        savefile.write('\n')
        
        sum_bm=(sum_b1+sum_b2+sum_b3+sum_b4)/400
        savefile.write('mean background intensity= '+str(sum_bm))
        savefile.write('\n')
        print(sum)
        
        #--------------------------------------------------------------------
        
        
        intensityArray.append(arr20)  #intensityArray is the array of 2D arrays for plotting multiple reflectors
        print()
        
        for i in range(len(a20)):
            a20[i]=a20[i]-sum_bm
        arr40=arr12(a20,20,20)
        savefile.write('20x20 subset around coordinate'+str(i+1)+" with background intensity correction\n")
        savefile.write('[\n')
        savefile.writelines(["%s\n" % item  for item in arr40])
        savefile.write(']\n\n')
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
    tk.Label(newframe, text=" = " + str(k/len(k_VH))).grid(column=2, row=1, sticky=W)
    addPlotButtons(newframe,len(k_VH))

#==================================================================================================
def arr12(arr,c1,r1):
    c=0
    i=0
    col=[]
    while c<c1:
        r=0
        row=[]
        while r<r1:
            row.append(arr[i])
            i=i+1
            r=r+1
        col.append(row)
        c=c+1
    return col
def addPlotButtons(newframe,length):
    tk.Label(newframe, text="Plots of the corner reflectors").grid(column=1,row=2,sticky=W)
    for i in range(length):
        tk.Button(newframe, text="Reflector "+str(i+1), command=lambda i=i: plotReflector(i)).grid(column=(i)%2+1, row=3+(i)//2, sticky=W)


def plotReflector(new):
    
    global intensityArray
    
    new = int(new)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(0, 20, 1)
    X, Y = np.meshgrid(x, y)
    zs = np.array([intensityArray[int(new)][int(x)][int(y)] for x,y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)
    surf = ax.plot_surface(X, Y, Z)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap='Reds',linewidth=0.5, antialiased=False)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()



#======================================================================================================
def writef(arr,c1,r1):
    c=0
    i=0
    while c<c1:
        r=0
        while r<r1:
            savefile.write(str(arr[i])+"\t")
            i=i+1
            r=r+1
        savefile.write("\n")    
        c=c+1

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
    global opmenu
    global OpMenu
    #print(filename)
    filename = askopenfilename()
    tk.Label(mainframe, text="File Selected", width=15).grid(column=2, row=1, sticky=W)
    p=ProductIO.readProduct(filename)       
    BandNames=list(p.getBandNames())#function to create array of BandNames
    print(BandNames)
    
    OpMenu.set("Select The Band Name") # default value
    opmenu = OptionMenu(mainframe, OpMenu, BandNames[0],BandNames[1], BandNames[2], BandNames[3]).grid(column=1, row=8)

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
OpMenu = StringVar()

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

tk.Label(mainframe, text="Number of Reflector(s)").grid(column=1, row=7, sticky=W)
tk.Button(mainframe, text="Confirm", command=display).grid(column=3, row=7, sticky=W)


#------------------------------------------------------------------------------------


# Padding for the window.
for child in mainframe.winfo_children(): child.grid_configure(padx=15, pady=15)

length_entry.focus()

#root.bind('<Return>', calculate)

root.mainloop()
savefile.close()
