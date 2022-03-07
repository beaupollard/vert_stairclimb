import scipy
import re
import numpy as np
from tire_generate_auto import planetary_gen, tire_gen

def monte_sim_wheel():

    sim_dict = {
        "wheelbase_mean" : 0.31,
        "wheelbase_std" :  0.05,
        "payload_xloc_mean" : 0.0,
        "payload_xloc_std" :  0.15,
        "payload_zloc_mean" : 0.0,
        "payload_zloc_std" :  0.075,    
        "wheel_size_mean" : 0.225,
        "wheel_size_std" : 0.05,
    }


    file_name='horsemat.xml'
    with open(file_name) as f:
        lines = f.readlines()

    count = 0
    for i, stg in enumerate(lines):
        if re.search(r'rf_wheel', stg):
            start_s = i
        elif re.search(r'^\t\t\t</body>', stg) and count<4:
            count = count +1
            if count == 4:
                stop_s = i
        elif re.search(r'name=\"mass0\"',stg):
            vals=re.findall(r"[-+]?(?:\d*\.\d+|\d+)",stg)
            payloadx = -0.1
            while payloadx <-0.05:
                payloadx = np.random.normal(sim_dict["payload_xloc_mean"],sim_dict["payload_xloc_std"])
            payloadz = 0.3
            while abs(payloadz) >0.2:
                payloadz = np.random.normal(sim_dict["payload_zloc_mean"],sim_dict["payload_zloc_std"])

            lines[i]=stg[:re.search(vals[1],stg).regs[0][0]]+str(payloadx)+" 0.00 "+str(payloadz)+stg[re.search(vals[3],stg).regs[0][1]:]


    string1,radius,posx=tire_gen(sim_dict)
    lines[start_s:stop_s+1]=string1

    file_name='envi.xml'
    f=open(file_name,"w")
    for i in lines:
        f.writelines(i)
    f.close()

    return np.array([radius,posx,payloadx,payloadz])

def monte_sim_planet():

    sim_dict = {
        "wheelbase_mean" : 0.31,
        "wheelbase_std" :  0.05,
        "payload_xloc_mean" : 0.0,
        "payload_xloc_std" :  0.15,
        "payload_zloc_mean" : 0.0,
        "payload_zloc_std" :  0.075,    
        "wheel_size_mean" : 0.225,
        "wheel_size_std" : 0.05,
        "sub_wheel_size_mean" : 0.0762,
        "sub_wheel_size_std" : 0.01,        
    }

    string1, sub_radius, wheel_num, radius, posx, payloadx, payloadz=planetary_gen(sim_dict)
    file_name='horsemat.xml'
    with open(file_name) as f:
        lines = f.readlines()

    count = 0
    for i, stg in enumerate(lines):
        if re.search(r'rf_wheel', stg):
            start_s = i
        elif re.search(r'^\t\t\t</body>', stg) and count<4:
            count = count +1
            if count == 4:
                stop_s = i

    lines[:stop_s+1]=string1

    file_name='envi.xml'
    f=open(file_name,"w")
    for i in lines:
        f.writelines(i)
    f.close()

    return np.array([ sub_radius, wheel_num, radius, posx, payloadx, payloadz])


#     count = 0
# stg0=stg[re.search(r'^\t*',stg).regs[0][0]:re.search(r'^\t*',stg).regs[0][1]]
# lines[start_]
        # print("hey")
    # if re.search(r'_wheel', stg):
    #     ind=re.search(r'pos\s*=\s*\"',stg)
    #     if ind:
    #         stg0=stg[:ind.regs[0][1]]
    #         vals=re.findall(r"[-+]?(?:\d*\.\d+|\d+)",stg[ind.regs[0][1]:])
    #         indf=[re.search(vals[0],stg).regs[0][0],re.search(vals[0],stg).regs[0][1]]
            

    #     else:
    #         print("error")
