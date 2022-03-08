import numpy as np

def get_gauss_rand(in_mean,in_std=0,l_lim=-1000000,u_lim=1000000):
    outp = l_lim-1
    while outp<l_lim or outp>u_lim:
        outp = np.random.normal(in_mean,in_std)
    return outp