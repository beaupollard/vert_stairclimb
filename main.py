from mujoco_py import load_model_from_path, MjSim, MjViewer
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import ilqr
from matplotlib.animation import FuncAnimation
from pd_controller import control

def plotters():
    ax.cla()
    ax1.cla()

    ax.plot(torque[1:])
    ax1.plot(wheelspeed[1:])
    ax1.plot(wheelspeed0[1:])
    plt.show(block=False)
    plt.pause(0.001)

_xml_path = 'horsemat.xml'
model  = load_model_from_path(_xml_path)
sim = MjSim(model)

pd = control(sim,0.4)
# ilqr = ilqr.ilqr(sim)
viewer = MjViewer(sim)
t = 0
contr_tot=np.zeros((1,len(sim.model._actuator_id2name)))
contr_pow=np.zeros((1,len(sim.model._actuator_id2name)))
contr_max=np.zeros((1,len(sim.model._actuator_id2name)+4))

fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
ax = plt.subplot(121)
ax1= plt.subplot(122)

torque=[]
wheelspeed=[]
wheelspeed0=[]
count=0.0
lim=85
run=True
while run==True:

    if t>100:  
        pd.velowheel(-6.28,lim)
        # pd.velo(-6.28,lim)
    t += 1
    sim.step()

    # torque.append(180/math.pi*math.asin(sim.data.get_body_xquat('frame')[3]))
    # wheelspeed.append(sim.data.actuator_force[0])
    # wheelspeed0.append(sim.data.actuator_force[1])
    # ilqr.forward()
    # plotters()
    viewer.render()

    if sim.data.qpos[0]>=4.5:
        contr_max[0,0]=sim.data.time-100*sim.model.opt.timestep()#0.05
        contr_max[0,1]=10/(sim.data.time-100*sim.model.opt.timestep())*60
        contr_max[0,2]=sim.data.qM[0]
        contr_max[0,3]=max([np.amax((contr_pow[:,0])),np.amax((contr_pow[:,1])),np.amax((contr_pow[:,2])),np.amax((contr_pow[:,3]))])
        for i in range(len(sim.model._actuator_id2name)):
            contr_max[0,i+4]=np.amax(np.abs(contr_tot[:,i]))
        np.savetxt("torques.csv", contr_max, delimiter=",")
        run=False
    else:
        contr_tot=np.append(contr_tot,np.reshape(sim.data.actuator_force,(1,len(sim.model._actuator_id2name))),axis=0)
        # contr_pow=np.append(contr_pow,np.reshape(abs(sim.data.actuator_force*(sim.data.qvel[-4:]/(2*math.pi)*60.)),(1,len(sim.model._actuator_id2name))),axis=0)
        contr_pow=np.append(contr_pow,np.reshape(abs(sim.data.actuator_force*sim.data.qvel[-4:]/(2*math.pi)*60./9.5488),(1,len(sim.model._actuator_id2name))),axis=0)
