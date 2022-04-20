from main import main_run
from monte import monte_sim_wheel, monte_sim_planet, monte_sim_planet_dolly
import numpy as np
from mj_utils import replace_output

sim_dict = {
    "wheelbase_mean" : 0.46,
    "wheelbase_std" :  0.0,
    "wheelbase_llim" : 0.3,
    "wheelbase_ulim" :  0.6,

    "payload_xloc_mean" : 0.25,
    "payload_xloc_std" :  0.2,
    "payload_xloc_llim" :  0.05,
    "payload_xloc_ulim" :  0.4,

    "payload_zloc_mean" : -0.1,
    "payload_zloc_std" :  0.1, 
    "payload_zloc_llim" :  -0.2,
    "payload_zloc_ulim" :  0.1,  

    "wheel_size_mean" : 0.2286,
    "wheel_size_std" : 0.0,
    "wheel_size_llim" : 0.15,
    "wheel_size_ulim" : 0.305,

    "sub_wheel_size_mean" : 0.05715,
    "sub_wheel_size_std" : 0.00,
    "sub_wheel_size_llim" : 0.01,
    "sub_wheel_size_ulim" : 0.15,

    "wheel_num_mean" : 3,
    "wheel_num_std" : 1,
    "wheel_num_llim" : 3,
    "wheel_num_ulim" : 6, 

    "step_num_mean" : 11,
    "step_num_std" : 0,
    "step_num_llim" : 1,
    "step_num_ulim" : 1000,

    "step_rise_mean" : 0.174,
    "step_rise_std" : 0.0,#0.0254,
    "step_rise_llim" : 0.1524,
    "step_rise_ulim" : 0.2413,

    "step_slope_mean" : 38,
    "step_slope_std" : 0,
    "step_slope_llim" : 28,
    "step_slope_ulim" : 45,  

    "payload_mean" : 60,
    "payload_std" : 0,
    "payload_llim" : 0,
    "payload_ulim" : 455,    

    "front2rear_ratio" : 1.0 ,

    "hinge" : 0,
    "planet": 0,
    "dolly" : 0,
    "stable_len" : 0.35,
    "fix_plans" : 1,
    "friction" : 0.62,
    "track" : 0,

    "winch" : 0,
    "winch_force": 100
}


# rise_in=np.linspace(0.1651,0.2413,5)
# slope_in=np.linspace(30,45,10)
# weight_in=np.linspace(30,70,10)
# payx_in=np.linspace(0.15,0.3,10)
weight_in=np.linspace(0.1,-0.2,10)
radius_in=np.linspace(0.05,0.3,10)
sim_dict["wheel_size_mean"] = 0.1778#5.5/39.37#0.265#0.1778#0.265
planet=0
dolly=0
count2=0
winch=0
outfilename='Wheeled/slope42/v1payxlocVzloc_pay40.csv'
# sim_dict["step_slope_mean"] = 30.0
# sim_dict["payload_zloc_mean"] = 1.0/39.37
# sim_dict["payload_xloc_mean"] = -1./39.37
# sim_dict["sub_wheel_size_mean"] = 4.5/39.37/2
writeout=0

filename_env='enviR1.xml'
# inpts=monte_sim_wheel(sim_dict,filename_env)
# inpts=monte_sim_planet_dolly(sim_dict,filename_env)
# success_flag, contr_max = main_run(viz=False,env_name=filename_env,torque_lim=100.,planet=planet,winch=winch,kei=1.25,track=sim_dict["track"])
# filename_env='envi_2pm_NR_F_V2.xml'

for i in range(len(radius_in)):
    # sim_dict["payload_xloc_mean"] = radius_in[0]
    for j in range(len(weight_in)):
        sim_dict["payload_mean"] = 110
        # sim_dict["payload_zloc_mean"] = weight_in[-1]
        if planet==0:
            inpts=monte_sim_wheel(sim_dict,filename_env)
        elif dolly==1:
            inpts=monte_sim_planet_dolly(sim_dict,filename_env)
        else:
            # sim_dict["wheel_size_mean"] = 0.2
            inpts=monte_sim_planet(sim_dict,filename_env)

        count = 0
        moveon=False
        utorque_lim=80.
        btorque_lim=0.
        torque_lim=utorque_lim
        env_name=filename_env
        count = 0
        contr_max_out=np.zeros((1,1))
        while moveon==False:
            success_flag, contr_max = main_run(viz=True,env_name=env_name,torque_lim=torque_lim,planet=planet,winch=winch,kei=0.95,track=sim_dict["track"])#0.95)
            
            if success_flag==False and count==0:#contr_max_out[0]==0:
                torque_lim=btorque_lim
            if count>10:
                moveon=True

            if success_flag==True:
                utorque_lim=torque_lim
                torque_lim=(torque_lim+btorque_lim)/2
                contr_max_out = contr_max
                print("success")
                if abs(torque_lim-(torque_lim+btorque_lim)/2)<1.0:
                    moveon=True
            else:
                btorque_lim=torque_lim
                torque_lim=(torque_lim+utorque_lim)/2
            print(torque_lim)
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
