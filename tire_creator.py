import numpy as np
import math

# radius = 0.2286         # meters
# half_width = 0.0125     # meters
# tread_height = 0.009    # meters
# tread_width = 0.00525   # meters
radius = 0.24765          # meters
half_width = 0.0125       # meters
tread_height = 0.03175    # meters
tread_width = 0.0508      # meters
names = ['lf_','rf_','lb_','rb_']
wheel_pos = np.array([[0.5,-0.4,-0.1],[0.5,0.4,-0.1],[-0.5,-0.4,-0.1],[-0.5,0.4,-0.1]])
mass = 1
num_treads=16
theta = np.linspace(0,(360-360/num_treads)*math.pi/180,num_treads)
tabs="\t\t\t"
string1 = ""
## Create the wheel ##
for i,name in enumerate(names):
    string1 = string1+tabs+"<body name=\""+name+"wheel\" pos=\""+str(wheel_pos[i,0])+" "+str(wheel_pos[i,1])+" "+str(wheel_pos[i,2])+"\" quat=\"0.7071067811865476 0.7071067811865476 0 0\"> \n"
    string1 = string1+tabs+"\t<geom mass=\""+str(mass)+"\" rgba=\"0 0 1 1\" size=\""+str(radius) +" " + str(half_width)+"\" type=\"cylinder\"/>\n"
    string1 = string1+tabs+"\t<joint axis=\"0 0 1\" name=\"wheel"+str(i)+"\" type=\"hinge\"/>\n"
    string1=string1+tabs+"\t<site name=\"wheel"+str(i)+"_t\" pos=\"0 0 0.0\" size='0.00005 0.00005 0.00005' rgba='0 1 0 1' type='sphere'/>\n"
    for j,ang in enumerate(theta):
        quat = ["{:.6f}".format(math.cos(ang/2)),"0.0","0.0","{:.6f}".format(math.sin(ang/2))]

        string1 = string1+tabs+"\t<body name=\""+name+"tread"+str(j)+"\" pos=\""+"{:.4f}".format(radius*math.cos(ang))+ " " + "{:.4f}".format(radius*math.sin(ang)) +" 0.0\" quat=\"" +quat[0]+" "+quat[1]+" "+quat[2]+" "+quat[3]+"\">\n"
        string1 = string1+tabs+"\t\t<geom mass=\"0.001\" rgba=\"0 0 1 1\" size=\""+"{:.3f}".format(tread_height) +" "+ "{:.3f}".format(tread_width) + " " + "{:.4f}".format(half_width) +"\" type=\"box\"/>\n"
        string1 = string1+tabs+"\t</body>\n"
    string1=string1+tabs+"</body>\n"
    # print(string1)

text_file=open("wheel.txt","w")
text_file.write(string1)
text_file.close()