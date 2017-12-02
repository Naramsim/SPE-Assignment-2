###########
# IMPORTS #
###########

import math
from heapq import heappush as heap_push

import numpy.random as distributions

import settings
import log
from scheduler import Scheduler
from packet import Packet

#########
# CLASS #
#########

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
        self.packets_generated = 0
        self.packets_lost = 0
        self.packets_sent = 0
        self.packets_received = 0
        self.packets_collided = 0
        self.last_packet_size = 0
        self.data_sent = 0
        self.has_collided = False

        Node.count += 1

    def __str__(self):
        queued = []
        for packet in self.queue:
            queued.append(packet.id)

        destinations = []
        for neighbour in self.neighbours:
            destinations.append(neighbour.id)

        lines = ["",
                 log.title("- NODE {} -".format(self.id), "magenta"),
                 "x          = {}".format(self.x),
                 "y          = {}".format(self.y),
                 "neighbours = {}".format(destinations),
                 "queue      = {}".format(queued),
                 " ".join(["sending    =", settings.PRECISION, "s(abs)"]).format(self.sending_until),
                 " ".join(["receiving  =", settings.PRECISION, "s(abs)"]).format(self.receiving_until),
                 "lost       = {}".format(self.packets_lost),
                 "sent       = {}".format(self.packets_sent),
                 "received   = {}".format(self.packets_received),
                 "collided   = {}".format(self.packets_collided)]

        return "\n".join(lines)

    def find_neighbours(self, nodes):
        for node in nodes:
            distance = math.hypot(self.x-node.x, self.y-node.y)
            if distance <= settings.BOUNDS and self.id != node.id:
                self.neighbours.append(node)

    def generate_next_packet(self):
        time_delta = distributions.exponential(scale=settings.EXPONENTIAL_SCALE) # in numpy the rate is equal to 1/scale
        packet = Packet(self.id, Scheduler.time+time_delta)
        self.packets_generated += 1

        if len(self.queue)-1 < settings.BUFFER:
            # since the queue adds each packet as it
            # is *decided* when it is generated and 
            # not as it *is* generated, one element 
            # the queue is not counted

            # logging                                                                               
            log.success(" ".join([str(self.id), "generated packet", str(packet.id)]))               
            # logging

            self.queue.append(packet)
            heap_push(Scheduler.events, packet)
        else:
            # logging
            log.error(" ".join([str(self.id), "lost packet", str(packet.id), "(queue full)"]))
            # logging
            self.packets_lost += 1
            packet.is_lost = True
            heap_push(Scheduler.events, packet)
            # the packet is pushed into the event's queue because it still has to generatea new packet,
            # from the point in time where it *would* have been handled                                                    
                                                                                                    
    def handle_packet(self, packet):                                                                
        if self.is_idle():                                                                          
            # logging
            log.success(" ".join([str(self.id), "sent packet", str(packet.id)]))
            # logging
            self._send_packet(packet)
        elif self.is_sending() and packet.time == Scheduler.time_previous:
            # the node had multiple packets scheduled at the same time, 
            # so if it is already sending, it queues the next one(s)

            # logging                                                                               
            log.success(" ".join([str(self.id), "queued packet", str(packet.id)]))                  
            # logging
            self._queue_packet(packet)
        elif self.is_receiving() and packet.time == Scheduler.time_previous:
            # two (or more) queued packets are sent at the same time by neighbouring nodes 

            # logging                                                                               
            log.warning(" ".join([str(self.id), "sent packet", str(packet.id), "(expect a collision)"]))
            # logging
            self._send_packet(packet)
        else:
            # logging
            log.success(" ".join([str(self.id), "queued packet", str(packet.id)]))
            # logging
            self._queue_packet(packet)

    def is_sending(self):
        return self.sending_until > Scheduler.time

    def is_receiving(self):
        return self.receiving_until > Scheduler.time

    def is_idle(self):
        return not self.is_sending() and not self.is_receiving()

    def _send_packet(self, packet):
        self.queue.pop(0)
        self.sending_until = Scheduler.time+packet.transfer_time

        for neighbour in self.neighbours:
            self.packets_sent += 1
            self.last_packet_size = packet.size/len(self.neighbours) # If a packet weights 3kB, and we have 3 neighbors, we send 1kB to each one 

            if neighbour.is_idle():
                neighbour.has_collided = False
                neighbour.packets_received += 1
                self.data_sent += self.last_packet_size
            elif neighbour.is_receiving():
                # logging
                log.error(" ".join([str(neighbour.id), "was receiving"]))
                # logging

                
                if not neighbour.has_collided:  
                    # when the first collision is detected on a neighbour, 
                    # that neighbour loses both the packet it was receiving,
                    # and the packet that has just been sent;                                                    
                    neighbour.packets_received -= 1                                                 
                    neighbour.packets_collided += 2                                                 
                    neighbour.has_collided = True                                                   
                else:
                    # if a collision was already detected,
                    # the neighbour only loses the just sent packet (the others were already lost)                                                                               
                    neighbour.packets_collided += 1                                                 
            elif neighbour.is_sending():                                                            
                # logging
                log.error(" ".join([str(self.id), "and", str(neighbour.id), "both sending"]))
                # logging
                if not neighbour.has_collided:
                    if neighbour.data_sent > 0:
                        neighbour.data_sent -= neighbour.last_packet_size/len(neighbour.neighbours)
                    neighbour.packets_collided += 1
                    self.packets_collided += 1
                    neighbour.has_collided = True
                else:
                    neighbour.packets_collided += 1

            if self.sending_until > neighbour.receiving_until:
                # the just sent packet keeps the receiver busy for more than the previous packet                                      
                neighbour.receiving_until = self.sending_until                                      

    def _queue_packet(self, packet):
        packet.is_queued = True
        # the packet is scheduled for resending as soon as the node is free;
        packet.time = max(self.sending_until, self.receiving_until)                         
        heap_push(Scheduler.events, packet)                                                         
        if not packet.is_queued:
            # only enques the packet if it had just been generated,
            # avoiding reenqueueing                                                                    
            self.queue.append(packet)                                                               
