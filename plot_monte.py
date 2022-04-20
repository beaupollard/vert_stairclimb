import matplotlib.pyplot as plt
import numpy as np
import csv
from os.path import exists    
from matplotlib import cm

def Plot_Data(filename,xparms,yparms,disc,titlein,count,pay_ind):
    rows=[]
    inpy2=[]
    inpx2=[]
    fig = plt.figure(figsize=plt.figaspect(0.5))
    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])
                payw=inp[pay_ind]
                inpy=[]
                inpx=[]
                if inp[0]==1:
                    inpy.append(1)
                else:
                    inpy.append(0)
                for j in yparms:
                    if len(inp)>j:
                        inpy.append(inp[j])
                    else:
                        inpy.append(0)
                for j in xparms:
                    if len(inp)>j:
                        inpx.append(inp[j])
                    else:
                        inpx.append(0)
                inpy2.append(inpy)
                inpx2.append(inpx)
                rows.append(row)
        inpy=np.array(inpy2)
        inpx=np.array(inpx2)
    for i in range(len(xparms)):
        
        plt.figure(i+count)
        plt.suptitle(titlein+' '+str(payw)+' kg')
        for j in range(len(yparms)):
            
            
            
            plt.subplot(len(yparms)/2, len(yparms)/2, j+1)
            for k in range(len(inpx[:,0])):
                if inpy[k,0]==1:
                    plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # if inpx[k,0]==3:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # elif inpx[k,0]==4:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'r.')
                    # else:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'g.')
                else:
                    plt.plot(inpx[k,i],inpy[k,j+1],'r.')

            plt.xlabel(disc[xparms[i]-1])
            plt.ylabel(disc[yparms[j]-1])
        
def Plot_Stable_Area(filename,xparms,yparms,disc,titlein,count,pay_ind):
    rows=[]
    inpy2=[]
    inpx2=[]
    fig = plt.figure(figsize=plt.figaspect(0.5))
    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])
                payw=inp[pay_ind]
                inpy=[]
                inpx=[]
                if inp[0]==1:
                    inpy.append(1)
                else:
                    inpy.append(0)
                for j in yparms:
                    if len(inp)>j:
                        inpy.append(inp[j])
                    else:
                        inpy.append(0)
                for j in xparms:
                    inpx.append(inp[j])
                inpy2.append(inpy)
                inpx2.append(inpx)
                rows.append(row)
        inpy=np.array(inpy2)
        inpx=np.array(inpx2)
    for i in range(len(xparms)):
        
        plt.figure(i+count)
        plt.suptitle(titlein+' '+str(payw)+' kg')
        for j in range(len(yparms)):
            
            
            if len(yparms)==2:
                plt.subplot(2, 1, j+1)
            elif len(yparms)==1:
                plt.subplot(1, 1, j+1)
            else:
                plt.subplot(len(yparms)/2, len(yparms)/2, j+1)
            for k in range(len(inpx[:,0])):
                if inpy[k,0]==1:
                    plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # if inpx[k,0]==3:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # elif inpx[k,0]==4:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'r.')
                    # else:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'g.')
                else:
                    plt.plot(inpx[k,i],inpy[k,j+1],'r.')

            plt.xlabel(disc[xparms[i]-1])
            plt.ylabel(disc[yparms[j]-1])

## for planetary dolly ##
# 1 : sub_radius    2 : wheel_num   3 : radius  4 : wheelbase   5 : payloadx    6 : payloadz    7 : step_rise
# 8 : step_slope    9 : payload_weight  10 : sim time   11 : speed [steps/min]  12 : mass   13 : max power  14-end : max torque 
# disc=['sub_rad','num_wheel','radius','wheelbase','paylocx','paylocz','step_rise','step_slope','pay_weight','sim time','speed','mass','max power','max torque']
# path = 'Wheel_Monte/'
# filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
# count=0
# for i in range(4):
#     Plot_Data(path+filenamelist[i],[2,3],[7,2,13,14],disc,disc[8],count)
#     count=count+2
# plt.show()


## for wheeled ##
# 1 : radius    2 : wheelbase   3 : payloadx  4 : payloadz   5 : step_rise    6 : step_slope    7 : payload_weight
# 8 : sim time    9 : speed [steps/min]  10 : mass  11 : max power  12 : average power   13 : power sum  14-end : max torque 
disc=['radius','wheelbase','payloadx','payloadz','step_rise','step_slope','payload_weight','sim_time','speed','mass','max power','average power','power sum','max torque']
path = 'Wheel_Monte/V1'
filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
count=0
for i in range(4):
    # Plot_Data(path+filenamelist[i],[12],[3,4,12,14],disc,disc[7],count,7)
    Plot_Stable_Area(path+filenamelist[i],[3],[4],disc,disc[7],count,7)
    count=count+1
plt.show()