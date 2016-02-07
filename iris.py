###########
# IMPORTS #
###########

import random as distributions

# import numpy.random as distributions

import arguments
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

arguments.save(arguments.parse())

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

if settings.TIME:
    while Scheduler.time < settings.TIME:
        Scheduler.step()
elif settings.STEPS:
    for i in range(0, settings.STEPS+1):
        Scheduler.step()
