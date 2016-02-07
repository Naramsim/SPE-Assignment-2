###########
# IMPORTS #
###########

from heapq import heappop as heap_pop
from heapq import nsmallest as heap_read

from terminaltables import AsciiTable

import settings
import log
import __main__ as net

#########
# CLASS #
#########

class Scheduler:
    time = 0
    time_previous = 0
    events = []

    def __str__(self):
        lines = ["",
                 Scheduler._get_heap_table(),
                 "",
                 Scheduler._get_status_table()]
        return "\n".join(lines)

    def step():
        # logging
        if settings.VERBOSE:
            lines = ["",
                     "",
                     log.success("stepping")]
            print("\n".join(lines))
        # logging

        packet = heap_pop(Scheduler.events)

        Scheduler.time_previous = Scheduler.time
        Scheduler.time = packet.time

        current_node = net.nodes[packet.sender]                                                     # this works because the way the list is
        if not packet.is_queued:                                                                    # built introduces a 1:1 relation between
            current_node.generate_next_packet()                                                     # the id and the index;
        if not packet.is_lost:                                                                      # if the packet was lost (i.e. the queue
            current_node.handle_packet(packet)                                                      # was full, take no action

        # logging
        if settings.VERBOSE:
            print(Scheduler())
        # logging

    def _get_heap_table():
        heap_title = log.color("events", "green")
        heap_data = [["TIME", "NODE", "PACKET"]]

        ordered_events = heap_read(len(Scheduler.events), Scheduler.events)
        for packet in ordered_events:
            if packet.time == Scheduler.time:
                time = log.evidence(settings.PRECISION.format(packet.time), "yellow")
            else:
                time = settings.PRECISION.format(packet.time)

            heap_data.append([time, str(packet.sender), str(packet.id)])

        return AsciiTable(heap_data, heap_title).table

    def _get_status_table():
        status_title = log.color(" ".join(["time =", settings.PRECISION, "s(abs)"]).format(Scheduler.time), "green")
        status_data = [["NODE", "STATUS", "QUEUE", "TO", "FOR s(rel)", "UNTIL s(abs)", "LOST", "SENT", "RECEIVED", "COLLIDED"]]

        for node in net.nodes:
            if node.is_idle():
                status = log.evidence("IDLE", "green")
                time_relative = "-"
                time_absolute = "-"
            elif node.is_sending():
                status = log.evidence("SENDING", "cyan")
                time_relative = settings.PRECISION.format(node.sending_until-Scheduler.time)
                time_absolute = settings.PRECISION.format(node.sending_until)
            elif node.is_receiving():
                status = log.evidence("RECEIVING", "magenta")
                time_relative = settings.PRECISION.format(node.receiving_until-Scheduler.time)
                time_absolute = settings.PRECISION.format(node.receiving_until)

            destinations = []
            for neighbour in node.neighbours:
                destinations.append(neighbour.id)

            queued = []
            for packet in node.queue:
                queued.append(packet.id)

            status_data.append([str(node.id), status, str(queued), str(destinations), time_relative, time_absolute, str(node.packets_lost), str(node.packets_sent), str(node.packets_received), str(node.packets_collided)])

        return AsciiTable(status_data, status_title).table
