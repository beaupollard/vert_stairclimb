# from matplotlib.lines import _LineStyle
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

                
                inpy=[]
                inpx=[]
                if inp[0]==1:
                    inpy.append(1)
                    payw=inp[pay_ind]
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
        plt.suptitle('Vehicle Weight '+str(payw*2.20462)+' lbs')
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
                    # plt.plot(inpx[k,i]*39.3701,inpy[k,j+1]*39.3701,'b.')
                    # if inpx[k,0]==3:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'b.')
                    # elif inpx[k,0]==4:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'r.')
                    # else:
                    #     plt.plot(inpx[k,i],inpy[k,j+1],'g.')
                else:
                    # plt.plot(inpx[k,i]*39.3701,inpy[k,j+1]*39.3701,'r.')
                    plt.plot(inpx[k,i],inpy[k,j+1],'r.')

            plt.xlabel(disc[xparms[i]-1])
            plt.ylabel(disc[yparms[j]-1])

def Load_Data(path,filenamelist,pay_ind,rows):
    rows=[]
    inpy2=[]
    inpx2=[]
    # fig = plt.figure(figsize=plt.figaspect(0.5))
    for i in filenamelist:
        filename=path+i
        if exists(filename):
            with open(filename, 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                for row in csvreader:
                    inp=(row[0][:].split(' '))
                    inp = ([float(x) for x in inp])
                    payw=inp[pay_ind]
                    if inp[0]==1:
                        leninp=len(inp)
                        rows=np.append(rows,np.array(inp))
    return np.reshape(rows,(-1,leninp))

def friction_plot(path,filenamelist,pay_ind):
    frictionin=np.linspace(0.1,0.5,10)
    count=0
    fig = plt.figure(figsize=(12, 6))
    for i in filenamelist:
        filename=path+i
        if exists(filename):
            with open(filename, 'r') as file:
                csvreader = csv.reader(file)
                header = next(csvreader)
                for row in csvreader:
                    inp=(row[0][:].split(' '))
                    inp = ([float(x) for x in inp])
                    payw=inp[pay_ind]
                    if inp[0]==1:    
                        plt.plot(int(inp[pay_ind]*2.20462),frictionin[count],'b.',markersize=20)
                    else:
                        plt.plot(int(inp[pay_ind]*2.20462),frictionin[count],'r.',markersize=20)
                    count=count+1
                    if count==len(frictionin):
                        count=0
        fs = 24
        plt.tight_layout()
        plt.xlabel('Vehicle Weight [lbs]',fontsize=fs)
        plt.ylabel('Friction Coefficient',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)        

def Weight_plots(data,xparm,yparm,names,count):
    
    plt.figure(count)
    for i in range(len(data[:,0])):
        if data[i,0]==1:
            plt.plot(data[i,xparm],data[i,yparm],'b.')
        # else:
        #     plt.plot(data[i][xparm],data[i][yparm],'r.')
    # plt.suptitle(titlein+' '+str(payw)+' kg')
    plt.xlabel(disc[xparm-1])
    plt.ylabel(disc[yparm-1])


def Plot_tvp(data,xind,yind,payloadind):
    pay=np.unique(data[:,payloadind])
    colors=['.b','.r','.g','.k']
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind])
                yval.append(data[i,yind])
        plt.plot(xval,yval,colors[k])
        plt.xlabel('Torque [Nm]')
        plt.ylabel('Average Power [W]')

def Plot_tvr(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    fig = plt.figure(figsize=(12, 6))
    # for i in range(len(data[:,0])):
    fs=26
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*39.37/6.85)
                yval.append(max(data[i,yind:])*0.73756214927727)
        plt.plot(xval,yval,colors[k]+sty,linewidth=5)
        plt.xlim([.5, 1.75])
        plt.ylim([30, 150])
        plt.xlabel('Radius/Step Rise',fontsize=fs)
        plt.ylabel('Torque [lbs-ft]',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)
        plt.tight_layout()
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=fs)

def Plot_svr(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    fig = plt.figure(figsize=(12, 6))
    # for i in range(len(data[:,0])):
    fs=26    
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*39.37/6.85)
                yval.append((data[i,yind]*11/10))
        plt.plot(xval,yval,colors[k]+sty,linewidth=3)
        plt.xlim([.5, 1.75])
        # plt.ylim([30, 120])
        plt.tight_layout()
        plt.xlabel('Radius/Step Rise',fontsize=fs)

        plt.ylabel('Speed [step/min]',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=fs)

def Plot_svt(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    # for i in range(len(data[:,0])):

    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*0.73756214927727)
                yval.append((data[i,yind]*11/10))
        plt.plot(xval,yval,colors[k]+sty,linewidth=3)
        # plt.xlim([.5, 1.75])
        # plt.ylim([30, 120])
        plt.xlabel('Radius/Step Rise',fontsize=14)
        plt.ylabel('Speed [step/min]',fontsize=14)
        plt.tick_params(axis='x', labelsize=14)
        plt.tick_params(axis='y', labelsize=14)
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=14)

def Plot_pvr(data,xind,yind,payloadind,sty):
    pay=np.unique(data[:,payloadind])
    colors=['b','r','g','k']
    ideal_p=(6.85)/39.37*pay*9.81
    fig = plt.figure(figsize=(12, 6))
    # for i in range(len(data[:,0])):
    fs=26
    #     plt.plot(data[i,xind],data[i,yind])
    for k in range(len(pay)):
        xval=[]
        yval=[]
        for i in range(len(data[:,0])):
            if data[i,payloadind]==pay[k]:
                xval.append(data[i,xind]*39.37/6.85)
                yval.append((data[i,yind]*4))
        plt.plot(xval,yval,colors[k]+sty,linewidth=5)
        
        plt.xlim([.5, 1.75])
        plt.ylim([50, 800])
        plt.tight_layout()
        plt.xlabel('Radius/Step Rise',fontsize=fs)
        plt.ylabel('Power [W]',fontsize=fs)
        plt.tick_params(axis='x', labelsize=fs)
        plt.tick_params(axis='y', labelsize=fs)
        plt.legend(['Weight = '+str(int(pay[0]*2.20462))+' lbs', 'Weight = '+str(int(pay[1]*2.20462))+' lbs','Weight = '+str(int(pay[2]*2.20462))+' lbs','Weight = '+str(int(pay[3]*2.20462))+' lbs'],fontsize=fs)
    for k in range(len(pay)):
        # ideal_p=(6.85)/39.37*pay[k]
        plt.plot([0,2],[ideal_p[k],ideal_p[k]],colors[k]+'--')




## for planetary dolly ##
# 1 : sub_radius    2 : wheel_num   3 : radius  4 : wheelbase   5 : payloadx    6 : payloadz    7 : step_rise
# 8 : step_slope    9 : payload_weight  10 : sim time   11 : speed [steps/min]  12 : mass   13 : max power  14-end : max torque 
# disc=['sub_rad','num_wheel','radius','wheelbase','paylocx','paylocz','step_rise','step_slope','pay_weight','sim time','speed','mass','max power','max torque']
# path = 'Wheel_Monte/'
# filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
# count=0
# # data=Load_Data(path,filenamelist,7,[])
# for i in range(4):
#     Plot_Data(path+filenamelist[i],[3],[7,2,13,14],disc,disc[8],count,9)
#     count=count+2
# plt.show()
# print("HEY")

## for wheeled ##
# 1 : radius    2 : wheelbase   3 : payloadx  4 : payloadz   5 : step_rise    6 : step_slope    7 : payload_weight
# 8 : sim time    9 : speed [steps/min]  10 : mass  11 : max power  12 : average power   13 : power sum  14-end : max torque 
# disc=['radius','wheelbase','payloadx','payloadz','step_rise','step_slope','payload_weight','sim_time','speed','mass','max power','average power','power sum','max torque']
# # path = 'Wheel_Monte/V3'
# # path = 'Wheel_8in/w9'

# # path = 'Planet_9in/w12'
# # path='Wheel_fix/'
# filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
# count=0
# for i in range(4):
    # Plot_Data(path+filenamelist[i],[12],[3,4,12,14],disc,disc[7],count,7)

    # Plot_Stable_Area(path+filenamelist[i],[3],[4],disc,disc[6],count,7)

# count=count+1

# path = 'Wheel_Size/plan5'
# data=Load_Data(path,filenamelist,7,[])
# # Plot_svr(data,3,11,9,'-')
# # Plot_svt(data,-4,11,9,'.')
# # Plot_tvr(data,3,-4,9,'-')
# Plot_pvr(data,3,14,9,'-')
# # plt.show()
# path = 'Wheel_Size/w2'#plan2'
# data=Load_Data(path,filenamelist,7,[])
# Plot_pvr(data,1,12,7,'-')
# # Plot_tvr(data,1,-4,7,'-')
# # Plot_svr(data,1,9,7,'-')
# plt.show()

## friction plot##
# path = 'Wheel_Size/fricplan'
# friction_plot(path,filenamelist,9)
# plt.show()
# path = 'Wheel_Size/fricwheel'
# friction_plot(path,filenamelist,7)
# plt.show()





# # Plot_tvr(data,3,-2,9)
# # Weight_plots(data,1,14,disc,0)
# # Weight_plots(data,7,12,disc,1)
# # print("HEY")
# plt.show()

## for planetary dolly ##
# 1 : sub_radius    2 : wheel_num       3 : radius      4 : wheelbase           5 : payloadx    6 : payloadz    7 : step_rise
# 8 : step_slope    9 : payload_weight  10 : sim time   11 : speed [steps/min]  12 : mass       13 : max power
# 14: average power 15: power sum       16-end : max torque 
disc=['sub_rad','num_wheel','radius','wheelbase','paylocx','paylocz','step_rise','step_slope','pay_weight','sim time','speed','mass','max power','average power','power sum','max torque']
path = 'Planet_9in/w7'
filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
count=0
for i in range(4):
    # Plot_Data(path+filenamelist[i],[2,3],[7,2,13,14],disc,disc[8],count)

    Plot_Stable_Area(path+filenamelist[i],[5],[6],disc,disc[8],count,9)

    count=count+1
plt.show()

# data=Load_Data(path,filenamelist,9,[])
# Plot_tvp(data,-1,13,9)
# # Weight_plots(data,9,13,disc,0)
# # Weight_plots(data,16,15,disc,1)
# plt.show()