from main import main_run
from monte import monte_sim_wheel, monte_sim_planet, monte_sim_planet_dolly
import numpy as np
from mj_utils import replace_output
from multiprocessing import Process

sim_dict = {
    "wheelbase_mean" : 0.46,
    "wheelbase_std" :  0.0,
    "wheelbase_llim" : 0.3,
    "wheelbase_ulim" :  0.6,

    "payload_xloc_mean" : 0.25,
    "payload_xloc_std" :  0.0,
    "payload_xloc_llim" :  -0.1,
    "payload_xloc_ulim" :  0.4,

    "payload_zloc_mean" : -0.1,
    "payload_zloc_std" :  0.0, 
    "payload_zloc_llim" :  -0.2,
    "payload_zloc_ulim" :  0.1,  

    "wheel_size_mean" : 0.167,#0.1778,
    "wheel_size_std" : 0.0,
    "wheel_size_llim" : 0.10,
    "wheel_size_ulim" : 0.305,

    "sub_wheel_size_mean" : 0.05715,
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

    "friction_mean" : 1.0,
    "friction_std" : 0,
    "friction_llim" : 0,
    "friction_ulim" : 1.1,    


    "front2rear_ratio" : 1.0 ,

    "hinge" : 0,
    "planet": 1,
    "dolly" : 0,
    "stable_len" : 0.35,
    "fix_plans" : 0,
    "track" : 0,
    "planet_tread" : 0,

    "winch" : 0,
    "winch_force": 100,

    "seed": 0
}

def run_multi(ii):
    path = 'Wheel_Size/fricplan'
    filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
    vmass=[50,70,90,110]
    np.random.seed(ii+1)
    sim_dict["payload_mean"] = vmass[ii]
    writeout=1
    output_com=False
    # wheel_s=np.linspace(0.1,0.3,10)
    frictionin=np.linspace(0.1,0.5,10)
    # radius_in=np.linspace(0.05,0.3,10)
    count2=0
    outfilename=path+filenamelist[ii]
    filename_env=['envi0.xml','envi1.xml','envi2.xml','envi3.xml']
    print_torque=False
    for jj in range(len(frictionin)):
        # sim_dict["wheel_size_mean"]=wheel_s[jj]
        sim_dict["friction"]=frictionin[jj]
        if sim_dict["planet"]==0:
            inpts=monte_sim_wheel(sim_dict,filename_env[ii])
        elif sim_dict["dolly"]==1:
            inpts=monte_sim_planet_dolly(sim_dict,filename_env[ii])
        else:
            inpts=monte_sim_planet(sim_dict,filename_env[ii])

        count = 0
        moveon=False
        utorque_lim=200.
        btorque_lim=40.
        torque_lim=utorque_lim
        env_name=filename_env[ii]#'envi.xml'
        count = 0
        contr_max_out=np.zeros((1,1))
        kei=1.2
        while moveon==False:
            success_flag, contr_max, cmpos, cmvel, powtot, tortot  = main_run(viz=False,env_name=env_name,torque_lim=torque_lim,planet=sim_dict["planet"],winch=sim_dict["winch"],kei=kei,track=sim_dict["track"])
            
            if success_flag==False and count==0:
                
                if sim_dict["planet"]==1:
                    torque_lim=btorque_lim
                else:
                    kei=0.9
            if count>11:
                moveon=True

            if success_flag==True:
                utorque_lim=torque_lim
                torque_lim=(torque_lim+btorque_lim)/2
                contr_max_out = contr_max
                cmpos_out=np.reshape(cmpos,(-1,3))
                cmvel_out=np.reshape(cmvel,(-1,3))
                power_out=powtot
                torque_out=tortot
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
        if print_torque==True:
            if sim_dict["planet"]==1:
                np.savetxt("plan_"+str(sim_dict["wheel_size_mean"])+"_cmpos.csv", cmpos_out, delimiter=",")
                np.savetxt("plan_"+str(sim_dict["wheel_size_mean"])+"_cmvel.csv", cmvel_out, delimiter=",")
                np.savetxt("plan_"+str(sim_dict["wheel_size_mean"])+"_pow.csv", power_out, delimiter=",")
                np.savetxt("plan_"+str(sim_dict["wheel_size_mean"])+"_torque.csv", torque_out, delimiter=",")
            else:
                np.savetxt("wheel_"+str(sim_dict["wheel_size_mean"])+"_cmpos.csv", cmpos_out, delimiter=",")
                np.savetxt("wheel_"+str(sim_dict["wheel_size_mean"])+"_cmvel.csv", cmvel_out, delimiter=",")
                np.savetxt("wheel_"+str(sim_dict["wheel_size_mean"])+"_pow.csv", power_out, delimiter=",")
                np.savetxt("wheel_"+str(sim_dict["wheel_size_mean"])+"_torque.csv", torque_out, delimiter=",")
        outp=np.reshape(outp,(1,len(outp)))
        if output_com==True:
            np.savetxt(path+filenamelist[ii][:-4]+"cmpos"+str(count2)+".csv", cmpos_out, delimiter=",")
            np.savetxt(path+filenamelist[ii][:-4]+"cmvel"+str(count2)+".csv", cmvel_out, delimiter=",")     
        ## Setup .csv file ##
        if writeout==1:
            if count2==0:
                with open(outfilename,'w') as csvfile:
                    np.savetxt(csvfile,outp,delimiter=' ',header='Success wheel_radius wheelbase payload_xloc payload_zloc time steps/min cg_xloc max_power W0_torque W1_torque W2_torque W3_torque')
            else:
                with open(outfilename,'a') as csvfile:
                    np.savetxt(csvfile,outp)
        else:
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
# run_multi(3)
print('done')