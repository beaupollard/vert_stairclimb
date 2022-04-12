import numpy as np
import math

def tire_gen(radius,wheelbase,payloadx,payloadz,payload_weight,front2rear):

    half_width = 0.0125         # meters
    tread_height = 0.03175/2    # meters
    tread_width = 0.0508/2      # meters
    names = ['rf_','lf_','rb_','lb_']

    mass = 2
    num_treads=12
    _, wheelbase = Get_track_parms(tread_height,radius,num_treads,wheelbase)
    wheel_pos = np.array([[wheelbase,-0.4,-0.19],[wheelbase,0.4,-0.19],[-wheelbase,-0.4,-0.19],[-wheelbase,0.4,-0.19]])

    theta = np.linspace(0,(360-360/num_treads)*math.pi/180,num_treads)+(0.9*180/num_treads*math.pi/180)
    tabs="\t\t\t"
    ## Setup the initial mujoco lines ##
    string1=[]
    string1.append('<mujoco model=\"env\">\n')
    string1.append('\t<size njmax=\"8000\" nconmax=\"4000\"/>\n\t<option timestep=\"0.0025\" />\n')

    # if tracked==1:
    #     string2, anchor=build_track(radius,wheelbase,tabs,wheel_pos,tread_width,tread_height,num_treads)
    #     string1.append('\t<contact>\n\t\t<exclude body1="Bl00" body2="rmf" />\n\t</contact>\n')
    #     string1.append('\t<equality>\n\t\t<connect body1="Bl00" body2="rmf" anchor="'+str(anchor[0])+' '+str(anchor[1])+' '+str(anchor[2])+'" solref="0.01 1" solimp="0.99 0.99 0.001 0.5 2" />\n\t</equality>\n')        



        
    string1.append('\t<actuator>\n')
    
    ## Specify the motor names and numbers ##
    for i in range(4):
        string1.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+str(i)+'\" name=\"motor'+str(i)+'\"/>\n')

    ## Finish setting up Mujoco inputs ##-0.15
    string1.append('\t</actuator>\n\n\t<worldbody>\n\t\t<body name=\"frame\" pos=\"0.0 0 0.0\" quat=\"1.0 0.0 0 0\">\n')
    string1.append(tabs+'<geom mass=\"0.005\" pos=\"0 0 0\" rgba=\"1 0 0 1.0\" size=\"0.5 0.3 0.1651\" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"'+str(payload_weight)+'\" rgba=\"0 1 1 1\" size=\"0.025\" type=\"sphere\"/>\n\t\t\t</body>\n')
    string1.append(tabs+'<site name="winch" pos="0.5 0 0.0" size="0.1 0.1 0.1" rgba="0 1 0 0" type="sphere"/>\n')
    # string1.append(tabs+'<camera euler=\"0 0 0\" fovy=\"40\" name=\"rgb\" pos=\"0 0 2.5\"></camera>\n')

    radius_in=radius
    ## Create the wheel ##
    for i,name in enumerate(names):
        if i <2:
            radius=radius_in*front2rear
        else:
            radius = radius_in

        string1.append(tabs+"<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i,0])+" "+str(wheel_pos[i,1])+" "+str(wheel_pos[i,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n")
        string1.append(tabs+"\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 1.0\" size=\""+str(radius) +" " + str(half_width)+"\" type=\"cylinder\"/>\n")
        string1.append(tabs+"\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+"\" type=\"hinge\"/>\n")
        string1.append(tabs+"\t<site name=\"wheel"+str(i)+"_t\" pos=\"0 0 0.0\" size='0.00005 0.00005 0.00005' rgba='0 1 0 1' type='sphere'/>\n")
        for j,ang in enumerate(theta):
            quat = ["{:.6f}".format(math.cos(ang/2)),"0.0","0.0","{:.6f}".format(math.sin(ang/2))]

            string1.append(tabs+"\t<body name=\""+name+"tread"+str(j)+"\" pos=\""+"{:.4f}".format((tread_height+radius)*math.cos(ang))+ " " + "{:.4f}".format((tread_height+radius)*math.sin(ang)) +" 0.0\" quat=\"" +quat[0]+" "+quat[1]+" "+quat[2]+" "+quat[3]+"\">\n")
            string1.append(tabs+"\t\t<geom mass=\"0.022\" rgba=\"0 0 1 1.0\" size=\""+"{:.3f}".format(tread_height) +" "+ "{:.3f}".format(tread_width) + " " + "{:.4f}".format(half_width) +"\" type=\"box\"/>\n")
            string1.append(tabs+"\t</body>\n")
        string1.append(tabs+"</body>\n")
    string1.append("\t\t</body>\n")

    return string1

def planetary_gen(sub_radius,wheel_num,radius,wheelbase,payloadx,payloadz,payload_weight):

    names = ['rf_','lf_','rb_','lb_']
    half_width = 0.0125   
    wheel_pos = np.array([[wheelbase,-0.4,-0.19],[wheelbase,0.4,-0.19],[-wheelbase,-0.4,-0.19],[-wheelbase,0.4,-0.19]])
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
    string1.append(tabs+'<site name="winch" pos="0.5 0 0.0" size="0.1 0.1 0.1" rgba="0 1 0 0" type="sphere"/>\n')
    # string1.append(tabs+'<camera euler=\"0 0 0\" fovy=\"40\" name=\"rgb\" pos=\"0 0 2.5\"></camera>\n')
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

def dolly_gen(sub_radius,wheel_num,radius,wheelbase,payloadx,payloadz,payload_weight,stable_len,fix_plan,friction):
    
    names = ['rf_','lf_']
    half_width = 0.0125   
    wheel_pos = np.array([[0.,-0.4,0.],[0.,0.4,0.]])
    mass = 1
    theta = np.linspace(0,(360-360/wheel_num)*math.pi/180,wheel_num)
    tabs="\t\t\t"

    ## Setup the initial mujoco lines ##
    string1=[]
    string1.append('<mujoco model=\"env\">\n')
    string1.append('\t<size njmax=\"8000\" nconmax=\"4000\"/>\n\t<option timestep=\"0.0025\" />\n')
    string1.append('\t<actuator>\n')
    
    ## Specify the motor names and numbers ##
    for i in range(2):
        if fix_plan==0:
            for j in range(wheel_num+1):
                string1.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+str(i)+str(j)+'\" name=\"motor'+str(i)+str(j)+'\"/>\n')
        else:
            string1.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+str(i)+str(0)+'\" name=\"motor'+str(i)+str(0)+'\"/>\n')

    ## Finish setting up Mujoco inputs ##
    string1.append('\t</actuator>\n\n\t<worldbody>\n\t\t<body name=\"frame\" pos=\"-0.15 0 1.0\" quat=\"1.0 0.0 0 0\">\n')
    string1.append(tabs+'<geom mass=\"0.5\" pos=\"0 0 0\" rgba=\"1 0 0 1\" size=\"0.0254 0.3 0.0127\" friction="'+str(friction)+' 0.005 0.0001" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"'+str(payload_weight)+'\" rgba=\"0 0 1 1\" size=\"0.009 0.005 0.0125\" type=\"box\"/>\n\t\t\t</body>\n')
    string1.append(tabs+'<site name="winch" pos="0.5 0 0.0" size="0.1 0.1 0.1" rgba="0 1 0 0" type="sphere"/>\n')
    # string1.append(tabs+'<camera euler=\"0 0 0\" fovy=\"40\" name=\"rgb\" pos=\"0 0 2.5\"></camera>\n')
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
            string1.append(tabs+"\t\t<geom mass=\"1.0\" rgba=\"0 0 1 1\" size=\""+"{:.3f}".format(sub_radius) +" "+ " " + "{:.4f}".format(half_width) +"\" friction=\""+str(friction)+" 0.005 0.0001\" type=\"cylinder\"/>\n")
            if fix_plan==0:
                string1.append(tabs+"\t\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+str(j+1)+"\" type=\"hinge\"/>\n")
            string1.append(tabs+"\t</body>\n")
        string1.append(tabs+"</body>\n")
    string1.append(tabs+'<body name="stable" pos="'+str(-(stable_len+0.0254))+' 0.0000 0.0" >\n'+tabs+'\t<geom mass="0.5" rgba="0 0 1 1" size="'+str(stable_len)+' 0.0127 0.0127" type="box"/>\n'+tabs+'</body>"\n')
				
			
    string1.append("\t\t</body>\n")         

    return string1

def build_track_old(radius,wheelbase,tabs,wheel_pos,tread_width,tread_height,num_treads):

    # tread_length = total_length/40. # Change to automate the number of treads

    string1=[]
    dx, _ = Get_track_parms(tread_height,radius,num_treads,wheelbase)
    widthx=2*math.pi*(radius+tread_height)/num_treads/6.
    widthy=0.05
    widthz=0.025/2    
    string1.append('\t\t<body name="rml" pos="'+str(wheel_pos[-2,0]+wheelbase/2)+' '+str(wheel_pos[-2,1])+' '+str(0*wheel_pos[-2,2])+'" quat="0.7071 0.7071 0 0">\n')
    string1.append(tabs+'<geom mass="0.005" pos="0 0 0" rgba="1 1 1 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder"></geom>\n')
    string1.append(tabs+'<joint type="free" name="l0" pos="0 0 0"/>\n')
    # string1.append(tabs+'<body name="mlp'+str(0)+'" pos="'+str(0.0)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
    # string1.append(tabs+'\t<geom mass="0.005" pos="0 0 '+str(widthz)+'" rgba="1 1 0 1.0" size="'+str(dx*0.45)+' '+str(widthy)+ ' '+str(widthz/4)+'" type="box"></geom>\n')
    # string1.append(tabs+'</body>\n')    

    count=0
    ## Top links ##
    for i in range(math.floor(wheelbase/dx)*2):
        string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(dx)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder"></geom>\n')
        string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(dx/2)+' '+str(0.0)+' '+str(0.0)+'" axis="0 0 1"/>\n')
        # string1.append(tabs+'\t<body name="tp'+str(count)+'" pos="'+str(0.0)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
        # string1.append(tabs+'\t\t<geom mass="0.005" pos="0 0 '+str(widthz)+'" rgba="1 1 0 1.0" size="'+str(dx*0.45)+' '+str(widthy)+ ' '+str(widthz/4)+'" type="box"></geom>\n')
        # string1.append(tabs+'\t</body>\n')
        tabs=tabs+'\t'
        count=count+1

    for i in range(int(num_treads/2)-1):#int(num_treads/2)):
        string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(0)+' '+str(-dx)+' '+str(0)+'" quat="1 0 0 0">\n')

        string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="1 0 0 0"></geom>\n')
        
        string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(0)+' '+str(-dx/2)+' '+str(0)+'" axis="0 0 1"/>\n')

        tabs=tabs+'\t'  
        count=count+1 

    for i in range(math.floor(wheelbase/dx)*2):
        string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(-dx)+' '+str(0)+' '+str(0)+'" quat="1 0 0 0">\n')

        string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="1 0 0 0"></geom>\n')
        
        string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(-dx/2)+' '+str(0)+' '+str(0)+'" axis="0 0 1"/>\n')

        tabs=tabs+'\t'  
        count=count+1    

    for i in range(int(num_treads/2)-3):#int(num_treads/2)):
        string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(0)+' '+str(dx)+' '+str(0)+'" quat="1 0 0 0">\n')

        string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="1 0 0 0"></geom>\n')
        
        string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(0)+' '+str(dx/2)+' '+str(0)+'" axis="0 0 1"/>\n')

        tabs=tabs+'\t'  
        count=count+1 

    string1.append(tabs+'<body name="rmf'+str(count)+'" pos="'+str(0)+' '+str(dx)+' '+str(0)+'" quat="1 0 0 0">\n')

    string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 1 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="1 0 0 0"></geom>\n')
    tabs=tabs+'\t'  
    count=count+1     
    # string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(0)+' '+str(dx/2)+' '+str(0)+'" axis="0 0 1"/>\n')

    # theta0 = np.linspace(math.pi/2,-math.pi/2,int(num_treads/2))-2*math.pi/(num_treads)
    # x0=[]
    # z0=[]
    # for i in range(int(num_treads/2)):
    #     x0.append((radius+tread_height*1.5)*math.cos(theta0[i]))
    #     z0.append((radius+tread_height*1.5)*math.cos(theta0[i]))

    # for i in range(len(x0)-1):
    #     string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(x0[i+1]-x0[i])+' '+str(z0[i+1]-z0[i])+' '+str(0)+'" quat="1 0 0 0">\n')

    #     string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="1 0 0 0"></geom>\n')
        
    #     string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str((x0[i+1]-x0[i])/2)+' '+str((z0[i+1]-z0[i])/2)+' '+str(0)+'" axis="0 0 1"/>\n')

    #     tabs=tabs+'\t'  
    #     count=count+1 

    # theta = np.linspace(math.pi/2,-math.pi/2-math.pi/(num_treads/2),int(num_treads/2)+1)
    # theta0 = np.linspace(math.pi/2,-math.pi/2,int(num_treads/2))-2*math.pi/(num_treads)
    # theta2=(math.pi-(theta0[1]-theta0[0]))/2

    # for i in range(int(num_treads/2)-1):#int(num_treads/2)):
    #     theta=-(math.pi-theta2-theta0[i])
    #     xdelta=dx*(math.cos(theta))
    #     zdelta=dx*(math.sin(theta))   

    #     string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(xdelta)+' '+str(zdelta)+' '+str(0)+'" quat="1 0 0 0">\n')

    #     string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="1 0 0 0"></geom>\n')
        
    #     string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(xdelta/2)+' '+str(zdelta/2)+' '+str(0)+'" axis="0 0 1"/>\n')

    #     tabs=tabs+'\t'  
    #     count=count+1 



    # ## Bottom links ##
    # for i in range(math.floor(wheelbase/dx)*2):
    #     string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(-dx)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
    #     string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder"></geom>\n')
    #     string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(0.0)+'" axis="0 0 1"/>\n')
    #     # string1.append(tabs+'\t<body name="tp'+str(count)+'" pos="'+str(0.0)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
    #     # string1.append(tabs+'\t\t<geom mass="0.005" pos="0 0 '+str(widthz)+'" rgba="1 1 0 1.0" size="'+str(dx*0.45)+' '+str(widthy)+ ' '+str(widthz/4)+'" type="box"></geom>\n')
    #     # string1.append(tabs+'\t</body>\n')
    #     tabs=tabs+'\t'
    #     count=count+1

  
    tot_tab=len(tabs.split("\t"))
    for i in range(tot_tab-2,1,-1):
        tab2='\t'*i
        string1.append(tab2+'</body>\n')        
    return string1

def build_track_rec(radius,wheelbase,tabs,wheel_pos,tread_width,tread_height,num_treads):
    # total_length = (wheelbase*2+2*math.pi*radius)*1.05

    # tread_length = total_length/40. # Change to automate the number of treads
    widthx=2*math.pi*(radius+tread_height*2)/num_treads/6.
    widthy=0.05
    widthz=0.025/2
    string1=[]
    p0=[wheel_pos[-2,0], wheel_pos[-2,1], wheel_pos[-2,2]]
    dx = 2*math.pi*radius/num_treads
    string1.append('\t\t<body name="rml" pos="'+str(wheel_pos[-2,0])+' '+str(wheel_pos[-2,1])+' '+str(0*wheel_pos[-2,2])+'" quat="1.0 0.0 0 0">\n')
    string1.append(tabs+'<geom mass="0.005" pos="0 0 0" rgba="1 1 1 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="box"></geom>\n')
    string1.append(tabs+'<joint type="free" name="l0" pos="0 0 0"/>\n')
    string1.append(tabs+'<body name="mlp'+str(0)+'" pos="'+str(0.0)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
    string1.append(tabs+'\t<geom mass="0.005" pos="0 0 '+str(widthz)+'" rgba="1 1 0 1.0" size="'+str(dx*0.45)+' '+str(widthy)+ ' '+str(widthz/4)+'" type="box"></geom>\n')
    string1.append(tabs+'</body>\n')    

    count=0
    ## Top links ##
    for i in range(math.ceil(wheelbase*2/dx)):
        string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(dx)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="box"></geom>\n')
        string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(dx/2)+' '+str(0.0)+' '+str(0.0)+'" axis="0 1 0"/>\n')
        string1.append(tabs+'\t<body name="tp'+str(count)+'" pos="'+str(0.0)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
        string1.append(tabs+'\t\t<geom mass="0.005" pos="0 0 '+str(widthz)+'" rgba="1 1 0 1.0" size="'+str(dx*0.45)+' '+str(widthy)+ ' '+str(widthz/4)+'" type="box"></geom>\n')
        string1.append(tabs+'\t</body>\n')
        tabs=tabs+'\t'
        count=count+1

    # theta = math.pi/6*np.ones(int(num_treads/2))#np.linspace(math.pi/2,-math.pi/2,int(num_treads/2))-math.pi/(num_treads/2)
    theta = np.linspace(math.pi/2,-math.pi/2-math.pi/(num_treads/2),int(num_treads/2)+1)
    # theta = np.linspace(math.pi/2,-math.pi/2,int(num_treads/2))-math.pi/(num_treads/2)
    # theta = np.linspace(0,-math.pi-math.pi/(num_treads/2),int(num_treads/2)+1)
    ## Front Links ##
    for i in range(2):#int(num_treads/2)):
        r=abs((wheel_pos[0,-1])+widthz)
        # xdelta=dx*(math.cos(theta[i]))#-math.cos(theta[i]))
        # zdelta=dx*(math.sin(theta[i]))#-math.sin(theta[i]))
        xdelta=r*(math.cos(theta[i+1])-math.cos(theta[i]))
        zdelta=r*(math.sin(theta[i+1])-math.sin(theta[i]))   
        p=-np.array([0,xdelta,0,zdelta])      
        if i > 0:           
            c2=math.cos(theta[i+1]/2)*(-math.cos(theta[i]/2))
            s2=math.sin(theta[i+1]/2)*math.sin(theta[i]/2)
            qi=np.array([c2,0,-s2,0])
            q=np.array([c2,0,s2,0])
            p2=np.dot(np.dot(q,p),qi)
            xdelta=p2[1]
            zdelta=p2[-1]
            # print((theta[i+1]/2)*180/math.pi)
        else:
            c2=math.cos(theta[i+1]/2)
            s2=math.sin(theta[i+1]/2)
       
        # string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(xdelta)+' '+str(0.0)+' '+str(zdelta)+'" quat="'+str(1)+' 0 '+str(0)+' 0'+'">\n')
        string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(xdelta)+' '+str(0.0)+' '+str(zdelta)+'" quat="'+str(c2)+' 0 '+str(s2)+' 0'+'">\n')
        # string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(dx*math.cos(theta[i]))+' '+str(0.0)+' '+str(dx*math.sin(theta[i]))+'" quat="'+str(1)+' 0 '+str(0)+' 0'+'">\n')
        # string1.append(tabs+'<body name="rl0'+str(count)+'" pos="'+str(dx*math.cos(theta[i]))+' '+str(0.0)+' '+str(dx*math.sin(theta[i]))+'" quat="'+str(math.cos(-theta[i]/2))+' 0 '+str(math.sin(-theta[i]/2))+' 0'+'">\n')
        
        # string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="box" quat="'+str(math.cos(theta[i+1]/2))+' 0 '+str(math.sin(theta[i+1]/2))+' 0"></geom>\n')
        string1.append(tabs+'\t<geom mass="0.005" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="box" quat="1 0 0 0"></geom>\n')
        
        string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(dx/2*math.cos(theta[i]))+' '+str(0.0)+' '+str(dx/2*math.sin(theta[i]))+'" axis="0 1 0"/>\n')
        string1.append(tabs+'\t<body name="tp'+str(count)+'" pos="'+str(0.0)+' '+str(0.0)+' '+str(0.0)+'" quat="1.0 0.0 0 0">\n')
        
        # string1.append(tabs+'\t\t<geom mass="0.005" pos="0 0 '+str(widthz)+'" rgba="1 1 0 1.0" size="'+str(dx*0.45)+' '+str(widthy)+ ' '+str(widthz/4)+'" type="box" quat="'+str(math.cos(theta[i+1]/2))+' 0 '+str(math.sin(theta[i+1]/2))+' 0"></geom>\n')
        string1.append(tabs+'\t\t<geom mass="0.005" pos="0 0 '+str(widthz)+'" rgba="1 1 0 1.0" size="'+str(dx*0.45)+' '+str(widthy)+ ' '+str(widthz/4)+'" type="box" quat="1 0 0 0"></geom>\n')
        
        string1.append(tabs+'\t</body>\n')
        tabs=tabs+'\t'  
        count=count+1 
  
    tot_tab=len(tabs.split("\t"))
    for i in range(tot_tab-2,1,-1):
        tab2='\t'*i
        string1.append(tab2+'</body>\n')
    return string1

def Get_track_parms(tread_height,radius,num_treads,wheelbase):

    tread_height=tread_height*1.5
    theta = 2*math.pi/num_treads
    x0=((tread_height+radius)*math.cos(theta)-(tread_height+radius))**2
    y0=((tread_height+radius)*math.sin(theta))**2
    dx = (x0+y0)**0.5
    return dx, round(wheelbase/dx)*dx

def build_track(radius,wheelbase,tabs,wheel_pos,tread_width,tread_height,num_treads):

    ## Build Ellipse ##
    a = wheelbase+(radius+tread_height)*1.1
    b = radius+tread_height
    dx, _ = Get_track_parms(tread_height,radius,num_treads,wheelbase)
    h=(a-b)**2/(a+b)**2
    perim=math.pi*(a+b)*(1+(3*h)/(10+(4-3*h)**0.5))
    track_width=dx*0.35
    ## Set ellipse parameter based on link pitch ##
    while perim%dx/dx>0.01:
        a=a+0.001
        b=b+0.001
        h=(a-b)**2/(a+b)**2
        perim=math.pi*(a+b)*(1+(3*h)/(10+(4-3*h)**0.5))
    n_links=round(perim/dx)
    dtheta=2*math.pi/n_links
    theta = np.zeros(n_links)

    ## Space the links equally ##
    for i in range(n_links-1):       
        theta[i+1]=theta[i]+math.pi/180
        err=1
        while err>0.0001:
            x1=a*math.cos(theta[i+1])
            y1=b*math.sin(theta[i+1]) 
            x0=a*math.cos(theta[i])
            y0=b*math.sin(theta[i]) 
            f=(x1-x0)**2+(y1-y0)**2-dx**2
            dfdt=2*(x1-x0)*(-a*math.sin(theta[i+1]))+2*(y1-y0)*(b*math.cos(theta[i+1]))
            theta[i+1]=theta[i+1]-0.01*f/dfdt
            x1=a*math.cos(theta[i+1])
            y1=b*math.sin(theta[i+1]) 
            err = abs(1-(((x1-x0)**2+(y1-y0)**2)**0.5/dx))

    string1=[]
    
    widthx=2*math.pi*(radius+tread_height)/num_treads/6.
    widthy=0.05
    widthz=0.025/2   

    x1=a*math.cos(theta[-1])
    y1=b*math.sin(theta[-1]) 
    x0=a*math.cos(theta[0])
    y0=b*math.sin(theta[0])     
    string1.append('\t\t<body name="bml" pos="'+str(0)+' '+str(0)+' '+str(0)+'" quat="1 0 0 0">\n')
    string1.append(tabs+'<geom mass="0.02" pos="0 0 0" rgba="1 1 1 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="0.7071 0.7071 0 0" ></geom>\n')
    string1.append(tabs+'<joint type="free" name="l0" pos="0 0 0"/>\n')
    i=-1
    dx=widthx*math.cos(theta[i+1])
    dy=widthx*math.sin(theta[i+1])
    string1.append(tabs+'\t<body name="tml " pos="'+str(dx)+' '+str(0.0)+' '+str(dy)+'" quat="'+str(math.cos((math.pi/2-theta[i+1])/2))+'0.0'+str(math.sin((math.pi/2-theta[i+1])/2))+' 0">\n')
    string1.append(tabs+'\t\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(track_width)+' '+str(widthy)+ ' '+str(0.001)+'" type="box" quat="1 0 0 0" ></geom>\n')
    string1.append(tabs+'\t</body>\n')      
    
    count=0
    string1.append(tabs+'<body name="Bl0'+str(count)+'" pos="'+str(x1-x0)+' '+str(0.0)+' '+str(y1-y0)+'" quat="1.0 0.0 0 0">\n')
    string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 0 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="0.7071 0.7071 0 0" ></geom>\n')
    string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(-(x1-x0)/2)+' '+str(0.0)+' '+str(-(y1-y0)/2)+'" axis="0 1 0"/>\n')
    i=-2
    dx=widthx*math.cos(theta[i+1])
    dy=widthx*math.sin(theta[i+1])
    string1.append(tabs+'\t<body name="tl0'+str(count)+'" pos="'+str(dx)+' '+str(0.0)+' '+str(dy)+'" quat="'+str(math.cos((math.pi/2-theta[i+1])/2))+'0.0'+str(math.sin((math.pi/2-theta[i+1])/2))+' 0">\n')
    string1.append(tabs+'\t\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(track_width)+' '+str(widthy)+ ' '+str(0.001)+'" type="box" quat="1 0 0 0" ></geom>\n')
    string1.append(tabs+'\t</body>\n')    
    string1.append(tabs+'</body>\n')
    count=1
  
    for i in range(len(theta)-3):
        dx=a*math.cos(theta[i+1])-a*math.cos(theta[i])
        dy=b*math.sin(theta[i+1])-b*math.sin(theta[i])
        string1.append(tabs+'<body name="Bl0'+str(count)+'" pos="'+str(dx)+' '+str(0.0)+' '+str(dy)+'" quat="1.0 0.0 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="0.7071 0.7071 0 0" ></geom>\n')
        string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(-dy/2)+'" axis="0 1 0"/>\n')     
        ## Flat treads ##
        # string1.append(tabs+'\t<body name="tl0'+str(count)+'" pos="'+str(0)+' '+str(0.0)+' '+str(widthx)+'" quat="1 0 0 0">\n')
        # string1.append(tabs+'\t<body name="tl0'+str(count)+'" pos="'+str(0)+' '+str(0.0)+' '+str(widthx)+'" quat="'+str(math.cos((theta[i+1]-math.pi/2)/2))+'0.0'+str(math.sin((theta[i+1]-math.pi/2)/2))+' 0">\n')
        dx=widthx*math.cos(theta[i+1])
        dy=widthx*math.sin(theta[i+1])
        string1.append(tabs+'\t<body name="tl0'+str(count)+'" pos="'+str(dx)+' '+str(0.0)+' '+str(dy)+'" quat="'+str(math.cos((math.pi/2-theta[i+1])/2))+'0.0'+str(math.sin((math.pi/2-theta[i+1])/2))+' 0">\n')
        string1.append(tabs+'\t\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(track_width)+' '+str(widthy)+ ' '+str(0.001)+'" type="box" quat="1 0 0 0" ></geom>\n')
        string1.append(tabs+'\t</body>\n')

        tabs=tabs+'\t'
        count=count+1
    i=i+1
 
    dx=a*math.cos(theta[i+1])-a*math.cos(theta[i])
    dy=b*math.sin(theta[i+1])-b*math.sin(theta[i])   
    string1.append(tabs+'<body name="rmf'+'" pos="'+str(dx)+' '+str(0)+' '+str(dy)+'" quat="1 0 0 0">\n')
    string1.append(tabs+'\t<joint type="hinge" name="rl1'+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(-dy/2)+'" axis="0 1 0"/>\n')   
    string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 1 1.0" size="'+str(widthx)+' '+str(widthy)+ ' '+str(widthz)+'" type="cylinder" quat="0.7071 0.7170 0 0"></geom>\n')
    dx=widthx*math.cos(theta[i+1])
    dy=widthx*math.sin(theta[i+1])
    string1.append(tabs+'\t<body name="tl0'+str(count)+'" pos="'+str(dx)+' '+str(0.0)+' '+str(dy)+'" quat="'+str(math.cos((math.pi/2-theta[i+1])/2))+'0.0'+str(math.sin((math.pi/2-theta[i+1])/2))+' 0">\n')
    string1.append(tabs+'\t\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(track_width)+' '+str(widthy)+ ' '+str(0.001)+'" type="box" quat="1 0 0 0" ></geom>\n')
    string1.append(tabs+'\t</body>\n')
    tabs=tabs+'\t'  
    count=count+1   
  
    tot_tab=len(tabs.split("\t"))
    for i in range(tot_tab-2,1,-1):
        tab2='\t'*i
        string1.append(tab2+'</body>\n')
    pa0 = [a*math.cos(theta[-1]),b*math.sin(theta[-1])]
    pa1 = [a*math.cos(theta[-2]),b*math.sin(theta[-2])]
    anchor = [a*(math.cos(theta[-2])-math.cos(theta[-1]))/2,0,b*(math.sin(theta[-2])-math.sin(theta[-1]))/2]
    return string1, anchor 

def build_track_cyl(radius,wheelbase,tabs,wheel_pos,half_width,string_header=[],init_pos=-1):
    tread_height=wheelbase*2/60
    width=half_width
    pi=math.pi
    track_len = (radius+tread_height)*2*pi+wheelbase*4
    slinks=round(wheelbase/tread_height)
    rlinks=round((radius+tread_height)*pi/(2*tread_height))
    if init_pos==-1:
        side="L"
    else:
        side="R"

    string1=[]
    ## Create the first link in chain ##
    string1.append('\t\t<body name="BM'+side+'" pos="'+str(wheel_pos[init_pos,0]+tread_height*4)+' '+str(wheel_pos[init_pos,1])+' '+str(wheel_pos[init_pos,2]+(radius+tread_height))+'" quat="0.7071 0.7071 0 0">\n')
    string1.append(tabs+'<geom mass="0.02" pos="0 0 0" rgba="1 1 1 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
    string1.append(tabs+'<joint type="free" name="'+side+'0" pos="0 0 0"/>\n')
    
    count = 0
    ## Create the second link in chain ##
    string1.append(tabs+'<body name="TM'+side+'" pos="'+str(-tread_height*2)+' '+str(0.0)+' '+str(0)+'" quat="1 0 0 0">\n')
    string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
    string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(tread_height)+' '+str(0.0)+' '+str(0)+'" axis="0 0 1"/>\n')
    string1.append(tabs+'</body>\n') 
    
    count = 1
    ## Create the upper track links ##
    for i in range(slinks-2):
        dx=0
        dy=0
        string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(tread_height*2)+' '+str(0.0)+' '+str(0)+'" quat="1 0 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
        string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(-tread_height)+' '+str(0.0)+' '+str(0)+'" axis="0 0 1"/>\n')
        tabs=tabs+'\t'
        count=count+1

    ## Create the front track links ##
    theta = np.linspace(math.pi/2,-math.pi/2,rlinks)
    for i in range(rlinks-1):
        r=radius+tread_height
        dx=r*(math.cos(theta[i+1])-math.cos(theta[i]))
        dy=r*(math.sin(theta[i+1])-math.sin(theta[i]))
        string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(dx)+' '+str(dy)+' '+str(0)+'" quat="1 0 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
        string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(-dy/2)+'" axis="0 0 1"/>\n')
        tabs=tabs+'\t'
        count=count+1

    ## Create the lower track links ##
    for i in range(slinks):
        dx=0
        dy=0
        string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(-tread_height*2)+' '+str(0.0)+' '+str(0)+'" quat="1 0 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
        string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(tread_height)+' '+str(0.0)+' '+str(0)+'" axis="0 0 1"/>\n')
        tabs=tabs+'\t'
        count=count+1

    ## Create the back track links ##
    theta = np.linspace(3*math.pi/2,math.pi/2,rlinks)
    for i in range(rlinks-2):
        r=radius+tread_height
        dx=r*(math.cos(theta[i+1])-math.cos(theta[i]))
        dy=r*(math.sin(theta[i+1])-math.sin(theta[i]))
        string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(dx)+' '+str(dy)+' '+str(0)+'" quat="1 0 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
        string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(-dy/2)+'" axis="0 0 1"/>\n')
        tabs=tabs+'\t'
        count=count+1
    
    ## Joining link ##
    i=i+1
    dx=r*(math.cos(theta[i+1])-math.cos(theta[i]))
    dy=r*(math.sin(theta[i+1])-math.sin(theta[i]))
    string1.append(tabs+'<body name="B'+side+'F" pos="'+str(dx)+' '+str(dy)+' '+str(0)+'" quat="1 0 0 0">\n')
    string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
    string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(-dy/2)+'" axis="0 0 1"/>\n')
    tabs=tabs+'\t'
    count=count+1    
    string_header.append('\t<contact>\n\t\t<exclude body1="TM'+side+'" body2="B'+side+'F" />\n')
    for i in range(1,count-2):
        string_header.append('\t\t<exclude body1="B'+side+'0'+str(i)+'" body2="B'+side+'0'+str(i+1)+'"/>\n')
    string_header.append('\t</contact>\n')

    ## Close off all the bodies ##       
    tot_tab=len(tabs.split("\t"))
    
    for i in range(tot_tab-2,1,-1):

        tab2='\t'*i
        string1.append(tab2+'</body>\n')

    
  
    
    return string1, [-tread_height,0,0], string_header

def build_track_veh(radius,wheelbase,payloadx,payloadz,payload_weight):

    half_width = 0.05        # meters
    tread_height = 0.03175/2    # meters
    tread_width = 0.0508/2      # meters
    names = ['rf_','lf_','rb_','lb_']

    mass = 2
    wheel_pos = np.array([[wheelbase,-0.4,-0.19],[wheelbase,0.4,-0.19],[-wheelbase,-0.4,-0.19],[-wheelbase,0.4,-0.19]])

    tabs="\t\t\t"

    ## Setup the initial mujoco lines ##
    string1=[]
    string1.append('<mujoco model=\"env\">\n')
    string1.append('\t<size njmax=\"8000\" nconmax=\"4000\"/>\n\t<option timestep=\"0.0025\" />\n')


    string2,anchor,string_header=build_track_cyl(radius,wheelbase,tabs,wheel_pos,half_width,string_header=[],init_pos=-2)
    string1.append('\t<equality>\n\t\t<connect body1="TMR" body2="BRF" anchor="'+str(anchor[0])+' '+str(anchor[1])+' '+str(anchor[2])+'" solref="0.01 1" solimp="0.99 0.99 0.001 0.5 2" />\n\t</equality>\n')      
    string1.append(string_header)


        
    string1.append('\t<actuator>\n')
    
    ## Specify the motor names and numbers ##
    for i in range(4):
        string1.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+str(i)+'\" name=\"motor'+str(i)+'\"/>\n')

    ## Finish setting up Mujoco inputs ##-0.15
    string1.append('\t</actuator>\n\n\t<worldbody>\n\t\t<body name=\"frame\" pos=\"0.0 0 0.0\" quat=\"1.0 0.0 0 0\">\n')
    string1.append(tabs+'<geom mass=\"0.005\" pos=\"0 0 0\" rgba=\"1 0 0 1.0\" size=\"0.5 0.3 0.1651\" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"'+str(payload_weight)+'\" rgba=\"0 1 1 1\" size=\"0.025\" type=\"sphere\"/>\n\t\t\t</body>\n')
    string1.append(tabs+'<site name="winch" pos="0.5 0 0.0" size="0.1 0.1 0.1" rgba="0 1 0 0" type="sphere"/>\n')
    # string1.append(tabs+'<camera euler=\"0 0 0\" fovy=\"40\" name=\"rgb\" pos=\"0 0 2.5\"></camera>\n')

    radius_in=radius
    ## Create the wheel ##
    for i,name in enumerate(names):

        string1.append(tabs+"<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i,0])+" "+str(wheel_pos[i,1])+" "+str(wheel_pos[i,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n")
        string1.append(tabs+"\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 1.0\" size=\""+str(radius) +" " + str(half_width)+"\" type=\"cylinder\"/>\n")
        string1.append(tabs+"\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+"\" type=\"hinge\"/>\n")
        string1.append(tabs+"\t<site name=\"wheel"+str(i)+"_t\" pos=\"0 0 0.0\" size='0.00005 0.00005 0.00005' rgba='0 1 0 1' type='sphere'/>\n")
        string1.append(tabs+"</body>\n")
    string1.append("\t\t</body>\n")
    string1.append(string2)

    return string1

def build_track_fixed(radius,wheelbase,payloadx,payloadz,payload_weight):
    half_width = 0.05        # meters
    tread_height = 0.03175/2    # meters
    tread_width = 0.0508/2      # meters
    names = ['rf_','lf_','rb_','lb_']

    mass = 2
    wheel_pos = np.array([[wheelbase,-0.4,-0.19],[wheelbase,0.4,-0.19],[-wheelbase,-0.4,-0.19],[-wheelbase,0.4,-0.19]])

    tabs="\t\t\t"

    ## Setup the initial mujoco lines ##
    string1=[]
    string1.append('<mujoco model=\"env\">\n')
    string1.append('\t<size njmax=\"8000\" nconmax=\"4000\"/>\n\t<option timestep=\"0.0025\" />\n')
    
    string_acts=[]
    string_acts.append('\t<actuator>\n')
    string2, string_acts = build_track_cyl_fixed(radius,wheelbase,tabs,wheel_pos,half_width,string_acts,init_pos=0)
    string3, string_acts = build_track_cyl_fixed(radius,wheelbase,tabs,wheel_pos,half_width,string_acts,init_pos=1)

    string_acts.append('\t</actuator>\n\n')
    string1.append(string_acts)

    ## Finish setting up Mujoco inputs ##-0.15
    string1.append('\t<worldbody>\n\t\t<body name=\"frame\" pos=\"0.0 0 0.0\" quat=\"1.0 0.0 0 0\">\n')
    string1.append(tabs+'<geom mass=\"0.005\" pos=\"0 0 0\" rgba=\"1 0 0 1.0\" size=\"0.5 0.3 0.1651\" type=\"box\"></geom>\n\t\t\t<joint type=\'free\' name=\'frame:base\' pos=\'0 0 0\'/>\n')
    string1.append(tabs+'<body name=\"mass0\" pos=\"'+str(payloadx)+' 0.0000 '+ str(payloadz)+'\" >\n\t\t\t\t<geom mass=\"'+str(payload_weight)+'\" rgba=\"0 1 1 1\" size=\"0.025\" type=\"sphere\"/>\n\t\t\t</body>\n')
    string1.append(tabs+'<site name="winch" pos="0.5 0 0.0" size="0.1 0.1 0.1" rgba="0 1 0 0" type="sphere"/>\n')
    string1.append(string2)
    string1.append(string3)
    string1.append('\t\t</body>\n\n')
    return string1

def build_track_cyl_fixed(radius,wheelbase,tabs,wheel_pos,half_width,string_acts=[],init_pos=0):
    tread_height=wheelbase*2/64
    width=half_width
    pi=math.pi
    track_len = (radius+tread_height)*2*pi+wheelbase*4
    slinks=round(wheelbase/tread_height)
    rlinks=round((radius+tread_height)*pi/(2*tread_height))
    if init_pos==0:
        side="L"
    else:
        side="R"

    string1=[]
    count=0
    theta = np.linspace(math.pi/2,-math.pi/2,rlinks)
    for i in range(rlinks):
        r=radius+tread_height
        dx=(wheel_pos[init_pos,0])+r*(math.cos(theta[i]))
        dy=wheel_pos[init_pos,2]+r*(math.sin(theta[i]))
        string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(dx)+' '+str(wheel_pos[init_pos,1])+' '+str(dy)+'" quat="0.7071 0.7071 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.1" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
        string1.append(tabs+'\t<joint axis=\"0 0 1\" name=\"wheel'+side+str(count)+'" type="hinge"/>\n')
        string1.append(tabs+'</body>\n')
        string_acts.append('\t\t<motor gear="1.0" joint="wheel'+side+str(count)+'" name="motor'+side+str(count)+'"/>\n')
        # string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(-dy/2)+'" axis="0 0 1"/>\n')
        # tabs=tabs+'\t'
        count=count+1
    xpos=(wheel_pos[init_pos,0])

    ## Create the lower track links ##
    for i in range(slinks):
        r=radius+tread_height
        xpos=xpos-2.5*tread_height
        zpos=wheel_pos[init_pos,2]+r*(math.sin(theta[-1]))
        string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(xpos)+' '+str(wheel_pos[init_pos,1])+' '+str(zpos)+'" quat="0.7071 0.7071 0 0">\n')
        string1.append(tabs+'\t<geom mass="0.1" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
        string1.append(tabs+'\t<joint axis=\"0 0 1\" name=\"wheel'+side+str(count)+'" type="hinge"/>\n')
        string1.append(tabs+'</body>\n')
        string_acts.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+side+str(count)+'\" name=\"motor'+side+str(count)+'\"/>\n')
        # tabs=tabs+'\t'
        count=count+1 

    # count = 0
    # string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(wheel_pos[init_pos,0])+' '+str(wheel_pos[init_pos,1])+' '+str(wheel_pos[init_pos,2])+'" quat="0.7071 0.7071 0 0">\n')
    # string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
    # string1.append(tabs+'\t<joint axis=\"0 0 1\" name=\"wheel'+side+str(count)+'" type="hinge"/>\n')
    # string1.append(tabs+'</body>\n')
    # string_acts.append('\t\t<motor gear="1.0" joint="wheel'+side+str(count)+'" name="motor'+side+str(count)+'"/>\n')    
    # count = 1


    ## Create the front track links ##
    # theta = np.linspace(math.pi/2,-math.pi/2,rlinks)
    # for i in range(rlinks-1):
    #     r=radius+tread_height
    #     dx=(wheel_pos[init_pos,0])+r*(math.cos(theta[i+1])-math.cos(theta[i]))
    #     dy=wheel_pos[init_pos,2]+r*(math.sin(theta[i+1])-math.sin(theta[i]))
    #     string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(dx)+' '+str(wheel_pos[init_pos,1])+' '+str(dy)+'" quat="0.7071 0.7071 0 0">\n')
    #     string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
    #     string1.append(tabs+'\t<joint axis=\"0 0 1\" name=\"wheel'+side+str(count)+'" type="hinge"/>\n')
    #     string1.append(tabs+'</body>\n')
    #     string_acts.append('\t\t<motor gear="1.0" joint="wheel'+side+str(count)+'" name="motor'+side+str(count)+'"/>\n')
    #     # string1.append(tabs+'\t<joint type="hinge" name="J'+side+str(count)+'" pos="'+str(-dx/2)+' '+str(0.0)+' '+str(-dy/2)+'" axis="0 0 1"/>\n')
    #     # tabs=tabs+'\t'
    #     count=count+1

    # ## Create the lower track links ##
    # for i in range(slinks):
    #     dx=0
    #     dy=0
    #     string1.append(tabs+'<body name="B'+side+'0'+str(count)+'" pos="'+str(-tread_height*2)+' '+str(0.0)+' '+str(0)+'" quat="1 0 0 0">\n')
    #     string1.append(tabs+'\t<geom mass="0.02" pos="0 0 0" rgba="1 1 0 1.0" size="'+str(tread_height)+' '+str(width)+ '" type="cylinder" quat="1 0 0 0" ></geom>\n')
    #     string1.append(tabs+'\t<joint axis=\"0 0 1\" name=\"wheel'+side+str(count)+'" type="hinge"/>\n')
    #     string_acts.append('\t\t<motor gear=\"1.0\" joint=\"wheel'+side+str(count)+'\" name=\"motor'+side+str(count)+'\"/>\n')
    #     # tabs=tabs+'\t'
    #     count=count+1   

    # ## Close off all the bodies ##       
    # tot_tab=len(tabs.split("\t"))
    
    # for i in range(tot_tab-2,1,-1):

    #     tab2='\t'*i
    #     string1.append(tab2+'</body>\n')

    
  
    
    return string1, string_acts