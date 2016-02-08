###########
# IMPORTS #
###########

from colorclass import Color as colorize

import settings

#############
# FUNCTIONS #
#############

def success(string):
    if settings.VERBOSE:
        print(colorize("    ".join(["{higreen}[    OK    ]{/green}", string])))

def error(string):
    if settings.VERBOSE:
        print(colorize("    ".join(["{hired}[   FAIL   ]{/red}", string])))

def warning(string):
    if settings.VERBOSE:
        print(colorize("    ".join(["{hiyellow}[   WARN   ]{/yellow}", string])))

def plain(string):
    if settings.VERBOSE:
        print(string)

def format_color(string, color):
    return colorize("".join(["{", color, "}", string, "{/", color, "}"]))

def format_evidence(string, color):
    return colorize("".join(["{bg", color, "}{black}", string, "{/black}{/bg", color, "}"]))
