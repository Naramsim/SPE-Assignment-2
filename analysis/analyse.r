# execute with source(chdir=TRUE) for automatic relative paths, if not uncomment the below function and manually enter
# the path where both this script and the .csv files are
setwd("C:\\Users\\affa\\OneDrive\\Documents\\Coding\\Uni\\Performance\\Assignment\ II\\analysis")

#---------#
# HELPERS #
#---------#

# operations
as.numeric.factor <- function(x)
    {
    as.numeric(levels(x))[x]
    }

element.last <- function(set)
    {
    tail(as.numeric.factor(set), 1)
    }

sigfig <- function(number, digits=significantDigits)
    {
    formatC(signif(number, digits=digits), digits=digits, format="fg", flag="#")
    }

# outputs


# graphs
plot.new <- function()
    {
    dev.new()
    par(
        cex=0.6,
        cex.main=1.8,
        cex.lab=3.0,
        cex.axis=2.6,
        lwd=1.2,
        mar=c(6, 6, 6, 2)
        )
    }

plot.offered.actual <- function(xData, yData)
    {
    plot.new()
    plot(xData, yData, type="l", xlab="offered throughput (kB/s)", ylab="actual throughput (kB/s)")
    }

plot.offered.collided <- function(xData, yData)
    {
    plot.new()
    plot(xData, yData, type="l", xlab="offered throughput (kB/s)", ylab="collided packets (%)")
    }

plot.throughput.collided <- function(xData, yData, node)
    {
    plot.new()
    plot(xData, yData, type="l", xlab=paste0("node ", node, " throughput (kB/s)"), ylab="collided packets (%)")
    }

plot.throughput.lost <- function(xData, yData, node)
    {
    plot.new()
    plot(xData, yData, type="l", xlab=paste0("node ", node, " throughput (kB/s)"), ylab="lost packets (%)")
    }

#----------#
# SETTINGS #
#----------#

significantDigits = 5 # significant digits kept throughout the computation

#------#
# DATA #
#------#

data = read.csv("total.csv")

sets = aggregate(data[2:5], list(scale=data$scale), mean)

#    print(sets)

plot.offered.actual(sets$load, sets$throughput)
plot.offered.collided(sets$load, sets$collision)

data = read.csv("nodes.csv")
nodes = split(data, data$node)

for (node in nodes)
    {
    set = aggregate(node[1:5], list(scale=node$scale), mean)

#        print(set)

    plot.throughput.collided(set$throughput, set$collision, set$node[1])
    plot.throughput.lost(set$throughput, set$lost, set$node[1])
    }

#-------#
# NOTES #
#-------#
