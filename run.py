###########
# IMPORTS #
###########

import multiprocessing
import os
import sys
import platform
import _thread
from subprocess import Popen
import numpy as np

#############
# FUNCTIONS #
#############

def spawn_files():
    file = open("data/total.csv", "w+")
    file.write(",".join(["scale", "throughput", "load", "collision", "lost"]))
    file.write("\n")
    file.close()
    file = open("data/nodes.csv", "w+")
    file.write(",".join(["node", "scale", "throughput", "load", "collision", "lost"]))
    file.write("\n")
    file.close()


def simulate(minVal, maxVal, step):
    for val in np.arange(minVal, maxVal, step):
        scale = val/100000
        print("[ STEP ] {:.8g}".format(scale))
        for seed in range(100):
            if platform.system() == 'Windows':
                os.system("python ./iris/iris.py -q -s 1000 -f data -r {} {}".format(seed, scale))
            else:
                os.system(".virtual_env/bin/python ./iris/iris.py -q -s 1000 -f data -r {} {}".format(seed, scale))

########
# MAIN #
########

try:
    req_version = (3, 0)
    cur_version = sys.version_info

    if cur_version >= req_version:
        spawn_files()
        # sweet spot is at 0.0031 from 0.00095 to 0.9 values will be divided by 100000  
        simulate(95, 300, 5)  # from 0.00095 to 0.003
        simulate(300, 500, 40)  # from 0.003 to 0.005
        simulate(500, 1000, 100)  # from 0.005 to 0.01
        simulate(1000, 2000, 400)  # from 0.01 to 0.02
        simulate(2000, 10000, 800) # from 0.02 to 0.1
    else:
        print("Please, use Python 3.x")
except Exception as e:
    print("Wrong Python version, please use the 3.x")
    raise e
