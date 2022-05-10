import scipy
import re
import numpy as np
from tire_generate_auto import planetary_gen, tire_gen, tire_gen_hinge, dolly_gen, build_track_veh, build_track_fixed
from step_gen import gen_steps
from utils_monte import get_gauss_rand

def monte_sim_wheel(sim_dict,file_name):
    payload_weight = get_gauss_rand(sim_dict["payload_mean"],sim_dict["payload_std"],sim_dict["payload_llim"],sim_dict["payload_ulim"])
    step_num=get_gauss_rand(sim_dict["step_num_mean"],sim_dict["step_num_std"],sim_dict["step_num_llim"],sim_dict["step_num_ulim"])
    step_rise=get_gauss_rand(sim_dict["step_rise_mean"],sim_dict["step_rise_std"],sim_dict["step_rise_llim"],sim_dict["step_rise_ulim"])
    step_slope=get_gauss_rand(sim_dict["step_slope_mean"],sim_dict["step_slope_std"],sim_dict["step_slope_llim"],sim_dict["step_slope_ulim"])

    payloadx=get_gauss_rand(sim_dict["payload_xloc_mean"],sim_dict["payload_xloc_std"],sim_dict["payload_xloc_llim"],sim_dict["payload_xloc_ulim"])
    payloadz=get_gauss_rand(sim_dict["payload_zloc_mean"],sim_dict["payload_zloc_std"],sim_dict["payload_zloc_llim"],sim_dict["payload_zloc_ulim"])
    friction=get_gauss_rand(sim_dict["friction_mean"],sim_dict["friction_std"],sim_dict["friction_llim"],sim_dict["friction_ulim"])
    count=1
    wheelbase=0
    radius=1
    while wheelbase-radius<=0:
        radius=get_gauss_rand(sim_dict["wheel_size_mean"],sim_dict["wheel_size_std"],sim_dict["wheel_size_llim"],sim_dict["wheel_size_ulim"])
        wheelbase=get_gauss_rand(sim_dict["wheelbase_mean"],sim_dict["wheelbase_std"],sim_dict["wheelbase_llim"],sim_dict["wheelbase_ulim"])
        count=count+1
        if count>100:
            print("Wheelbase error")
            return

    ## Change payload location ##
    if sim_dict["hinge"] ==1:
        string1=tire_gen_hinge(radius,wheelbase,payloadx,payloadz,payload_weight)
    elif sim_dict["track"]==1:
        string1=build_track_fixed(radius,wheelbase,payloadx,payloadz,payload_weight)
    else:
        string1=tire_gen(radius,wheelbase,payloadx,payloadz,payload_weight,sim_dict["front2rear_ratio"],friction)
    lines=string1

    ## Change step Geom ##
    string1 = gen_steps(step_num,step_rise,step_slope,friction)
    lines.append(string1)


    # file_name='envi.xml'
    f=open(file_name,"w")
    for i in lines:
        f.writelines(i)
    f.close()

    return np.array([radius,wheelbase,payloadx,payloadz, step_rise, step_slope,payload_weight])

def monte_sim_planet(sim_dict,file_name):
    payload_weight = get_gauss_rand(sim_dict["payload_mean"],sim_dict["payload_std"],sim_dict["payload_llim"],sim_dict["payload_ulim"])
    step_num=get_gauss_rand(sim_dict["step_num_mean"],sim_dict["step_num_std"],sim_dict["step_num_llim"],sim_dict["step_num_ulim"])
    step_rise=get_gauss_rand(sim_dict["step_rise_mean"],sim_dict["step_rise_std"],sim_dict["step_rise_llim"],sim_dict["step_rise_ulim"])
    step_slope=get_gauss_rand(sim_dict["step_slope_mean"],sim_dict["step_slope_std"],sim_dict["step_slope_llim"],sim_dict["step_slope_ulim"])

    payloadx=get_gauss_rand(sim_dict["payload_xloc_mean"],sim_dict["payload_xloc_std"],sim_dict["payload_xloc_llim"],sim_dict["payload_xloc_ulim"])
    payloadz=get_gauss_rand(sim_dict["payload_zloc_mean"],sim_dict["payload_zloc_std"],sim_dict["payload_zloc_llim"],sim_dict["payload_zloc_ulim"])
    wheel_num=int(get_gauss_rand(sim_dict["wheel_num_mean"],sim_dict["wheel_num_std"],sim_dict["wheel_num_llim"],sim_dict["wheel_num_ulim"]))
    friction=get_gauss_rand(sim_dict["friction_mean"],sim_dict["friction_std"],sim_dict["friction_llim"],sim_dict["friction_ulim"])
    count=1
    wheelbase=0
    sub_radius=0
    radius=1
    while wheelbase-(radius+sub_radius)<=0:
        radius=get_gauss_rand(sim_dict["wheel_size_mean"],sim_dict["wheel_size_std"],sim_dict["wheel_size_llim"],sim_dict["wheel_size_ulim"])
        wheelbase=get_gauss_rand(sim_dict["wheelbase_mean"],sim_dict["wheelbase_std"],sim_dict["wheelbase_llim"],sim_dict["wheelbase_ulim"])
        sub_radius=get_gauss_rand(sim_dict["sub_wheel_size_mean"],sim_dict["sub_wheel_size_std"],sim_dict["sub_wheel_size_llim"],sim_dict["sub_wheel_size_ulim"])
        count=count+1
        if count>100:
            print("Wheelbase error")
            return

    lines=planetary_gen(sub_radius,wheel_num,radius,wheelbase,payloadx,payloadz,payload_weight,sim_dict["fix_plans"],friction,sim_dict["planet_tread"])

    ## Change step Geom ##
    string1 = gen_steps(step_num,step_rise,step_slope,friction)
    lines.append(string1)

    file_name=file_name
    f=open(file_name,"w")
    for i in lines:
        f.writelines(i)
    f.close()

    return np.array([ sub_radius, wheel_num, radius, wheelbase, payloadx, payloadz, step_rise, step_slope,payload_weight])

def monte_sim_planet_dolly(sim_dict,file_name):
    payload_weight = get_gauss_rand(sim_dict["payload_mean"],sim_dict["payload_std"],sim_dict["payload_llim"],sim_dict["payload_ulim"])
    step_num=get_gauss_rand(sim_dict["step_num_mean"],sim_dict["step_num_std"],sim_dict["step_num_llim"],sim_dict["step_num_ulim"])
    step_rise=get_gauss_rand(sim_dict["step_rise_mean"],sim_dict["step_rise_std"],sim_dict["step_rise_llim"],sim_dict["step_rise_ulim"])
    step_slope=get_gauss_rand(sim_dict["step_slope_mean"],sim_dict["step_slope_std"],sim_dict["step_slope_llim"],sim_dict["step_slope_ulim"])

    payloadx=get_gauss_rand(sim_dict["payload_xloc_mean"],sim_dict["payload_xloc_std"],sim_dict["payload_xloc_llim"],sim_dict["payload_xloc_ulim"])
    payloadz=get_gauss_rand(sim_dict["payload_zloc_mean"],sim_dict["payload_zloc_std"],sim_dict["payload_zloc_llim"],sim_dict["payload_zloc_ulim"])
    wheel_num=int(get_gauss_rand(sim_dict["wheel_num_mean"],sim_dict["wheel_num_std"],sim_dict["wheel_num_llim"],sim_dict["wheel_num_ulim"]))
    count=1
    wheelbase=0
    sub_radius=0
    radius=1
    while wheelbase-(radius+sub_radius)<=0:
        radius=get_gauss_rand(sim_dict["wheel_size_mean"],sim_dict["wheel_size_std"],sim_dict["wheel_size_llim"],sim_dict["wheel_size_ulim"])
        wheelbase=get_gauss_rand(sim_dict["wheelbase_mean"],sim_dict["wheelbase_std"],sim_dict["wheelbase_llim"],sim_dict["wheelbase_ulim"])
        sub_radius=get_gauss_rand(sim_dict["sub_wheel_size_mean"],sim_dict["sub_wheel_size_std"],sim_dict["sub_wheel_size_llim"],sim_dict["sub_wheel_size_ulim"])
        count=count+1
        if count>100:
            print("Wheelbase error")
            return

    lines=dolly_gen(sub_radius,wheel_num,radius,wheelbase,payloadx,payloadz,payload_weight,sim_dict["stable_len"],sim_dict["fix_plans"],sim_dict["friction"])

    ## Change step Geom ##
    string1 = gen_steps(step_num,step_rise,step_slope,sim_dict["friction"])
    lines.append(string1)

    file_name=file_name
    f=open(file_name,"w")
    for i in lines:
        f.writelines(i)
    f.close()

    return np.array([ sub_radius, wheel_num, radius, wheelbase, payloadx, payloadz, step_rise, step_slope,payload_weight])

def ID_Stairs(lines):
    for i, stg in enumerate(lines):
        if re.search(r'floor', stg):
            return i

def Payload_loc(lines,payloadx,payloadz):
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

            lines[i]=stg[:re.search(vals[1],stg).regs[0][0]]+str(payloadx)+" 0.00 "+str(payloadz)+stg[re.search(vals[3],stg).regs[0][1]:]
    return start_s, stop_s, lines
