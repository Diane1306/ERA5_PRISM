library(kohonen)

# data <- read.csv('./var/May.csv')
data <- read.csv('./var/March.csv')
# data <- read.csv('./var/April.csv')

X <- scale(data[,-1])
set.seed(222)
g <- somgrid(3, 3, topo="rectangular")
map <- som(X, grid=g, alpha=0.05, radius=.5)

# pdf("./plot/SOMtest/test.pdf")
# plot(map, type='mapping')
# dev.off()

# map$unit.classif
# map$codes
# map$data
# map$distances

# write.table(map$codes, "./var/MaySOMweight.txt")
# write.table(map$unit.classif, "./var/MaySOMtimeseries.txt")

write.table(map$codes, "./var/MarchSOMweight.txt")
write.table(map$unit.classif, "./var/MarchSOMtimeseries.txt")

# write.table(map$codes, "./var/AprilSOMweight.txt")
# write.table(map$unit.classif, "./var/AprilSOMtimeseries.txt")