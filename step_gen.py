import numpy as np
import math

def gen_steps(num_steps,rise,slope):

    dy=rise/2
    dx=(dy/math.tan(slope*math.pi/180))
    pos = [1.0,0.0,dy]

    string1=[]

    string1.append('\t\t<body name="floor" pos="0 0 0.0">\n')
    string1.append('\t\t\t<geom condim="6" size="20.0 20.0 0.02" rgba="0 1 0 1" type="box"/>\n')

    for i in range(int(num_steps)-1):
        string1.append('\t\t\t<body name="step'+str(i)+'" pos="'+str(pos[0])+' '+str(pos[1])+' '+str(pos[2])+'+">\n')
        string1.append('\t\t\t\t<geom condim="3" size="'+str(dx)+' '+str(1.61)+' '+str(dy+dy*i)+'" rgba="1 1 1 1" type="box"/>\n')
        string1.append('\t\t\t</body>\n')
        pos[0]=pos[0]+dx*2
        pos[2]=pos[2]+dy
    
    string1.append('\t\t\t<body name="landing" pos="'+str(pos[0]+2.0)+' '+str(pos[1])+' '+str(pos[2])+'+">\n')
    string1.append('\t\t\t\t<geom condim="3" size="'+str(2.+dx)+' '+str(1.61)+' '+str(dy+dy*(i+1))+'" rgba="1 1 1 1" type="box"/>\n')
    string1.append('\t\t\t\t<site name="wypt0" pos="0 0 '+str(pos[2])+'" size="0.15 0.15 0.15" rgba="1 1 0 1" type="sphere"/>\n')
    string1.append('\t\t\t</body>\n')

    string1.append('\t\t</body>\n')
    string1.append('\t</worldbody>\n')
    string1.append('</mujoco>')

    return string1