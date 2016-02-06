###########
# IMPORTS #
###########

import random as distributions

# import numpy.random as distributions

import settings
import log
from scheduler import Scheduler
from node import Node

#######
# NET #
#######

nodes = []

########
# MAIN #
########

# init
#

distributions.seed(settings.SEED)

for point in settings.POINTS:
    nodes.append(Node(point[0], point[1]))

for node in nodes:
    node.find_neigbhours(nodes)
    node.generate_next_packet()

# simulation
#

for i in range(0, settings.STEPS+1):
    print(log.before_step(Scheduler))
    Scheduler.step()
    print(log.after_step(Scheduler))
