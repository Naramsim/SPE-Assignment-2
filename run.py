###########
# IMPORTS #
###########

import multiprocessing
import os
import _thread

#############
# FUNCTIONS #
#############

def spawn_files():
    file = open("data\\total.csv", "w+")
    file.write(",".join(["scale", "throughput", "load"]))
    file.write("\n")
    file.close()
    file = open("data\\nodes.csv", "w+")
    file.write(",".join(["node", "scale", "throughput", "collision", "lost"]))
    file.write("\n")
    file.close()

def simulate(exp_min, exp_max):
    for exp in range(exp_min, exp_max, 1):
        scale = 2**(exp/10)
        for seed in range(200):
            os.system("python iris\\iris.py -q -s 1000 -f data -r "+str(seed)+" "+str(scale))

########
# MAIN #
########

spawn_files()
simulate(-75, 35)
