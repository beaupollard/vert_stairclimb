from main import main_run
from monte import monte_sim_wheel, monte_sim_planet
import numpy as np

sim_dict = {
    "wheelbase_mean" : 0.46,
    "wheelbase_std" :  0.0,#0.05
    "wheelbase_llim" : 0.1,
    "wheelbase_ulim" :  0.6,

    "payload_xloc_mean" : 0.3,
    "payload_xloc_std" :  0.0,
    "payload_xloc_llim" :  -0.05,
    "payload_xloc_ulim" :  0.35,

    "payload_zloc_mean" : -0.15,
    "payload_zloc_std" :  0.0, 
    "payload_zloc_llim" :  -0.15,
    "payload_zloc_ulim" :  0.15,  

    "wheel_size_mean" : 0.3,
    "wheel_size_std" : 0.00,
    "wheel_size_llim" : 0.1,
    "wheel_size_ulim" : 0.35,

    "sub_wheel_size_mean" : 0.0762,
    "sub_wheel_size_std" : 0.00,
    "sub_wheel_size_llim" : 0.01,
    "sub_wheel_size_ulim" : 0.15,

    "wheel_num_mean" : 4,
    "wheel_num_std" : 0,
    "wheel_num_llim" : 3,
    "wheel_num_ulim" : 6, 

    "step_num_mean" : 11,
    "step_num_std" : 0,
    "step_num_llim" : 1,
    "step_num_ulim" : 1000,

    "step_rise_mean" : 0.2413,#0.1778,
    "step_rise_std" : 0.0,
    "step_rise_llim" : 0.1524,
    "step_rise_ulim" : 0.2413,

    "step_slope_mean" : 45,
    "step_slope_std" : 0,
    "step_slope_llim" : 28,
    "step_slope_ulim" : 45,  

    "payload_mean" : 40,
    "payload_std" : 0,
    "payload_llim" : 0,
    "payload_ulim" : 455,     
}

planet=0
count2=0
while True:
    if planet==0:
        inpts=monte_sim_wheel(sim_dict)
    else:
        inpts=monte_sim_planet(sim_dict)

    count = 0
    moveon=False
    utorque_lim=150.
    btorque_lim=40.
    torque_lim=utorque_lim
    env_name='envi.xml'
    count = 0
    
    while moveon==False:
        success_flag, contr_max = main_run(viz=True,env_name=env_name,torque_lim=torque_lim,planet=planet)
        
        if success_flag==False and count==0:
            torque_lim=btorque_lim
        if count>7:
            moveon=True

        if success_flag==True:
            utorque_lim=torque_lim
            torque_lim=(torque_lim+btorque_lim)/2
            contr_max_out = contr_max
            if abs(torque_lim-(torque_lim+btorque_lim)/2)<1.0:
                moveon=True
        else:
            btorque_lim=torque_lim
            torque_lim=(torque_lim+utorque_lim)/2

        count = count + 1

    if abs(contr_max_out[0,-1])>0.0:
        outp=np.append([1],np.append(inpts,np.reshape(contr_max_out,(len(contr_max_out[0]),))))
    else:
        outp=np.append([0],np.append(inpts,np.reshape(contr_max_out,(len(contr_max_out[0]),))))

    outp=np.reshape(outp,(1,len(outp)))
    ## Setup .csv file ##
    if count2==0:
        with open('data.csv','w') as csvfile:
            np.savetxt(csvfile,outp,delimiter=' ',header='Success wheel_radius wheelbase payload_xloc payload_zloc time steps/min cg_xloc max_power W0_torque W1_torque W2_torque W3_torque')
    else:
        with open('data.csv','a') as csvfile:
            np.savetxt(csvfile,outp)        
    count2=count2+1
    print(count2)
