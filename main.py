from mujoco_py import load_model_from_path, MjSim, MjViewer
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pd_controller import control
from mujoco_py.generated import const
from mj_utils import get_power

fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
ax = plt.subplot(121)
ax1= plt.subplot(122)

def plotters(in1,in2):
    ax.cla()
    ax1.cla()

    ax.plot(in1[1:])
    ax1.plot(in2[1:])
    # ax1.plot(wheelspeed[1:])
    # ax1.plot(wheelspeed0[1:])
    plt.show(block=False)
    plt.pause(0.001)

def apply_force(sim):
    jacp=np.array(sim.data.get_site_jacp('winch').reshape((3, -1))[:,0:6])
    jacr=np.array(sim.data.get_site_jacr('winch').reshape((3, -1))[:,0:6])
    jacf=np.vstack([jacp,jacr])
    vec=np.vstack([np.array(sim.data.get_site_xpos('wypt0')-sim.data.get_site_xpos('winch')).reshape(3,1),np.zeros((3,1))])
    vec = 60.*vec/np.linalg.norm(vec)
    Fout = jacf.transpose()@vec
    for i,F in enumerate(Fout):
        sim.data.xfrc_applied[1,i] = F

def main_run(viz,env_name,torque_lim,planet,winch,kei,track):
    _xml_path = env_name
    model  = load_model_from_path(_xml_path)
    sim = MjSim(model)

    pd = control(sim,0.4)
    if viz==True:
        viewer = MjViewer(sim)
        viewer.cam.type = const.CAMERA_FIXED
        viewer.cam.fixedcamid = 0        
        

    t = 0
    init_time=300
    contr_tot=np.zeros((1,len(sim.model._actuator_id2name)))
    contr_pow=np.zeros((1,len(sim.model._actuator_id2name)))
    contr_max=np.zeros((1,len(sim.model._actuator_id2name)+6))
    
    torque=[]
    wheelspeed=[]
    wheelspeed0=[]
    count=0.0
    lim=torque_lim
    run=True
    while run==True:

        if t>init_time: 
            if planet==1:
                pd.velo(-6.28/1.5,lim)
                if winch==1:
                    apply_force(sim)                
            elif track==1:
                pd.velotrack(-36.28,lim,kei)
                if winch==1:
                    apply_force(sim)
            else:
                pd.velowheel(-6.28,lim,kei)
                if winch==1:
                    apply_force(sim)
        

        t += 1
        # if t>360:
        #     print(t)
        sim.step()
        # print(sim.data.time)
        # torque.append(sim.data.body_xpos[3][0])
        # wheelspeed.append(sim.data.body_xpos[3][1])
        # wheelspeed0.append(sim.data.body_xpos[3][2])

        # torque.append(sim.data.body_xpos[2][0])
        # wheelspeed.append(sim.data.body_xpos[2][1])
        # wheelspeed0.append(sim.data.body_xpos[2][2])  
              
        # # torque.append(180/math.pi*math.asin(sim.data.get_body_xquat('frame')[3]))
        # wheelspeed.append(sim.data.body_xpos[3])
        torque.append(sim.data.actuator_force[0])
        # wheelspeed.append(sim.data.actuator_force[-1])
        # torque.append(sim.data.qpos[sim.model.get_joint_qpos_addr('body_connect')]*180/math.pi)
        
        # torque.append(sim.data.xfrc_applied[1,0])        
        # wheelspeed.append(sim.data.get_site_xpos('winch')[0]/np.linalg.norm(np.array(sim.data.get_site_xpos('winch'))))        
        if viz==True:
            viewer.render()
            # plotters(torque,wheelspeed)
            
        if sim.data.qpos[0]>=sim.data.get_site_xpos('wypt0')[0]-1.0:
            contr_max[0,0]=sim.data.time-init_time*sim.model.opt.timestep
            contr_max[0,1]=10/(sim.data.time-init_time*sim.model.opt.timestep)*60
            contr_max[0,2]=sim.data.qM[0]
            pow_max=[]
            pow_ave=[]
            pow_sum=0
            for k in range(len(contr_pow[0,:])):
                pow_max.append(np.amax((contr_pow[:,k])))
                pow_ave.append(sum(contr_pow[:,k])/np.shape(contr_pow)[0])
                pow_sum=pow_sum+(sum(contr_pow[:,k]))
            contr_max[0,3]=max(pow_max)
            contr_max[0,4]=max(pow_ave)
            contr_max[0,5]=pow_sum#max(pow_sum)
            for i in range(len(sim.model._actuator_id2name)):
                contr_max[0,i+6]=np.amax(np.abs(contr_tot[:,i]))
            return True, contr_max
            run=False
        else:
            contr_tot=np.append(contr_tot,np.reshape(sim.data.actuator_force,(1,len(sim.model._actuator_id2name))),axis=0)
            contr_pow=np.append(contr_pow,np.array([get_power(sim)]),axis=0)
        

        if sim.data.time>25+init_time*0.0025:
            return False, contr_max
        elif abs(180/math.pi*math.asin(sim.data.get_body_xquat('frame')[2]))>45.:
            return False, contr_max
