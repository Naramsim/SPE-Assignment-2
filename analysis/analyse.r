# execute with source(chdir=TRUE) for automatic relative paths, if not uncomment the below function and manually enter
# the path where both this script and the .csv files are.
setwd("C:\\Users\\affa\\OneDrive\\Documents\\Coding\\Uni\\Performance\\Assignment\ II\\analysis")

#---------#
# HELPERS #
#---------#

# graphs

plot.new <- function()
    {
    dev.new(width=16, height=9)
    par(cex=0.6,
        cex.main=1.2,
        cex.lab=3.0,
        cex.axis=2.4,
        lwd=1.2,
        mar=c(6, 7.2, 6, 3),
        bty="n")
    }

plot.throughput <- function(xData, yData)
    {
    xLab = "offered throughput (%)"
    yLab = "actual throughput (%)"

    plot.new()
    plot(xData/percent, yData/percent, type="l", xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 14, 2))
    }

plot.packets <- function(xData, yData1, yData2)
    {
    xLab = "offered throughput (%)"
    yLab = "packets (%)"
    colors = c("blue", "red")
    legend = c("collided", "lost")

    plot.new()
    plot(xData/percent, yData1, ylim=c(0, max(yData1)), type="l", col=colors[1], xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    lines(xData/percent, yData2, type="l", col=colors[2])
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 100, 10))
    legend("topleft", legend=legend, lty=c(1, 1), col=colors, bty="n", cex=2.4)
    }

plot.node <- function(xData, yData1, yData2, node)
    {
    title = paste0("node ", node)
    xLab = "throughput (%)"
    yLab = "packets (%)"
    colors = c("blue", "red")
    legend = c("collided", "lost")

    plot.new()
    plot(xData/percent, yData1, type="l", col=colors[1], main=title, xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    lines(xData/percent, yData2, type="l", col=colors[2])
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 100, 10))
    legend("topleft", legend=legend, lty=c(1, 1), col=colors, bty="n", cex=2.4)
    }

boxplot.throughput <- function(data)
    {
    xLab = "offered throughput (%)"
    yLab = "actual throughput (%)"

    data$throughput = data$throughput/percent
    data$load = data$load/percent

    plot.new()
    boxplot(throughput ~ load, data=data, at=sort(unique(data$load)), boxwex=1, xlab=xLab, ylab=yLab, boxwex=1, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 14, 2))
    }

boxplot.node <- function(data, node)
    {
    title = ifelse(node != -1, paste0("node ", node), "nodes means")
    xLab = "offered throughput (%)"
    yLab = "packets collided (%)"

    data$load = data$load/percent

    plot.new()
    boxplot(collision ~ load, data=data, at=sort(unique(data$load)), main=title, xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 100, 10))
    }

#----------#
# SETTINGS #
#----------#

speed = 1000000
percent = speed/100

#------#
# DATA #
#------#

data = read.csv("total.csv")

sets = aggregate(data[2:5], list(scale=data$scale), mean)

plot.throughput(sets$load, sets$throughput)
boxplot.throughput(data)
plot.packets(sets$load, sets$collision, sets$lost)

data = read.csv("nodes.csv")
nodes = split(data, data$node)

for (node in nodes)
    {
    set = aggregate(node[1:6], list(scale=node$scale), mean)

    plot.node(set$load, set$collision, set$lost, set$node[1])
    boxplot.node(node, set$node[1])
    break
    }
