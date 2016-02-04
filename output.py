#         #
# IMPORTS #
#         #

from colorclass import Color, Windows

#           #
# FUNCTIONS #
#           #

def success(string):
    return Color("".join(["{higreen}", string, "{/green}"]))

def error(string):
    return Color("".join("ERROR: ", ["{hired}", string, "{/red}"]))

def warning(string):
    return Color("".join(["WARNING: ", "{hiyellow}", string, "{/yellow}"]))

def title(string, color):
    return Color("".join(["{hi", color, "}", string, "{/", color, "}"]))
