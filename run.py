###########
# IMPORTS #
###########

import multiprocessing
import os
import sys
import _thread

#############
# FUNCTIONS #
#############

def spawn_files():
    file = open("data\\total.csv", "w+")
    file.write(",".join(["scale", "throughput", "load", "collision", "lost"]))
    file.write("\n")
    file.close()
    file = open("data\\nodes.csv", "w+")
    file.write(",".join(["node", "scale", "throughput", "load", "collision", "lost"]))
    file.write("\n")
    file.close()

def simulate(minVal, maxVal, step):
    for val in range(minVal, maxVal, step):
        scale = val/10000
        for seed in range(1):
        #for seed in range(100):
            os.system("python iris\\iris.py -q -s 1000 -f data -r "+str(seed)+" "+str(scale))
            #os.system(".virtual_env\\Scripts\\python iris\\iris.py -q -s 1000 -f data -r "+str(seed)+" "+str(scale))
    print("[ STEP ]")

########
# MAIN #
########

try:
    req_version = (3,0)
    cur_version = sys.version_info

    if cur_version >= req_version:
        spawn_files()
        simulate(30, 69, 3)
        simulate(76, 132, 7)
        simulate(140, 440, 30)
        simulate(500, 1000, 100)
    else:
        print ("Please, use Python 3.x")
except Exception as e:
    print ("Wrong Python version, please use the 3.x")
    raise e

