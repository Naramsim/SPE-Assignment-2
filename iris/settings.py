from colorclass import Windows
import re
import traceback

Windows.enable()

# distributions
#

PACKET_SIZE_DISTRIBUTION = ""
INTERARRIVAL_TIME_DISTRIBUTION = ""
BINOMIAL_P = 1
BINOMIAL_N = 1
PACKET_SIZE_MIN = 1
PACKET_SIZE_MAX = 1
EXPONENTIAL_SCALE = 1 # Scale is the parameter used by numpy instead of rate, it is equal to 1/rate https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.random.exponential.html
EXPONENTIAL_RATE = 1 
SEED = None

# net
#

BOUNDS = 0.25
BUFFER = 100
SPEED = 1*1000*1000 # 1 MB or 8 Mb
NODES = []

POINTS = []
packet_size_re = "\t(\w+)\(p=(0\.\d+), n=(\d+)\)Support: \[(\d+), (\d+)\].*"
arrival_time_re = "\t(\w+)\(rate=([\d\?\.]+).*"
buffer_size_re = "Node buffer size: (\d+)"
points_re = "Node\d\(0\.(\d+), 0\.(\d+)\);"
try:
    for i, line in enumerate(open('./data/pezze.data')):
        size = re.search(packet_size_re, line)
        if(size):
            PACKET_SIZE_DISTRIBUTION = size.group(1)
            BINOMIAL_P = float(size.group(2))
            BINOMIAL_N = int(size.group(3))
            PACKET_SIZE_MIN = int(size.group(4))
            PACKET_SIZE_MAX = int(size.group(5))
        time = re.search(arrival_time_re, line)
        if(time):
            INTERARRIVAL_TIME_DISTRIBUTION = time.group(1)
            EXPONENTIAL_SCALE = float(time.group(2)) if time.group(2) != "?" else "None"
        buffer_size = re.search(buffer_size_re, line)
        if(buffer_size):
            BUFFER = int(buffer_size.group(1))
        node = re.search(points_re, line)
        if(node):
            POINTS.append((int(node.group(1))/1000, int(node.group(2))/1000))
except:
    traceback.print_exc()

# simulation
#

VERBOSE = None
QUIET = None
FOLDER = None
TIME = None
STEPS = None
PRECISION = "{:.8g}"
