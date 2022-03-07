from mujoco_py import load_model_from_path, MjSim, MjViewer
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pd_controller import control

def main_run(viz,env_name,torque_lim,planet):
    _xml_path = env_name
    model  = load_model_from_path(_xml_path)
    sim = MjSim(model)

    pd = control(sim,0.4)
    if viz==True:
        viewer = MjViewer(sim)

    t = 0
    contr_tot=np.zeros((1,len(sim.model._actuator_id2name)))
    contr_pow=np.zeros((1,len(sim.model._actuator_id2name)))
    contr_max=np.zeros((1,len(sim.model._actuator_id2name)+4))
    
    torque=[]
    wheelspeed=[]
    wheelspeed0=[]
    count=0.0
    lim=torque_lim
    run=True
    while run==True:

        if t>500: 
            if planet==1:
                pd.velo(-6.28,lim)
            else:
                pd.velowheel(-6.28,lim)

            
        t += 1
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
        # # wheelspeed0.append(sim.data.actuator_force[1])
        if viz==True:
            viewer.render()
            
        if sim.data.qpos[0]>=4.5:
            contr_max[0,0]=sim.data.time-500*sim.model.opt.timestep
            contr_max[0,1]=10/(sim.data.time-500*sim.model.opt.timestep)*60
            contr_max[0,2]=sim.data.qM[0]
            contr_max[0,3]=max([np.amax((contr_pow[:,0])),np.amax((contr_pow[:,1])),np.amax((contr_pow[:,2])),np.amax((contr_pow[:,3]))])
            for i in range(len(sim.model._actuator_id2name)):
                contr_max[0,i+4]=np.amax(np.abs(contr_tot[:,i]))
            return True, contr_max
            run=False
        else:
            contr_tot=np.append(contr_tot,np.reshape(sim.data.actuator_force,(1,len(sim.model._actuator_id2name))),axis=0)
            contr_pow=np.append(contr_pow,np.reshape(abs(sim.data.actuator_force*sim.data.qvel[-pd.num_acts:]/(2*math.pi)*60./9.5488),(1,len(sim.model._actuator_id2name))),axis=0)
        

        if sim.data.time>11+500*0.0025:
            return False, contr_max
        elif abs(180/math.pi*math.asin(sim.data.get_body_xquat('frame')[2]))>45.:
            return False, contr_max
