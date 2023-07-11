# Load data
address= file.choose()
DfClean_main= read.table("E:\\immo_eliza_scrapping_group7\\Notebook\\df_non_string_main.txt", header = TRUE,sep="\t",row.names = 1)
# Compute distances and hierarchical clustering
dd <- dist(scale(DfClean_main), method = "euclidean")
hc <- hclust(dd, method = "ward.D2")
class(hc)
plot(hc)

# Put the labels at the same height: hang = -1
plot(hc, hang = -1, cex = 0.6)

hcd <- as.dendrogram(hc)
class(hcd)

#coloring hierarchical clustering with package dendextend
suppressPackageStartupMessages(library(dendextend))
avg_dend_obj <- as.dendrogram(hcd)
avg_col_dend <- color_branches(hcd,h = 2,k=2, groupLabels =c(1,2),col = c("red", "purple"))
avg_col_dend <-   set(avg_col_dend,"labels_cex", 0.7)
avg_col_dend <-   set(avg_col_dend,"labels_col", "black")
avg_col_dend <-   set(avg_col_dend,"branches_lwd", 3)
#branches_lwd - set the line width of branches 
# or (using assign_values_to_branches_edgePar); 
avg_col_dend <-   set(avg_col_dend,"branches_lty", 1)
plot(avg_col_dend)
