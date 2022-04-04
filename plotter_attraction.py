import matplotlib.pyplot as plt
import numpy as np
import csv
from os.path import exists    
from matplotlib import cm

def Get_Basin(filename,parm1,parm2,parm3,ax,off_x):
    rows=[]
    inp2=[]
    if filename[-5]=='P':
        xin=parm1
        yin=parm2
        zin=parm3       
        # xin=8
        # yin=9
        # zin=18
    else:
        xin=parm1
        yin=parm2
        zin=parm3         
        # xin = 6
        # yin = 7
        # zin = 12

    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])
                if inp[0]==1:
                    inp2.append([inp[xin],inp[yin],max(inp[zin:])])
                else:
                    inp2.append([inp[xin],inp[yin],0])
                
                rows.append(row)
        print(np.amax(np.array(inp2)))
        for i in range(len(inp2)):
            if inp2[i][-1]==0:
                ax.plot(inp2[i][0]-off_x,inp2[i][1],'or',ms=12)
            else:
                ax.plot(inp2[i][0]-off_x,inp2[i][1],'ob',ms=12)

def Get_Surf(filename,parm1,parm2,parm3,ax,lx,lz,off_x):
    rows=[]
    inp2=[]
    if filename[-5]=='P':
        xin=parm1
        yin=parm2
        zin=parm3       
        # xin=8
        # yin=9
        # zin=18
    else:
        xin=parm1
        yin=parm2
        zin=parm3         
        # xin = 6
        # yin = 7
        # zin = 12

    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])
                if inp[0]==1:
                    inp2.append([inp[xin]-off_x,inp[yin],max(inp[zin:])])
                else:
                    inp2.append([inp[xin]-off_x,inp[yin],0])
                
                rows.append(row)

        inp2=np.array(inp2)
        # slope=np.unique(inp2[:,0])-0.05 = lz 0.15 = lx
        # weight=np.unique(inp2[:,1])
        slope2=[]
        weight2=[]
        torque2=[]
        for i in range(len(inp2[:,0])):
            if inp2[i,0]>lx and inp2[i,1]<lz:
                slope2.append(inp2[i,0])
                weight2.append(inp2[i,1])
                torque2.append(inp2[i,2])
        print(max(torque2))
        weight=np.array(weight2)
        slope=np.array(slope2)
        slope=np.unique(slope)
        weight=np.unique(weight)        
        X, Y = np.meshgrid(slope,weight)
        lengr=len(X[:,0])
        lengc=len(X[0,:])
        Z = np.zeros(np.shape(X))
        for i in range(lengr):
            for j in range(lengc):
                for k in range(len(inp2[:,0])):
                    if X[i,j]==inp2[k,0] and Y[i,j]==inp2[k,1]:
                        Z[i,j]=inp2[k,2]
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1,cmap=cm.coolwarm)
        # ax.axes.set_xlim3d(left=0.15, right=0.35) 
        # ax.axes.set_ylim3d(bottom=-0.25, top=-0.05) 
        # ax.view_init(30, -140)
        ax.view_init(30, -50)
        # ax.axes.set_zlim3d(bottom=0, top=10)

fig = plt.figure(figsize=plt.figaspect(0.5))

path='Wheeled/slope31/24'
# path='Planet/slope36_5W/'
titles=['0kg Payload','20kg Payload','40kg Payload','60kg Payload']
# names=[path+'Wheel_payxlocVzloc_pay0.csv',path+'Wheel_payxlocVzloc_pay20.csv','test.csv',path+'Wheel_payxlocVzloc_pay60.csv']
# names=[path+'Wheel_payxlocVzloc_pay0.csv',path+'Wheel_payxlocVzloc_pay20.csv',path+'Wheel_payxlocVzloc_pay40.csv',path+'Wheel_payxlocVzloc_pay60.csv']
names=[path+'payxlocVzloc_pay0.csv',path+'payxlocVzloc_pay20.csv',path+'payxlocVzloc_pay40.csv',path+'payxlocVzloc_pay60.csv']
fs=21
# for i in range(4):
#     ax = fig.add_subplot(2, 2, i+1)
#     Get_Basin(names[i],3,4,12,ax,off_x=0.0) # for wheeled hinge
#     # Get_Basin(names[i],3,4,12,ax,off_x=-0.225) # for wheeled hinge
#     # Get_Basin(names[i],5,6,14,ax,off_x=0.0)   # for planet


#     ax.set_xlabel('Payload Xloc [m]',fontsize=fs)
#     ax.set_ylabel('Payload Zloc [m]',fontsize=fs)
#     ax.set_title(titles[i],fontsize=fs)
#     for label in (ax.get_xticklabels() + ax.get_yticklabels()):
# 	    label.set_fontsize(fs)

for i in range(4):
    ax = fig.add_subplot(2, 2, i+1, projection='3d')
    Get_Surf(names[i],3,4,12,ax,-1.17,-0.01,off_x=-0.)#0.13 0 # for wheeled
    # Get_Surf(names[i],3,4,12,ax,-1.17,-0.01,off_x=-0.225)#0.13 0 # for wheeled
    # Get_Surf(names[i],5,6,14,ax,0.0,-0.01,off_x=0.0)#0.13 0 # for planet


    ax.set_xlabel('Payload Xloc [m]',fontsize=fs,labelpad=30)
    ax.set_ylabel('Payload Zloc [m]',fontsize=fs,labelpad=30)
    ax.set_zlabel('Max Torque [Nm]',fontsize=fs,labelpad=20)
    ax.set_title(titles[i],fontsize=fs)
    for label in (ax.get_xticklabels() + ax.get_yticklabels() + ax.get_zticklabels()):
	    label.set_fontsize(fs)

fig.tight_layout()
plt.show()
