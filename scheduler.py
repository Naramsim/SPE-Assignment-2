#         #
# IMPORTS #
#         #

from heapq import heappop as heap_pop

from terminaltables import AsciiTable

import settings
import output

#       #
# CLASS #
#       #

class Scheduler:
    time = 0
    events = []

    def step():
        packet = heap_pop(Scheduler.events)
        Scheduler.time = packet.arrival_time

        current_node = settings.NODES[packet.sender]
        current_node.generate_next_packet()
        current_node.prepare_packet(packet)

    def __str__(self):
        data = [["NODE", "STATUS", "TO", "FOR s (rel)", "UNTIL s (abs)", "SENT", "RECEIVED", "COLLIDED"]]

        for node in settings.NODES:
            if node.is_idle():
                status = "IDLE"
                time_relative = "-"
                time_absolute = "-"
            elif node.is_sending():
                status = "SENDING"
                time_relative = str(node.sending_until-Scheduler.time)
                time_absolute = str(node.sending_until)
            elif node.is_receiving():
                status = "RECEIVING"
                time_relative = str(node.receiving_until-Scheduler.time)
                time_absolute = str(node.receiving_until)

            destinations = []
            for neighbour in node.neighbours:
                destinations.append(neighbour.id)

            data.append([str(node.id), status, str(destinations), time_relative, time_absolute, str(node.packets_sent), str(node.packets_received), str(node.packets_collided)])

        table = AsciiTable(data, output.title("time = {} s (abs)".format(Scheduler.time), "green"))
        return "".join(["\n", table.table])
