#         #
# IMPORTS #
#         #

from node import Node

#           #
# CONSTANTS #
#           #

# distributions
UNIFORM_MIN = 32
UNIFORM_MAX = 6914
GAMMA_SHAPE = 1.314
GAMMA_SCALE = 1

# nodes
NODES = [Node(0.359, 0.799),
         Node(0.261, 0.485),
         Node(0.642, 0.499),
         Node(0.451, 0.666),
         Node(0.626, 0.469),
         Node(0.473, 0.541),
         Node(0.872, 0.529),
         Node(0.887, 0.412),
         Node(0.788, 0.502),
         Node(0.362, 0.702)]
BOUNDS = 0.25
BUFFER = 50
SPEED = 1*10000
