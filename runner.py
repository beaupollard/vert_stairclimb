from main import main_run
from monte import monte_sim_wheel, monte_sim_planet, monte_sim_planet_dolly
import numpy as np
from mj_utils import replace_output
from multiprocessing import Process
from wheeled_dict import sim_dict

def run_multi(ii):
    sim_dict["payload_xloc_mean"]=0.39764942
    sim_dict["payload_zloc_mean"]=-0.03492468
    sim_dict["wheel_size_mean"]=0.17147157
    sim_dict["payload_mean"] = 110
    if sim_dict["planet"]==0:
        path = 'Wheel_CDR35'
    else:
        path = 'Planet_CDR35'
    filenamelist=['payxlocVzloc_pay0.csv','payxlocVzloc_pay20.csv','payxlocVzloc_pay40.csv','payxlocVzloc_pay60.csv']
    vmass=[110]#[50,70,90,110]
    np.random.seed(ii+1)
    
    writeout=0
    output_com=False
    # weight_in=np.linspace(0.1,-0.2,10)
    # radius_in=np.linspace(0.05,0.3,10)
    count2=0
    outfilename=path+filenamelist[ii]
    filename_env=['envi4.xml','envi5.xml','envi6.xml','envi7.xml']
    while True:

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
        env_name=filename_env[ii]
        count = 0
        contr_max_out=np.zeros((1,1))
        kei=1.2
        divisor=1.
        while moveon==False:
            success_flag, contr_max, cmpos, cmvel, powtot, tortot = main_run(viz=True,env_name=env_name,torque_lim=torque_lim,planet=sim_dict["planet"],winch=sim_dict["winch"],kei=kei,track=sim_dict["track"],divisor=divisor)
            
            if success_flag==False and count==0:
                divisor=3
                torque_lim=btorque_lim

            if count>9:
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

        outp=np.reshape(outp,(1,len(outp)))
        if output_com==True:
            np.savetxt(path+filenamelist[ii][:-4]+"cmpos"+str(count2)+".csv", cmpos_out, delimiter=",")
            np.savetxt(path+filenamelist[ii][:-4]+"cmvel"+str(count2)+".csv", cmvel_out, delimiter=",")     
        ## Setup .csv file ##
        if writeout==1:
            if count2==-10:
                with open(outfilename,'w') as csvfile:
                    np.savetxt(csvfile,outp,delimiter=' ',header='Success wheel_radius wheelbase payload_xloc payload_zloc time steps/min cg_xloc max_power W0_torque W1_torque W2_torque W3_torque')
            else:
                with open(outfilename,'a') as csvfile:
                    np.savetxt(csvfile,outp)
        else:
            exit()

            
        count2=count2+1
        print(count2)
run_multi(0)