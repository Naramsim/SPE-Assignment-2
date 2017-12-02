###########
# IMPORTS #
###########

import numpy.random as distributions

import settings
import log

#########
# CLASS #
#########

class Packet:
    count = 0

    def __init__(self, sender, time):
        self.id = Packet.count
        self.sender = sender
        self.time = time
        self.size = self.set_size(int(distributions.binomial(settings.BINOMIAL_N, settings.BINOMIAL_P)))
        self.transfer_time = self.size/settings.SPEED
        self.is_queued = False
        self.is_lost = False

        Packet.count += 1

    def __lt__(self, other):
        if self.time != other.time:
            return self.time < other.time
        else:
            # if the time is the same, discriminate
            # using the incremental nature of the id
            return self.id < other.id
            
    def __str__(self):
        lines = ["",
                 log.format_color("- PACKET {} -".format(self.id), "cyan"),
                 "sender        = {}".format(self.sender),
                 " ".join(["schedule time =", settings.PRECISION, "s(abs)"]).format(self.time),
                 " ".join(["transfer time =", settings.PRECISION, "s(rel)"]).format(self.transfer_time),
                 "size          = {} byte".format(self.size),
                 "status        = {}".format("QUEUED" if self.is_queued else "PENDING")]
        return "\n".join(lines)

    def set_size(self, size):
        if size < settings.PACKET_SIZE_MIN:
            size = settings.PACKET_SIZE_MIN
        elif size > settings.PACKET_SIZE_MAX:
            size = settings.PACKET_SIZE_MAX
        return size
