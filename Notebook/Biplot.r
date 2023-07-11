install.packages("devtools")
devtools::install_github("kassambara/factoextra")
library("factoextra")
Data= read.table("E:\\immo_eliza_scrapping_group7\\Notebook\\df_non_string_main.txt", header = TRUE,sep="\t",row.names = 1)
Data.Cor<-cor(DfClean_main)
res.pca <- prcomp(Data,  scale = TRUE)
var <- get_pca_var(res.pca)
install.packages("corrplot")
fviz_eig(res.pca)
#Biplot of individuals and variables
fviz_pca_biplot(res.pca, repel = TRUE,
                col.var = "#2E9FDF", # Variables color
                col.ind = "#696969"  # Individuals color
)