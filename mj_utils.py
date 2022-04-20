import numpy as np
from os.path import exists  
import csv
import math

def get_site_state(sim,site_id):
    '''
    INPUT:
    Takes in a MjSim object and a site id, outputs
    rot mat, pos, ang vel, lin vel in cartesian space
    OUTPUT:
    (R, p, w, v) in cartesian space
    '''
    pos     = np.array(sim.data.site_xpos[site_id])
    ori_mat = np.array(sim.data.site_xmat[site_id]).reshape((3,3))
    pos_vel = np.array(sim.data.site_xvelp[site_id])
    ori_vel = np.array(sim.data.site_xvelr[site_id])
    return (ori_mat, pos, ori_vel, pos_vel)    

def get_body_state(sim, body_id):
    '''
    INPUT:
    Takes in a MjSim object and a site id, outputs
    rot mat, pos, ang vel, lin vel in cartesian space
    OUTPUT:
    (R, p, w, v) in cartesian space
    '''
    pos     = np.array(sim.data.body_xpos[body_id])
    ori_mat = np.array(sim.data.body_xmat[body_id]).reshape((3,3))
    pos_vel = np.array(sim.data.body_xvelp[body_id])
    ori_vel = np.array(sim.data.body_xvelr[body_id])
    return (ori_mat, pos, ori_vel, pos_vel) 

def replace_output(filename,outp):
    inp2 = []
    rowout = []
    row2=[]
    count=0
    outp=outp.reshape((len(outp[0,:]),))
    if exists(filename):
        with open(filename, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                row2.append(row)
        # with open('test.csv','w') as csvfile:
     
        for i, row in enumerate(row2):
            inp=(row[0][:].split(' '))
            inp = np.array([float(x) for x in inp])
            # if i>len(row2)-6:
            #     print("Hey")
            # print(i)
            if i==0:
                with open(filename,'w') as csvfile:
                    np.savetxt(csvfile,inp.reshape((1,len(inp))),delimiter=' ',header='Success wheel_radius wheelbase payload_xloc payload_zloc time steps/min cg_xloc max_power W0_torque W1_torque W2_torque W3_torque')   
            else:
                if sum(inp[1:7]==outp[1:7])==6:
                    with open(filename,'a') as csvfile:
                        np.savetxt(csvfile,outp.reshape((1,len(outp))))
                else:
                    with open(filename,'a') as csvfile:
                        np.savetxt(csvfile,inp.reshape((1,len(inp))))

def get_power(sim):
    power=[]
    for i in ((sim.model._actuator_id2name)):
        jtn_index=sim.model.get_joint_qvel_addr(sim.model._actuator_id2name[i])
        qvel=sim.data.qvel[jtn_index]
        act_f=sim.data.actuator_force[i]
        power.append(act_f*qvel/(2*math.pi)*60./9.5488)
    return power