#importing all libraries from snappy

print('.................................Please wait till program loads.........................\n')
import math
import snappy
from snappy import *
import numpy as np

#getting no. of corner reflector from user 
n=input('Enter no. of corner reflector\n')

n=int(n)

#making an array of position of all corner reflector
pos_arr=[]

l=input('Enter length of one resolution cell\n')
l=int(l)
Pagr=(l*l)
L,lambd,alpha=input('Enter input in format length of corner reflector<space>wavelength og radation<>angle of incidence\n').strip().split()
L=float(L)
lambd=float(lambd)
alpha=float(alpha)
sigma=(4*math.pi*(L**4))/(3*(lambd**2))
print('enter the position of corner reflector in format x y')
for i in range(n):
    x,y=input().strip().split()
    pos_arr.append((x,y))
print('please wait till data is processed')
#making array for k
k_VH=[]
#defining a method for sum of array
def arr_sum(arr):
    i=0
    sum=0
    while i<len(arr):
        sum=sum+arr[i]
        i=i+1
    return (sum)
for i in range(n):
    #importing product
    p=ProductIO.readProduct('C:/Users/abhishek/Desktop/whole.dim')

    BandNames=list(p.getBandNames())#function to create array of BandNames
    
    HashMap = jpy.get_type('java.util.HashMap')
    GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
    parameters = HashMap()
    parameters.put('copyMetadata', True)


#creating subset
    a=int(pos_arr[i][0])-63
    b=int(pos_arr[i][1])-63
    a=str(a)
    b=str(b)
    parameters.put('region', "%s,%s,128,128"%(a,b) )
    subset = GPF.createProduct('Subset', parameters, p)
    Inty_VH = subset.getBand('Intensity_VH')
    w = Inty_VH.getRasterWidth()
    h = Inty_VH.getRasterHeight()
    Inty_VH_data = np.zeros(w * h, np.float32)
   
    
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

    #creating subset 20 x 20 to calculate Ip
    parameters.put('region', "53,53,20,20")
    subset20 = GPF.createProduct('Subset', parameters, subset)
    Inty_VH = subset20.getBand('Intensity_VH')
    w = Inty_VH.getRasterWidth()
    h = Inty_VH.getRasterHeight()
    Inty_VH_data = np.zeros(w * h, np.float32)
    a20=Inty_VH.readPixels(0, 0, w, h, Inty_VH_data)
    for i in range(len(a20)):
        a20[i]=a20[i]-sum_bm
    Ip=arr_sum(a20)
   
    K_VH=10*math.log10((Ip*Pagr*math.sin(alpha*math.pi/180))/sigma)
    k_VH.append(K_VH)

i=0
k=0
while i<len(k_VH):
    k=k+k_VH[i]
    i=i+1
print('K_VH= '+str(k/len(k_VH)))    
input('<PRESS \'ENTER\' TO EXIT>')



