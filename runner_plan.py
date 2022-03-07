from main import main_run
from monte import monte_sim_wheel, monte_sim_planet
import numpy as np
 
count2=0
while True:
    inpts=monte_sim_planet()
    count = 0
    moveon=False
    utorque_lim=130.
    btorque_lim=40.
    torque_lim=utorque_lim 
    env_name='envi.xml'
    count = 0
    out_len = 4*int(inpts[1]+1)+4
    contr_max_out=np.zeros((1,out_len))
    while moveon==False:
        success_flag, contr_max = main_run(viz=False,env_name=env_name,torque_lim=torque_lim,planet=1)
        
        if success_flag==False and count==0:
            torque_lim=btorque_lim
        if count>5:
            moveon=True

        if success_flag==True:
            if abs(torque_lim-(torque_lim+btorque_lim)/2)<1.0:
                utorque_lim=torque_lim
                torque_lim=(torque_lim+btorque_lim)/2
                contr_max_out = contr_max
                moveon=True
            else:
                utorque_lim=torque_lim
                torque_lim=(torque_lim+btorque_lim)/2
                contr_max_out = contr_max            
        else:
            btorque_lim=torque_lim
            torque_lim=(torque_lim+utorque_lim)/2

        count = count + 1

    if abs(contr_max_out[0,-1])>0.0:
        outp=np.append([1],np.append(inpts,np.reshape(contr_max_out,(out_len,))))
    else:
        outp=np.append([0],np.append(inpts,np.reshape(contr_max_out,(out_len,))))

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
