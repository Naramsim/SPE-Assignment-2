# execute with source(chdir=TRUE) for automatic relative paths, if not uncomment the below function and manually enter
# the path where both this script and the .csv files are.
setwd("C:\\Users\\affa\\OneDrive\\Documents\\Coding\\Uni\\Performance\\Assignment\ II\\analysis")

#---------#
# HELPERS #
#---------#

# graphs

plot.new <- function()
    {
    dev.new()
    par(cex=0.6,
        cex.main=3.0,
        cex.lab=3.0,
        cex.axis=2.4,
        lwd=1.2,
        mar=c(6, 6, 6, 2))
    }

plot.throughput <- function(xData, yData)
    {
    title = "system"
    xLab = "offered throughput (%)"
    yLab = "actual throughput (%)"

    plot.new()
    plot(xData/speed, yData/speed, type="l", main=title, xlab=xLab, ylab=yLab)
    }

plot.packets <- function(xData, yData1, yData2)
    {
    title = "system"
    xLab = "offered throughput (%)"
    yLab = "packets (%)"
    colors = c("blue", "red")
    legend = c("collided", "lost")

    plot.new()
    plot(xData/speed, yData1, ylim=c(0, max(yData1)), type="l", col=colors[1], main=title, xlab=xLab, ylab=yLab)
    lines(xData/speed, yData2, type="l", col=colors[2])
    legend("topleft", legend=legend, lty=c(1, 1), col=colors, bty="n", cex=2.4)
    }

plot.node <- function(xData, yData1, yData2, node)
    {
    title = ifelse(node != -1, paste0("node ", node), "nodes means")
    xLab = "throughput (%)"
    yLab = "packets (%)"
    colors = c("blue", "red")
    legend = c("collided", "lost")

    plot.new()
    plot(xData/speed, yData1, ylim=c(0, max(yData1)), type="l", col=colors[1], main=title, xlab=xLab, ylab=yLab)
    lines(xData/speed, yData2, type="l", col=colors[2])
    legend("topleft", legend=legend, lty=c(1, 1), col=colors, bty="n", cex=2.4)
    }

boxplot.throughput <- function(data)
    {
    title = "system"
    xLab = "offered throughput (%)"
    yLab = "actual throughput (%)"

    data$throughput = data$throughput/speed
    data$load = data$load/speed

    plot.new()
    boxplot(throughput ~ load, data=data, main=title, xlab=xLab, ylab=yLab)
    }

boxplot.node <- function(data, node)
    {
    title = ifelse(node != -1, paste0("node ", node), "nodes means")
    xLab = "scale"
    yLab = "packets collided (%)"

    plot.new()
    boxplot(collision ~ scale, data=data, main=title, xlab=xLab, ylab=yLab)
    }

#----------#
# SETTINGS #
#----------#

speed = 1000000

#------#
# DATA #
#------#

data = read.csv("total.csv")

sets = aggregate(data[2:5], list(scale=data$scale), mean)

plot.throughput(sets$load, sets$throughput)
boxplot.throughput(data)
# plot.packets(sets$load, sets$collision, sets$lost)

data = read.csv("nodes.csv")
nodes = split(data, data$node)

for (node in nodes)
    {
    set = aggregate(node[1:5], list(scale=node$scale), mean)

    plot.node(set$throughput, set$collision, set$lost, set$node[1])
    boxplot.node(node, set$node[1])
    }
