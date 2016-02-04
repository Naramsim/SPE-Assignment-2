#         #
# IMPORTS #
#         #

import random

from heapq import heappop as heap_pop

import settings
import output
from scheduler import Scheduler
from node import Node
from packet import Packet

#      #
# MAIN #
#      #

# init

random.seed(1)

for node in settings.NODES:
    node.find_neigbhours(settings.NODES)

for node in settings.NODES:
    node.generate_next_packet()

# test

for node in settings.NODES:
    print(node)

print(Scheduler())

for i in range(0, 1000):
    print(Scheduler.events[0])
    Scheduler.step()
    print(Scheduler())
