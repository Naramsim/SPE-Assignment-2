###########
# IMPORTS #
###########

from heapq import heappop as heap_pop

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

    def step():
        packet = heap_pop(Scheduler.events)

        Scheduler.time_previous = Scheduler.time
        Scheduler.time = packet.time

        current_node = net.nodes[packet.sender]
        if not packet.is_queued:
            current_node.generate_next_packet()
        if not packet.is_lost:
            current_node.handle_packet(packet)

    def __str__(self):
        title = log.title(" ".join(["time =", settings.PRECISION, "s(abs)"]).format(Scheduler.time), "green")
        data = [["NODE", "STATUS", "QUEUE", "TO", "FOR s(rel)", "UNTIL s(abs)", "LOST", "SENT", "RECEIVED", "COLLIDED"]]

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

            data.append([str(node.id), status, str(queued), str(destinations), time_relative, time_absolute, str(node.packets_lost), str(node.packets_sent), str(node.packets_received), str(node.packets_collided)])

        table = AsciiTable(data, title)
        return "\n".join(["",
                          table.table])
