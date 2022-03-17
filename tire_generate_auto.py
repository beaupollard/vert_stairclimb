import numpy as np
import math

def tire_gen(radius,wheelbase,payloadx,payloadz,payload_weight,front2rear):

    half_width = 0.0125         # meters
    tread_height = 0.03175/2    # meters
    tread_width = 0.0508/2      # meters
    names = ['rf_','lf_','rb_','lb_']

    
    wheel_pos = np.array([[wheelbase,-0.4,-0.19],[wheelbase,0.4,-0.19],[-wheelbase,-0.4,-0.19],[-wheelbase,0.4,-0.19]])
    mass = 2
    num_treads=12
    theta = np.linspace(0,(360-360/num_treads)*math.pi/180,num_treads)
    tabs="\t\t\t"
    ## Setup the initial mujoco lines ##
    string1=[]
    string1.append('<mujoco model=\"env\">\n')
    string1.append('\t<size njmax=\"8000\" nconmax=\"4000\"/>\n\t<option timestep=\"0.0025\" />\n')
    string1.append('\t<actuator>\n')
    
    ## Specify the motor names and numbers ##
    for i in range(4):
        string1.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+str(i)+'\" name=\"motor'+str(i)+'\"/>\n')

    ## Finish setting up Mujoco inputs ##-0.15
    string1.append('\t</actuator>\n\n\t<worldbody>\n\t\t<body name=\"frame\" pos=\"-0.15 0 1.0\" quat=\"1.0 0.0 0 0\">\n')
    string1.append(tabs+'<geom mass=\"0.005\" pos=\"0 0 0\" rgba=\"1 0 0 0.35\" size=\"0.5 0.3 0.1651\" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"'+str(payload_weight)+'\" rgba=\"0 1 1 1\" size=\"0.025\" type=\"sphere\"/>\n\t\t\t</body>\n')
    string1.append(tabs+'<site name="winch" pos="0.5 0 0.0" size="0.1 0.1 0.1" rgba="0 1 0 0" type="sphere"/>\n')
    string1.append(tabs+'<camera euler=\"0 0 0\" fovy=\"40\" name=\"rgb\" pos=\"0 0 2.5\"></camera>\n')

    radius_in=radius
    ## Create the wheel ##
    for i,name in enumerate(names):
        if i <2:
            radius=radius_in*front2rear
        else:
            radius = radius_in

        string1.append(tabs+"<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i,0])+" "+str(wheel_pos[i,1])+" "+str(wheel_pos[i,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n")
        string1.append(tabs+"\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 0.25\" size=\""+str(radius) +" " + str(half_width)+"\" type=\"cylinder\"/>\n")
        string1.append(tabs+"\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+"\" type=\"hinge\"/>\n")
        string1.append(tabs+"\t<site name=\"wheel"+str(i)+"_t\" pos=\"0 0 0.0\" size='0.00005 0.00005 0.00005' rgba='0 1 0 1' type='sphere'/>\n")
        for j,ang in enumerate(theta):
            quat = ["{:.6f}".format(math.cos(ang/2)),"0.0","0.0","{:.6f}".format(math.sin(ang/2))]

            string1.append(tabs+"\t<body name=\""+name+"tread"+str(j)+"\" pos=\""+"{:.4f}".format((tread_height+radius)*math.cos(ang))+ " " + "{:.4f}".format((tread_height+radius)*math.sin(ang)) +" 0.0\" quat=\"" +quat[0]+" "+quat[1]+" "+quat[2]+" "+quat[3]+"\">\n")
            string1.append(tabs+"\t\t<geom mass=\"0.022\" rgba=\"0 0 1 0.25\" size=\""+"{:.3f}".format(tread_height) +" "+ "{:.3f}".format(tread_width) + " " + "{:.4f}".format(half_width) +"\" type=\"box\"/>\n")
            string1.append(tabs+"\t</body>\n")
        string1.append(tabs+"</body>\n")  
    string1.append("\t\t</body>\n")    

    return string1

def planetary_gen(sub_radius,wheel_num,radius,wheelbase,payloadx,payloadz,payload_weight):

    names = ['rf_','lf_','rb_','lb_']
    half_width = 0.0125   
    wheel_pos = np.array([[wheelbase,-0.4,-0.14],[wheelbase,0.4,-0.14],[-wheelbase,-0.4,-0.14],[-wheelbase,0.4,-0.14]])
    # wheel_pos = np.array([[wheelbase,-0.4,-0.19],[wheelbase,0.4,-0.19],[-wheelbase,-0.4,-0.19],[-wheelbase,0.4,-0.19]])
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
    string1.append(tabs+'<geom mass=\"0.005\" pos=\"0 0 0\" rgba=\"1 0 0 1\" size=\"0.5 0.3 0.1651\" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"'+str(payload_weight)+'\" rgba=\"0 0 1 1\" size=\"0.009 0.005 0.0125\" type=\"box\"/>\n\t\t\t</body>\n')
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
    string1.append("\t\t</body>\n")         

    return string1

def tire_gen_hinge(radius,wheelbase,payloadx,payloadz,payload_weight):

    half_width = 0.0125         # meters
    tread_height = 0.03175/4    # meters
    tread_width = 0.0508/2      # meters
    names = ['rf_','lf_','rb_','lb_']
    wheelbase = wheelbase/2.
    
    wheel_pos = np.array([[wheelbase,-0.4,-0.19],[wheelbase,0.4,-0.19],[-wheelbase,-0.4,-0.19],[-wheelbase,0.4,-0.19]])
    mass = 2
    num_treads=16
    theta = np.linspace(0,(360-360/num_treads)*math.pi/180,num_treads)
    tabs="\t\t\t"
    ## Setup the initial mujoco lines ##
    string1=[]
    string1.append('<mujoco model=\"env\">\n')
    string1.append('\t<size njmax=\"8000\" nconmax=\"4000\"/>\n\t<option timestep=\"0.0025\" />\n')
    string1.append('\t<actuator>\n')
    
    ## Specify the motor names and numbers ##
    for i in range(4):
        string1.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+str(i)+'\" name=\"motor'+str(i)+'\"/>\n')

    ## Finish setting up Mujoco inputs ##-0.15
    string1.append('\t</actuator>\n\n\t<worldbody>\n\t\t<body name=\"frame\" pos=\"-0.15 0 1.0\" quat=\"1.0 0.0 0 0\">\n')
    string1.append(tabs+'<geom mass=\"0.01\" pos=\"0 0 0\" rgba=\"1 0 0 0.35\" size=\"0.2 0.3 0.1651\" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"'+str(payload_weight)+'\" rgba=\"0 1 1 1\" size=\"0.025\" type=\"sphere\"/>\n\t\t\t</body>\n')
    string1.append(tabs+'<site name="winch" pos="0.5 0 0.0" size="0.1 0.1 0.1" rgba="0 1 0 0" type="sphere"/>\n')
    string1.append(tabs+'<camera euler=\"0 0 0\" fovy=\"40\" name=\"rgb\" pos=\"0 0 2.5\"></camera>\n')

    radius_in=radius
    ## Create the wheel ##
    for i,name in enumerate(names[0:2]):

        string1.append(tabs+"<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i,0])+" "+str(wheel_pos[i,1])+" "+str(wheel_pos[i,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n")
        string1.append(tabs+"\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 0.25\" size=\""+str(radius) +" " + str(half_width)+"\" type=\"cylinder\"/>\n")
        string1.append(tabs+"\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+"\" type=\"hinge\"/>\n")
        string1.append(tabs+"\t<site name=\"wheel"+str(i)+"_t\" pos=\"0 0 0.0\" size='0.00005 0.00005 0.00005' rgba='0 1 0 1' type='sphere'/>\n")
        for j,ang in enumerate(theta):
            quat = ["{:.6f}".format(math.cos(ang/2)),"0.0","0.0","{:.6f}".format(math.sin(ang/2))]

            string1.append(tabs+"\t<body name=\""+name+"tread"+str(j)+"\" pos=\""+"{:.4f}".format((tread_height+radius)*math.cos(ang))+ " " + "{:.4f}".format((tread_height+radius)*math.sin(ang)) +" 0.0\" quat=\"" +quat[0]+" "+quat[1]+" "+quat[2]+" "+quat[3]+"\">\n")
            string1.append(tabs+"\t\t<geom mass=\"0.022\" rgba=\"0 0 1 0.25\" size=\""+"{:.3f}".format(tread_height) +" "+ "{:.3f}".format(tread_width) + " " + "{:.4f}".format(half_width) +"\" type=\"box\"/>\n")
            string1.append(tabs+"\t</body>\n")
        string1.append(tabs+"</body>\n")

    string1.append(tabs+'<body name="frame2" pos="-0.45 0 0.0" quat="1.0 0.0 0 0">\n')
    string1.append(tabs+'\t'+'<geom mass="0.01" pos="0 0 0" rgba="1 0 0 0.35" size="0.2 0.3 0.1651" type="box"></geom>\n')
    string1.append(tabs+'\t'+'<joint axis="0 1 0" pos="0.25 0 0" name="body_connect" type="hinge" stiffness="2000" limited="true" range="-20 20" damping="300." />\n')
    
    ## Create the wheel for 2nd body##
    for i,name in enumerate(names[2:]):

        string1.append(tabs+"\t<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i+2,0])+" "+str(wheel_pos[i+2,1])+" "+str(wheel_pos[i+2,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n")
        string1.append(tabs+"\t\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 0.25\" size=\""+str(radius) +" " + str(half_width)+"\" type=\"cylinder\"/>\n")
        string1.append(tabs+"\t\t<joint axis=\"0 0 1\" name=\"wheel"+str(i+2)+"\" type=\"hinge\"/>\n")
        string1.append(tabs+"\t\t<site name=\"wheel"+str(i+2)+"_t\" pos=\"0 0 0.0\" size='0.00005 0.00005 0.00005' rgba='0 1 0 1' type='sphere'/>\n")
        for j,ang in enumerate(theta):
            quat = ["{:.6f}".format(math.cos(ang/2)),"0.0","0.0","{:.6f}".format(math.sin(ang/2))]

            string1.append(tabs+"\t\t<body name=\""+name+"tread"+str(j)+"\" pos=\""+"{:.4f}".format((tread_height+radius)*math.cos(ang))+ " " + "{:.4f}".format((tread_height+radius)*math.sin(ang)) +" 0.0\" quat=\"" +quat[0]+" "+quat[1]+" "+quat[2]+" "+quat[3]+"\">\n")
            string1.append(tabs+"\t\t\t<geom mass=\"0.022\" rgba=\"0 0 1 0.25\" size=\""+"{:.3f}".format(tread_height) +" "+ "{:.3f}".format(tread_width) + " " + "{:.4f}".format(half_width) +"\" type=\"box\"/>\n")
            string1.append(tabs+"\t\t</body>\n")
        string1.append(tabs+"\t</body>\n")  
    string1.append(tabs+"</body>\n")  
    string1.append("\t\t</body>\n")    

    return string1
