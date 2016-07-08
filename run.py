###########
# IMPORTS #
###########

import multiprocessing
import os
import _thread

#############
# FUNCTIONS #
#############

def simulate(exp_min, exp_max):
    for exp in range(exp_min, exp_max, 1):
        scale = 2**(exp/10)
        for seed in range(200):
            os.system("python iris.py -q -s 1000 -f data\\results.csv -r "+str(seed)+" "+str(scale))

########
# MAIN #
########

simulate(-75, 35)
