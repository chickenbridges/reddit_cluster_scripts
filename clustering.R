# Define variables
data_file = 'data.csv'
num_clus = 40
plot_type = 'fan'
# plot_type = 'phylogram'

# Load data
setwd("/home/ed/Downloads/Reddit map")
mydata <- read.table(data_file, header=TRUE, sep='\t', row.names=1)

# Load required libraries
require(vegan)
require(ape)

# Produce distance matrix
d <- vegdist(t(mydata), method = "jaccard") # distance matrix

# Cluster subreddits
fit <- hclust(d, method="ward")

# Plot graph
mypal = rep(c("#556270", "#4ECDC4", '#D43700', '#0139bA'), num_clus/4)
clus5 = cutree(fit, num_clus)
plot(as.phylo(fit), type=plot_type, tip.color=mypal[clus5], label.offset=0.1, no.margin=TRUE, cex=0.9)
