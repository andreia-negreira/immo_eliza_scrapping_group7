DfClean_main= read.table("E:\\immo_eliza_scrapping_group7\\Notebook\\df_non_string_main.txt", header = TRUE,sep="\t",row.names = 1)
library(lavaan)
library(semPlot)
library(OpenMx)
library(tidyverse)
library(knitr)
library(kableExtra)
library(GGally)
library(foreign) 
# Organizing package information for table
packages <- c("tidyverse", "knitr", "kableExtra", "lavaan", "semPlot", "OpenMx", "GGally")
display <- c("Package","Title", "Maintainer", "Version", "URL")
table <- matrix(NA, 1, NROW(display), dimnames = list(1, display))
for(i in 1:NROW(packages)){
  list <- packageDescription(packages[i])
  table <- rbind(table, matrix(unlist(list[c(display)]), 1, NROW(display), byrow = T))
}
table[,NROW(display)] <- stringr::str_extract(table[,NROW(display)], ".+,")

# Table of packages
kable(table[-1,], format = "html", align = "c") %>%
  kable_styling(bootstrap_options = c("striped", "hover", "condensed"))
attach(DfClean_main)
			
model <-Price ~ Number_of_rooms + Living_Area + Terrace_Area + Garden_area + Surface_of_the_land + Surface_area_of_the_plot_of_land + Number_of_facades
fit <- lavaan::cfa(model, data = DfClean_main)
summary(fit, fit.measures = TRUE, standardized=T,rsquare=T)
library(semPlot)

semPaths(fit,"std",layout = 'tree', edge.label.cex=.9, curvePivot = TRUE)
