import numpy as np

def get_site_state(sim,site_id):
    '''
    INPUT:
    Takes in a MjSim object and a site id, outputs
    rot mat, pos, ang vel, lin vel in cartesian space
    OUTPUT:
    (R, p, w, v) in cartesian space
    '''
    pos     = np.array(sim.data.site_xpos[site_id])
    ori_mat = np.array(sim.data.site_xmat[site_id]).reshape((3,3))
    pos_vel = np.array(sim.data.site_xvelp[site_id])
    ori_vel = np.array(sim.data.site_xvelr[site_id])
    return (ori_mat, pos, ori_vel, pos_vel)    

def get_body_state(sim, body_id):
    '''
    INPUT:
    Takes in a MjSim object and a site id, outputs
    rot mat, pos, ang vel, lin vel in cartesian space
    OUTPUT:
    (R, p, w, v) in cartesian space
    '''
    pos     = np.array(sim.data.body_xpos[body_id])
    ori_mat = np.array(sim.data.body_xmat[body_id]).reshape((3,3))
    pos_vel = np.array(sim.data.body_xvelp[body_id])
    ori_vel = np.array(sim.data.body_xvelr[body_id])
    return (ori_mat, pos, ori_vel, pos_vel) 