#         #
# IMPORTS #
#         #

import random

import numpy.random as distribution

import settings
import output

#       #
# CLASS #
#       #

class Packet:
    count = 0

    def __init__(self, sender, arrival_time):
        self.id = Packet.count
        self.sender = sender
        self.arrival_time = arrival_time
        #self.size = int(distribution.uniform(settings.UNIFORM_MIN, settings.UNIFORM_MAX+1))
        self.size = int(random.uniform(settings.UNIFORM_MIN, settings.UNIFORM_MAX+1))
        self.transfer_time = self.size/settings.SPEED
        self.queued = False
        Packet.count += 1

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __str__(self):
        lines = ["",
                 output.title("- PACKET {} -".format(self.id), "cyan"),
                 "sender        = {}".format(self.sender),
                 "arrival time  = {} s (abs)".format(self.arrival_time),
                 "size          = {} byte".format(self.size),
                 "transfer time = {} s (rel)".format(self.transfer_time),
                 "status        = {}".format("QUEUED" if self.queued else "PENDING")]
        return "\n".join(lines)
