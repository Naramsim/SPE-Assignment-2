# execute with source(chdir=TRUE) for automatic relative paths, if not uncomment the below function and manually enter
# the path where both this script and the .csv files are
setwd("C:\\Users\\affa\\OneDrive\\Documents\\Coding\\Uni\\Performance\\Assignment I\\analysis")

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
    if (doDeliver)
        par(
            cex=0.6,
            cex.main=1.8,
            cex.lab=3.0,
            cex.axis=2.6,
            lwd=1.2,
            mar = c(6, 6, 6, 2)
            )
    }

#----------#
# SETTINGS #
#----------#

doDeliver = TRUE # whether the plots are rendered for exporting to .pdf or not
doPlot = TRUE # whether the data is plotted or not

significantDigits = 5 # significant digits kept throughout the computation

#------#
# DATA #
#------#



#-------#
# NOTES #
#-------#
