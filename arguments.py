###########
# IMPORTS #
###########

import argparse

import settings

#############
# FUNCTIONS #
#############

def parse():
    parser = argparse.ArgumentParser(description="simulate the behaviour of a simil aloha net")
    group_output = parser.add_mutually_exclusive_group()
    group_output.add_argument("-q", "--quiet", action="store_true", help="suppress all output on console, including the final statistics report")
    group_output.add_argument("-v", "--verbose", action="store_true", help="output on console the entire simulation's behaviour")
    parser.add_argument("-f", "--file", type=str, help="append to a file at relative path F the final statistics report", metavar="F")
    parser.add_argument("-r", "--seed", type=_positive_int, help="the initialization seed R of the random functions (default is the current UNIX time)", metavar="R")
    group_limits = parser.add_mutually_exclusive_group(required=True)
    group_limits.add_argument("-t", "--time", type=_positive_float, help="run the simulation until time T", metavar="T")
    group_limits.add_argument("-s", "--steps", type=_positive_int, help="run the simulation for S amount of steps", metavar="S")
    parser.add_argument("scale", type=_positive_float, help="the scale of the gamma distribution controlling the inter-arrival time")
    return parser.parse_args()

def save(args):
    settings.VERBOSE = args.verbose
    settings.QUIET = args.quiet
    settings.FILE = args.file
    settings.SEED = args.seed
    settings.GAMMA_SCALE = args.scale
    settings.TIME = args.time
    settings.STEPS = args.steps

def _positive_int(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("number must be positive")
    return number

def _positive_float(value):
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("number must be positive")
    return number
