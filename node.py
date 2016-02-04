#         #
# IMPORTS #
#         #

import math
import random
from heapq import heappush as heap_push

import numpy.random as distribution

import settings
import output
from scheduler import Scheduler
from packet import Packet

#       #
# CLASS #
#       #

class Node:
    count = 0

    def __init__(self, x, y):
        self.id = Node.count
        self.x = x
        self.y = y
        self.neighbours = []
        self.queue = []
        self.sending_until = 0
        self.receiving_until = 0
        self.packets_sent = 0
        self.packets_received = 0
        self.packets_collided = 0

        Node.count += 1

    def find_neigbhours(self, nodes):
        for node in nodes:
            distance = math.hypot(self.x-node.x, self.y-node.y)
            if distance <= settings.BOUNDS and distance != 0:
                self.neighbours.append(node)

    def generate_next_packet(self):
        #time_arrival = distribution.gamma(settings.GAMMA_SHAPE, settings.GAMMA_SCALE)
        time_arrival = random.uniform(0, 3)
        packet = Packet(self.id, Scheduler.time+time_arrival)
        self.queue.append(packet)
        heap_push(Scheduler.events, packet)

    def prepare_packet(self, packet):
        if self.is_idle():
            self.send_packet(packet)
        else:
            self.queue_packet(packet)

    def send_packet(self, packet):
        self.sending_until = Scheduler.time+packet.transfer_time
        for neighbour in self.neighbours:
            self.packets_sent += 1

            if neighbour.is_idle():
                neighbour.packets_received += 1
            elif neighbour.is_receiving():
                neighbour.packets_received -= 1
                neighbour.packets_collided += 1
            elif neighbour.is_sending():
                output.error("Two neighbours both sending.")
                neighbour.packets_received -= 1
                neighbour.packets_collided += 2    # lose both the packet being received and the one it's sending

            if self.sending_until > neighbour.receiving_until:    # if receiving time is more that the previous one
                neighbour.receiving_until = self.sending_until

    def queue_packet(self, packet):
        packet.queued = True
        packet.time = self.sending_until
        self.queue.append(packet)

    def is_sending(self):
        return self.sending_until-Scheduler.time > 0

    def is_receiving(self):
        return self.receiving_until-Scheduler.time > 0

    def is_idle(self):
        return not self.is_sending() and not self.is_receiving()

    def __str__(self):
        packets = []
        for packet in self.queue:
            packets.append(packet.id)
        destinations = []
        for neighbour in self.neighbours:
            destinations.append(neighbour.id)
        lines = ["",
                 output.title("- NODE {} -".format(self.id), "magenta"),
                 "x          = {}".format(self.x),
                 "y          = {}".format(self.y),
                 "neighbours = {}".format(destinations),
                 "queue      = {}".format(packets),
                 "sending    = {} s (abs)".format(self.sending_until),
                 "receiving  = {} s (abs)".format(self.receiving_until),
                 "sent       = {}".format(self.packets_sent),
                 "received   = {}".format(self.packets_received),
                 "collisions = {}".format(self.packets_collided)]
        return "\n".join(lines)
