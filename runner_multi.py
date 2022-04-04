from main import main_run
from monte import monte_sim_wheel, monte_sim_planet
import numpy as np
from mj_utils import replace_output
from multiprocessing import Process

sim_dict = {
    "wheelbase_mean" : 0.46,
    "wheelbase_std" :  0.0,#0.05
    "wheelbase_llim" : 0.1,
    "wheelbase_ulim" :  0.6,

    "payload_xloc_mean" : 0.3,
    "payload_xloc_std" :  0.0,
    "payload_xloc_llim" :  -1.05,
    "payload_xloc_ulim" :  1.35,

    "payload_zloc_mean" : -0.15,
    "payload_zloc_std" :  0.0, 
    "payload_zloc_llim" :  -1.25,
    "payload_zloc_ulim" :  1.15,  

    "wheel_size_mean" : 0.3,
    "wheel_size_std" : 0.00,
    "wheel_size_llim" : 0.1,
    "wheel_size_ulim" : 0.35,

    "sub_wheel_size_mean" : 0.0762,
    "sub_wheel_size_std" : 0.00,
    "sub_wheel_size_llim" : 0.01,
    "sub_wheel_size_ulim" : 0.15,

    "wheel_num_mean" : 3,
    "wheel_num_std" : 0,
    "wheel_num_llim" : 3,
    "wheel_num_ulim" : 6, 

    "step_num_mean" : 11,
    "step_num_std" : 0,
    "step_num_llim" : 1,
    "step_num_ulim" : 1000,

    "step_rise_mean" : 0.174,#0.2032,#0.2413,#0.2032,#0.1778, #0.2286
    "step_rise_std" : 0.0,
    "step_rise_llim" : 0.1524,
    "step_rise_ulim" : 0.2413,

    "step_slope_mean" : 31,
    "step_slope_std" : 0,
    "step_slope_llim" : 28,
    "step_slope_ulim" : 45,  

    "payload_mean" : 60,
    "payload_std" : 0,
    "payload_llim" : 0,
    "payload_ulim" : 455,    

    "front2rear_ratio" : 1.0 ,

    "hinge" : 0
}

def run_multi(ii):
    path = 'Wheeled/slope31/26v1'
    filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
    vmass=[50,70,90,110]
    sim_dict["step_slope_mean"] = 31
    sim_dict["payload_zloc_mean"] = 0
    writeout=1
    weight_in=np.linspace(0.1,-0.2,10)
    radius_in=np.linspace(0.05,0.3,10)#-0.225
    sim_dict["wheel_size_mean"] = 0.3302#0.3048#0.267#0.2286#0.1778#0.265
    planet=0
    count2=0
    winch=0    
    outfilename=path+filenamelist[ii]
    filename_env=['envi0.xml','envi1.xml','envi2.xml','envi3.xml']
    for i in range(len(radius_in)):
        sim_dict["payload_xloc_mean"] = radius_in[i]
        for j in range(len(weight_in)):
            sim_dict["payload_mean"] = vmass[ii]
            sim_dict["payload_zloc_mean"] = weight_in[j]
            if planet==0:
                inpts=monte_sim_wheel(sim_dict,filename_env[ii])
            else:
                # sim_dict["wheel_size_mean"] = 0.2
                inpts=monte_sim_planet(sim_dict,filename_env[ii])

            count = 0
            moveon=False
            utorque_lim=150.
            btorque_lim=40.
            torque_lim=utorque_lim
            env_name=filename_env[ii]#'envi.xml'
            count = 0
            contr_max_out=np.zeros((1,1))
            kei=1.2
            while moveon==False:
                success_flag, contr_max = main_run(viz=False,env_name=env_name,torque_lim=torque_lim,planet=planet,winch=winch,kei=kei)
                
                if success_flag==False and count==0:
                    
                    if planet==1:
                        torque_lim=btorque_lim
                    else:
                        kei=0.9
                if count>6:
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
            if writeout==1:
                if count2==0:
                    with open(outfilename,'w') as csvfile:
                        np.savetxt(csvfile,outp,delimiter=' ',header='Success wheel_radius wheelbase payload_xloc payload_zloc time steps/min cg_xloc max_power W0_torque W1_torque W2_torque W3_torque')
                else:
                    with open(outfilename,'a') as csvfile:
                        np.savetxt(csvfile,outp)
            else:
                # replace_output(outfilename,outp)
                exit()

                
            count2=count2+1
            print(count2)

processes = []
for i in range(4):
    p = Process(target=run_multi, args=(i,))
    p.start()
    processes.append(p)
    # run_multi(i)
for p in processes:
    p.join()
print('done')