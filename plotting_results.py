import matplotlib.pyplot as plt
import numpy as np
import csv

rows = []
with open("data_plan.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        rows.append(row)

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
fig, axs = plt.subplots(2, 2)
count=0
for i in rows:
    # 0 = success/fail
    # 1 = Sub Wheel radius
    # 2 = Wheel Num
    # 3 = Planetary radius
    # 4 = Wheel base
    # 5 = Payload x location
    # 6 = Payload z location
    # 7 = sim time
    # 8 = Steps/min
    # 9 = CG xloc
    # 10 = max power? not accurate there is a math mistake
    # 11 = W00 torque   15 = W10    19 = W20    23 = W30
    # 12 = W01 torque   16 = W11    20 = W21    24 = W31
    # 13 = W02 torque   17 = W12    21 = W22    25 = W32
    # 14 = W03 torque   18 = W13    22 = W23    26 = W33
    col=['ob','or','ok','og']
    inp=(i[0][:].split(' '))
    inp = [float(x) for x in inp]
    if float(inp[0])==1:

        axs[0,0].plot(float(inp[2]),float(inp[3]),'ob')
        axs[1,0].plot(float(inp[3]),float(inp[4]),'ob')
        axs[0,1].plot(float(inp[5]),inp[6],'ob')
        # axs[0,1].plot(float(inp[3]),float(inp[15]),'or')
        # for j in range(3):
        #     if inp[2]==j+3:
        # print(int[inp[2]-3])
        axs[1,1].plot(float(inp[3]),max(inp[11:]),col[int(inp[2]-3)])
        count=count+1
    else:
        axs[0,0].plot(float(inp[2]),float(inp[3]),'or',alpha=0.5)
        axs[1,0].plot(float(inp[3]),float(inp[4]),'or',alpha=0.5)
        axs[0,1].plot(float(inp[5]),inp[6],'or')
    
axs[0,0].set_xlabel('Wheel radius [m]')
axs[0,0].set_ylabel('Wheelbase [m]')
axs[1,0].set_xlabel('Planet radius [m]')
axs[1,0].set_ylabel('Wheelbase [m]')
axs[0,1].set_xlabel('Payload xloc [m]')
axs[0,1].set_ylabel('payload zloc [m]')
axs[1,1].set_xlabel('Planet radius [m]')
axs[1,1].set_ylabel('Torque [Nm]')

print(count)
plt.show()

# count = 0
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# for i in rows:
#     inp=(i[0][:].split(' '))
#     if float(inp[0])==1:
#         ax.scatter(float(inp[1]),float(inp[2]),float(inp[4]),color='b')
#         count=count+1
#     else:
#         ax.scatter(float(inp[1]),float(inp[2]),float(inp[4]),color='r',alpha=0.5)

# plt.show()
