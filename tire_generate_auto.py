import numpy as np
import math

def tire_gen(sim_dict):
    ## Ensure that tire radius > 4 inches and that tires aren't overlapping
    radius = 0.1
    posx=0.1
    while radius<0.1016 or posx<radius:
        radius = np.random.normal(sim_dict["wheel_size_mean"],sim_dict["wheel_size_std"])            # meters
        posx = np.random.normal(sim_dict["wheelbase_mean"],sim_dict["wheelbase_std"]) 

    half_width = 0.0125         # meters
    tread_height = 0.03175/2    # meters
    tread_width = 0.0508/2      # meters
    names = ['rf_','lf_','rb_','lb_']

    
    wheel_pos = np.array([[posx,-0.4,-0.19],[posx,0.4,-0.19],[-posx,-0.4,-0.19],[-posx,0.4,-0.19]])
    mass = 1
    num_treads=16
    theta = np.linspace(0,(360-360/num_treads)*math.pi/180,num_treads)
    tabs="\t\t\t"
    string1 = []

    ## Create the wheel ##
    for i,name in enumerate(names):
        string1.append(tabs+"<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i,0])+" "+str(wheel_pos[i,1])+" "+str(wheel_pos[i,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n")
        string1.append(tabs+"\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 1\" size=\""+str(radius) +" " + str(half_width)+"\" type=\"cylinder\"/>\n")
        string1.append(tabs+"\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+"\" type=\"hinge\"/>\n")
        string1.append(tabs+"\t<site name=\"wheel"+str(i)+"_t\" pos=\"0 0 0.0\" size='0.00005 0.00005 0.00005' rgba='0 1 0 1' type='sphere'/>\n")
        for j,ang in enumerate(theta):
            quat = ["{:.6f}".format(math.cos(ang/2)),"0.0","0.0","{:.6f}".format(math.sin(ang/2))]

            string1.append(tabs+"\t<body name=\""+name+"tread"+str(j)+"\" pos=\""+"{:.4f}".format(radius*math.cos(ang))+ " " + "{:.4f}".format(radius*math.sin(ang)) +" 0.0\" quat=\"" +quat[0]+" "+quat[1]+" "+quat[2]+" "+quat[3]+"\">\n")
            string1.append(tabs+"\t\t<geom mass=\"0.001\" rgba=\"0 0 1 1\" size=\""+"{:.3f}".format(tread_height) +" "+ "{:.3f}".format(tread_width) + " " + "{:.4f}".format(half_width) +"\" type=\"box\"/>\n")
            string1.append(tabs+"\t</body>\n")
        string1.append(tabs+"</body>\n")     

    return string1, radius, posx

def planetary_gen(sim_dict):
    ## Ensure that tire radius > 4 inches and that tires aren't overlapping
    sub_radius=0.05
    while sub_radius<0.0501:
        sub_radius=np.random.normal(sim_dict["sub_wheel_size_mean"],sim_dict["sub_wheel_size_std"])

    radius = 0.1
    posx=0.1
    while radius<0.1016 or posx<radius+sub_radius:
        radius = np.random.normal(sim_dict["wheel_size_mean"],sim_dict["wheel_size_std"])            # meters
        posx = np.random.normal(sim_dict["wheelbase_mean"],sim_dict["wheelbase_std"]) 
    
    wheel_num=2
    while wheel_num<3:
        wheel_num = round(np.random.normal(3,1)) 
    half_width = 0.0125         

    payloadx = -0.1
    while payloadx <-0.05:
        payloadx = np.random.normal(sim_dict["payload_xloc_mean"],sim_dict["payload_xloc_std"])
    payloadz = 0.3
    while abs(payloadz) >0.2:
        payloadz = np.random.normal(sim_dict["payload_zloc_mean"],sim_dict["payload_zloc_std"])

    ## Use to check particular cases ##
    # inp = [0.06082726298381294, 4.0, 0.2044621317366804, 0.3580181650193848, 0.22947856416144757, -0.12361366987075753]
    # sub_radius = inp[0]
    # wheel_num = int(inp[1])
    # radius = inp[2]
    # posx =  inp[3]
    # payloadx =  inp[4]
    # payloadz = inp[5]

    names = ['rf_','lf_','rb_','lb_']

    
    wheel_pos = np.array([[posx,-0.4,-0.19],[posx,0.4,-0.19],[-posx,-0.4,-0.19],[-posx,0.4,-0.19]])
    mass = 1
    theta = np.linspace(0,(360-360/wheel_num)*math.pi/180,wheel_num)
    tabs="\t\t\t"

    ## Setup the initial mujoco lines ##
    string1=[]
    string1.append('<mujoco model=\"env\">\n')
    string1.append('\t<size njmax=\"8000\" nconmax=\"4000\"/>\n\t<option timestep=\"0.0025\" />\n')
    string1.append('\t<actuator>\n')
    
    ## Specify the motor names and numbers ##
    for i in range(4):
        for j in range(wheel_num+1):
            string1.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+str(i)+str(j)+'\" name=\"motor'+str(i)+str(j)+'\"/>\n')
    
    ## Finish setting up Mujoco inputs ##
    string1.append('\t</actuator>\n\n\t<worldbody>\n\t\t<body name=\"frame\" pos=\"-0.15 0 1.0\" quat=\"1.0 0.0 0 0\">\n')
    string1.append(tabs+'<geom mass=\"50.0\" pos=\"0 0 0\" rgba=\"1 0 0 1\" size=\"0.55 0.3 0.2\" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"40.\" rgba=\"0 0 1 1\" size=\"0.009 0.005 0.0125\" type=\"box\"/>\n\t\t\t</body>\n')
    string1.append(tabs+'<camera euler=\"0 0 0\" fovy=\"40\" name=\"rgb\" pos=\"0 0 2.5\"></camera>\n')
    ## Create the wheel ##
    for i,name in enumerate(names):
        string1.append(tabs+"<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i,0])+" "+str(wheel_pos[i,1])+" "+str(wheel_pos[i,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n")
        string1.append(tabs+"\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 1\" size=\""+str(0.05) +" " + str(half_width)+"\" type=\"cylinder\"/>\n")
        string1.append(tabs+"\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+"0\" type=\"hinge\"/>\n")
        if (i% 2) == 0:
            zloc=0.03
        else:
            zloc=-0.03
        for j,ang in enumerate(theta):

            string1.append(tabs+"\t<body name=\""+name+"subwheel"+str(j)+"\" pos=\""+"{:.4f}".format(radius*math.cos(ang))+ " " + "{:.4f}".format(radius*math.sin(ang)) +" "+str(zloc)+"\" >\n")
            string1.append(tabs+"\t\t<geom mass=\"1.0\" rgba=\"0 0 1 1\" size=\""+"{:.3f}".format(sub_radius) +" "+ " " + "{:.4f}".format(half_width) +"\" type=\"cylinder\"/>\n")
            string1.append(tabs+"\t\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+str(j+1)+"\" type=\"hinge\"/>\n")
            string1.append(tabs+"\t</body>\n")
        string1.append(tabs+"</body>\n")     

    return string1, sub_radius, wheel_num, radius, posx, payloadx, payloadz