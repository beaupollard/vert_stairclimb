import numpy as np
import mj_utils

class control():
    def __init__(self,sim,vel_des):
        self.wypt_name = 'wypt0'
        self.frame_name = 'frame'
        self.vel_des=vel_des
        self.sim = sim
        self.xg0 = 0.0
        self.integ = np.zeros((1,len(self.sim.model._actuator_id2name)))
        self.integ_tot = np.zeros((1,len(self.sim.model._actuator_id2name)))
        

    def pos_error(self):
        xd=mj_utils.get_site_state(self.sim, self.sim.model.site_name2id(self.wypt_name))
        xc=mj_utils.get_body_state(self.sim, self.sim.model.body_name2id(self.frame_name))
        return xd[1]-xc[1]

    def vel_error(self):
        xc=mj_utils.get_body_state(self.sim, self.sim.model.body_name2id(self.frame_name))
        return np.linalg.norm(xc[3])

    def torque(self,input_t):
        xg = self.pos_error()
        vg = self.vel_des-self.vel_error()
        
        dxg=(xg-self.xg0)/self.sim.model.opt.timestep
        control_input=10.0*(3.0*(xg[0])+ 0.1*vg + 0.003*self.xg0 )

        print("position error: " + "{:.2f}".format(xg[0])+" velocity error: " + "{:.2f}".format(vg)+" Control input: " + "{:.2f}".format(control_input))
        
        for i in range(len(self.sim.model._actuator_id2name)):
            if self.sim.model._actuator_id2name[i][-1]=='0':
                self.sim.data.ctrl[i] = -input_t
            else:
                self.sim.data.ctrl[i] = -input_t#-input_t

    def velo(self,input_v,lim):

        kp=0.5
        ki=0.000001
        for i in range(len(self.sim.model._actuator_id2name)):
            if self.sim.model._actuator_id2name[i][-1]=='0':
                feedback=(20*kp*(self.sim.data.qvel[i+6]-input_v)+10000.*ki*self.integ[0][i])
                self.integ[0][i]=feedback
                
            else:
                feedback=(kp*(self.sim.data.qvel[i+6]-input_v)+ki*self.integ[0][i])
                self.integ[0][i]=feedback
            if abs(feedback)<lim:
                self.sim.data.ctrl[i] = -feedback
            else:
                self.sim.data.ctrl[i] = -lim
        self.integ_tot=np.append(self.integ_tot,self.integ,axis=0)

    def velowheel(self,input_v,lim):

        kp=10.#0.65*lim/input_v#10.
        ki=0.5
        for i in range(len(self.sim.model._actuator_id2name)):
            if i>=2:
                feedback=(11.*(self.sim.data.qvel[i+6]-input_v)+ki*self.integ[0][i])
            else:
                feedback=(kp*(self.sim.data.qvel[i+6]-input_v)+ki*self.integ[0][i])
            self.integ[0][i]=feedback
            if abs(feedback)<lim:
                self.sim.data.ctrl[i] = -feedback
            else:
                self.sim.data.ctrl[i] = -lim
        self.integ_tot=np.append(self.integ_tot,self.integ,axis=0)


