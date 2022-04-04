import matplotlib.pyplot as plt
import numpy as np
import csv
from os.path import exists


# rows = []
# with open("data.csv", 'r') as file:
#     csvreader = csv.reader(file)
#     header = next(csvreader)
#     for row in csvreader:
#         rows.append(row)

# fig, axs = plt.subplots(2, 2)
# count=0
# for i in rows:
#     # 0 = success/fail
#     # 1 = Wheel radius
#     # 2 = Wheel base
#     # 3 = Payload x location
#     # 4 = Payload z location
#     # 5 = sim time
#     # 6 = Steps/min
#     # 7 = CG xloc
#     # 8 = max power? not accurate there is a math mistake
#     # 9 = W0 torque
#     # 10 = W1 torque
#     # 11 = W2 torque
#     # 12 = W3 torque

#     inp=(i[0][:].split(' '))
#     if float(inp[0])==1:
#         axs[0,0].plot(float(inp[1]),float(inp[2]),'ob')
#         axs[1,0].plot(float(inp[3]),float(inp[4]),'ob')
#         axs[0,1].plot(float(inp[1]),float(inp[-1]),'ob')
#         axs[1,1].plot(float(inp[1]),float(inp[6]),'ob')
#         count=count+1
#     else:
#         axs[0,0].plot(float(inp[1]),float(inp[2]),'or',alpha=0.5)
#         axs[1,0].plot(float(inp[3]),float(inp[4]),'or',alpha=0.5)
    
# axs[0,0].set_xlabel('Wheel radius [m]')
# axs[0,0].set_ylabel('Wheelbase [m]')
# axs[1,0].set_xlabel('Payload xloc [m]')
# axs[1,0].set_ylabel('Payload zloc [m]')
# axs[0,1].set_xlabel('Wheel radius [m]')
# axs[0,1].set_ylabel('Torque [Nm]')
# axs[1,1].set_xlabel('Payload zloc [m]')
# axs[1,1].set_ylabel('Torque [Nm]')

# print(count)
# plt.show()

## Plotting for Planetary Wheels
# fig, axs = plt.subplots(2, 2)
# count=0
# for i in rows:
#     # 0 = success/fail
#     # 1 = Sub Wheel radius
#     # 2 = Wheel Num
#     # 3 = Planetary radius
#     # 4 = Wheel base
#     # 5 = Payload x location
#     # 6 = Payload z location
#     # 7 = sim time
#     # 8 = Steps/min
#     # 9 = CG xloc
#     # 10 = max power? not accurate there is a math mistake
#     # 11 = W00 torque   15 = W10    19 = W20    23 = W30
#     # 12 = W01 torque   16 = W11    20 = W21    24 = W31
#     # 13 = W02 torque   17 = W12    21 = W22    25 = W32
#     # 14 = W03 torque   18 = W13    22 = W23    26 = W33
#     col=['ob','or','ok','og']
#     inp=(i[0][:].split(' '))
#     inp = [float(x) for x in inp]
#     if float(inp[0])==1:

#         axs[0,0].plot(float(inp[2]),float(inp[3]),'ob')
#         axs[1,0].plot(float(inp[3]),float(inp[4]),'ob')
#         # axs[0,1].plot(float(inp[5]),inp[10],'ob')
#         axs[0,1].plot(float(inp[10]),max(inp[11:]),col[int(inp[2]-3)])
#         # axs[0,1].plot(float(inp[3]),float(inp[15]),'or')
#         # for j in range(3):
#         #     if inp[2]==j+3:
#         # print(int[inp[2]-3])
#         axs[1,1].plot(float(inp[3]),max(inp[11:]),col[int(inp[2]-3)])
#         count=count+1
#     else:
#         axs[0,0].plot(float(inp[2]),float(inp[3]),'or',alpha=0.5)
#         axs[1,0].plot(float(inp[3]),float(inp[4]),'or',alpha=0.5)
#         # axs[0,1].plot(float(inp[5]),inp[6],'or',alpha=0.35)
    
# axs[0,0].set_xlabel('Wheel radius [m]')
# axs[0,0].set_ylabel('Wheelbase [m]')
# axs[1,0].set_xlabel('Planet radius [m]')
# axs[1,0].set_ylabel('Wheelbase [m]')
# axs[0,1].set_xlabel('Max power [W]')
# axs[0,1].set_ylabel('Max Torque [Nm]')
# axs[1,1].set_xlabel('Planet radius [m]')
# axs[1,1].set_ylabel('Torque [Nm]')

# print(count)
# plt.show()

# rows = []
# with open("data_7P.csv", 'r') as file:
#     csvreader = csv.reader(file)
#     header = next(csvreader)
#     for row in csvreader:
#         rows.append(row)

# fig = plt.figure(figsize=plt.figaspect(0.5))
# ax = fig.add_subplot(1, 2, 1, projection='3d')
# count=0

# count = 0

# for i in rows:
#     inp=(i[0][:].split(' '))
#     inp = [float(x) for x in inp]
#     if float(inp[0])==1:
#         ax.scatter(float(inp[8]),float(inp[9]),max(inp[18:]),color='r')
#         count=count+1

# ax.set_xlabel('Step Slope [deg]')
# ax.set_ylabel('Payload Weight [kg]')
# ax.set_zlabel('Max Torque Per Motor [Nm]')
# rows = []
# with open("data_7W.csv", 'r') as file:
#     csvreader = csv.reader(file)
#     header = next(csvreader)
#     for row in csvreader:
#         rows.append(row)

# ax = fig.add_subplot(1, 2, 2, projection='3d')
# count = 0

# for i in rows:
#     inp=(i[0][:].split(' '))
#     inp = [float(x) for x in inp]
#     if float(inp[0])==1:
#         ax.scatter(float(inp[6]),float(inp[7]),max(inp[12:]),color='b')
#         count=count+1
#     # else:
#         # ax.scatter(float(inp[1]),float(inp[2]),float(inp[4]),color='r',alpha=0.5)
# ax.set_xlabel('Step Slope [deg]')
# ax.set_ylabel('Payload Weight [kg]')
# ax.set_zlabel('Max Torque Per Motor [Nm]')

# plt.show()
fig = plt.figure(figsize=plt.figaspect(0.5))
step_rise = [7,8,95]
num_in=3
for ii in range(num_in):
    rows = []
    inp2=[]
    
    filename="data_"+str(int(step_rise[ii]))+"P.csv"
    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])
                if inp[0]==1:
                    inp2.append([inp[8],inp[9],max(inp[18:])])
                else:
                    inp2.append([inp[8],inp[9],0])
                
                rows.append(row)

        inp2=np.array(inp2)
        slope=np.unique(inp2[:,0])
        weight=np.unique(inp2[:,1])

        X, Y = np.meshgrid(slope,weight)
        leng=len(X[:,0])
        Z = np.zeros(np.shape(X))
        for i in range(leng):
            for j in range(leng):
                for k in range(len(inp2[:,0])):
                    if X[i,j]==inp2[k,0] and Y[i,j]==inp2[k,1]:
                        Z[i,j]=inp2[k,2]
            



        
        ax = fig.add_subplot(num_in, 2, 1+ii*2, projection='3d')
        count=0
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1)

        ax.set_xlabel('Step Slope [deg]')
        ax.set_ylabel('Payload Weight [kg]')
        ax.set_zlabel('Max Torque Per Motor [Nm]')
        ax.set_title('Planetary '+str(int(step_rise[ii]))+' in Step')

    rows = []
    inp2=[]
    filename="data_"+str(int(step_rise[ii]))+"W.csv"
    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                inp=(row[0][:].split(' '))
                inp = ([float(x) for x in inp])
                if inp[0]==1:
                    inp2.append([inp[6],inp[7],max(inp[12:])])
                else:
                    inp2.append([inp[6],inp[7],0])
                
                rows.append(row)

        inp2=np.array(inp2)
        slope=np.unique(inp2[:,0])
        weight=np.unique(inp2[:,1])

        X, Y = np.meshgrid(slope,weight)
        leng=len(X[:,0])
        Z = np.zeros(np.shape(X))
        for i in range(leng):
            for j in range(leng):
                for k in range(len(inp2[:,0])):
                    if X[i,j]==inp2[k,0] and Y[i,j]==inp2[k,1]:
                        Z[i,j]=inp2[k,2]
            


        ax = fig.add_subplot(num_in, 2, 2+ii*2, projection='3d')
        count=0
        surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1)

        ax.set_xlabel('Step Slope [deg]')
        ax.set_ylabel('Payload Weight [kg]')
        ax.set_zlabel('Max Torque Per Motor [Nm]')
        ax.set_title('Wheel '+str(int(step_rise[ii]))+' in Step')
plt.show()
