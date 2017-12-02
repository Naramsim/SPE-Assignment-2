# execute with source(chdir=TRUE) for automatic relative paths, if not uncomment the below function and manually enter
# the path where this script is.
# setwd("/home/rstudio")

#---------#
# HELPERS #
#---------#

plot.new <- function() {
    dev.new(width=16, height=9)
    par(cex=0.6,
        cex.main=1.2,
        cex.lab=3.0,
        cex.axis=2.4,
        lwd=1.2,
        mar=c(6, 7.2, 6, 3),
        bty="n")
}

plot.scale <- function(xData, yData) {
    xLab = "rate"
    yLab = "offered throughput (%)"

    plot.new()
    # rate = 1/scale
    plot(1/xData, yData/percent, type="l", log="x", xlab=xLab, ylab=yLab, xaxt="n")
    axis(side=1, at=c(c(0, 10, 20, 25, 50, 100, 250, 500, 1000)))
    axis(side=2, at=seq(0, 1000, 20))
}

plot.throughput <- function(xData, yData) {
    xLab = "offered throughput (%)"
    yLab = "actual throughput (%)"
    
    plot.new()
    plot(xData/percent, yData/percent, type="l", xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 20))
    axis(side=2, at=seq(0, 16, 4))
}

plot.relativethroughput <- function(xData, yData) {
    xLab = "offered throughput (%)"
    yLab = "relative actual throughput (%)"

    plot.new()
    plot(xData/percent, (yData/percent)*(100/(xData/percent)), type="l", xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 20))
    axis(side=2, at=seq(0, 100, 20))
}

plot.packets <- function(xData, yData1, yData2) {
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

plot.decision <- function(xData, yData) {
    xLab = "collided packets (%)"
    yLab = "actual throughput (%)"

    plot.new()
    plot(xData, yData/percent, type="l", xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 20))
    axis(side=2, at=seq(0, 18, 2))
}

plot.node <- function(xData, yData1, yData2, node) {
    title = paste0("node ", node)
    xLab = "offered throughput (%)"
    yLab = "packets (%)"
    colors = c("blue", "red")
    legend = c("collided", "lost")

    plot.new()
    plot(xData/percent, yData1, type="l", col=colors[1], main=title, xlab=xLab, ylab=yLab, xaxt="n", yaxt="n", xlim=c(0, 100))
    lines(xData/percent, yData2, type="l", col=colors[2])
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 100, 10))
    legend("topleft", legend=legend, lty=c(1, 1), col=colors, bty="n", cex=2.4)
}

boxplot.throughput <- function(data) {
    xLab = "offered throughput (%)"
    yLab = "actual throughput (%)"
    
    data$throughput = data$throughput/percent
    data$load = data$load/percent

    plot.new()
    boxplot(throughput ~ load, data=data, at=sort(unique(data$load)), boxwex=1, xlab=xLab, ylab=yLab, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 20))
    axis(side=2, at=seq(0, 16, 4))
}

boxplot.packets <- function(data) {
    xLab = "offered throughput (%)"
    yLab = "packets collided (%)"

    data$load = data$load/percent

    plot.new()
    boxplot(collision ~ load, data=data, at=sort(unique(data$load)), boxwex=1, xlab=xLab, ylab=yLab, boxwex=1, xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 100, 10))
}

boxplot.node <- function(data, node) {
    title = ifelse(node != -1, paste0("node ", node), "nodes means")
    xLab = "offered throughput (%)"
    yLab = "packets collided (%)"

    data$load = data$load/percent

    plot.new()
    boxplot(collision ~ load, data=data, at=sort(unique(data$load)), main=title, xlab=xLab, ylab=yLab, xlim=c(0, 100), xaxt="n", yaxt="n")
    axis(side=1, at=seq(0, 100, 10))
    axis(side=2, at=seq(0, 100, 10))
}

plot.modelVsSimulator.packets <- function(model, simulator) {
    xLab = "offered throughput (%)"
    yLab = "packets collided (%)"
    colors = c("blue", "red")
    legend = c("model", "simulator")

    plot.new()
    plot(model$load, model$prob, xlab=xLab, ylab=yLab, type="l", col=colors[1], xaxt="n", yaxt="n", xlim=c(0, 100))
    lines(simulator$load/percent, simulator$collision, col=colors[2])
    
    axis(side=1, at=seq(0, 100, 20))
    axis(side=2, at=seq(0, 100, 20))
    legend("topleft", legend=legend, lty=c(1, 1), col=colors, bty="n", cex=2.4)
}

plot.modelVsSimulator.throughput <- function(model, simulator) {
    xLab = "offered throughput (%)"
    yLab = "actual throughput (%)"
    colors = c("blue", "red")
    legend = c("model", "simulator")

    plot.new()
    plot(model$load, model$prob, xlab=xLab, ylab=yLab, type="l", col=colors[1], xaxt="n", yaxt="n", xlim=c(0, 100))
    lines(simulator$load/percent, simulator$throughput/percent, , col=colors[2])
    
    axis(side=1, at=seq(0, 100, 20))
    axis(side=2, at=seq(0, 100, 20))
    legend("topright", legend=legend, lty=c(1, 1), col=colors, bty="n", cex=2.4)
}

#----------#
# SETTINGS #
#----------#

speed = 1000000
percent = speed/100

#------#
# DATA #
#------#

total.data = read.csv("./data/total.csv")
sets = aggregate(total.data[2:5], list(scale=total.data$scale), mean)

if (TRUE) {
    plot.scale(sets$scale, sets$load)
    plot.throughput(sets$load, sets$throughput)
    plot.relativethroughput(sets$load, sets$throughput)
    boxplot.throughput(total.data)
    plot.packets(sets$load, sets$collision, sets$lost)
    boxplot.packets(total.data)
    plot.decision(sets$collision, sets$throughput)
}

if (TRUE) {
    nodes.data = read.csv("./data/nodes.csv")
    nodes = split(nodes.data, nodes.data$node)
    index = 0
    for (node in nodes) {
        set = aggregate(node[1:6], list(scale=node$scale), mean)
    
        plot.node(set$load, set$collision, set$lost, set$node[1])
        # dev.copy2pdf(file=paste("~/graphs/Node", index, ".pdf"), width = 14, height = 8.5)
        boxplot.node(node, set$node[1])
        # dev.copy2pdf(file=paste("~/graphs/Node", index, "Boxplot.pdf"), width = 14, height = 8.5)
        index = index + 1
    }
}

if (FALSE) {
    model.data <- read.csv('./model/data/output.csv')
    model.data <- aggregate(.~state+load, model.data, sum)

    collision_rate <- split(model.data, model.data$state)[['c']]
    transmission_rate <- split(model.data, model.data$state)[['t']]

    transmission_rate$prob <- transmission_rate$prob*100
    collision_rate$prob <- collision_rate$prob*100

    plot.modelVsSimulator.packets(collision_rate, sets)
    plot.modelVsSimulator.throughput(transmission_rate, sets)
}
