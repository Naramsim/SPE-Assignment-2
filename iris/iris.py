###########
# IMPORTS #
###########

import numpy.random as distributions

import arguments
import settings
from scheduler import Scheduler
from settings import NODES
from node import Node

########
# MAIN #
########

arguments.save(arguments.parse())

# init
#

distributions.seed(settings.SEED)

for point in settings.POINTS:
    NODES.append(Node(point[0], point[1]))

for node in NODES:
    node.find_neighbours(NODES)
    node.generate_next_packet()

# simulation
#

if settings.TIME:
    while Scheduler.time < settings.TIME:
        Scheduler.step()
elif settings.STEPS:
    for i in range(0, settings.STEPS+1):
        Scheduler.step()

Scheduler.handle_results()
