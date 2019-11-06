
rm(list=ls())

library(reshape2)
library(ggplot2)
library(formattable)
library(RColorBrewer)

# DEFINE THE ORDER OF YOUR LABELS!!!
#DataLabels = c("p53_2W","p53_ctrl","p53_mdivi_2W","p53_mdivi_ctrl","KRAS_2W","KRAS_ctrl","KRAS_mdivi_2W","KRAS_mdivi_ctrl")
DataLabels = c("p53_2W","p53_aga","p53_ctrl","p53_mdivi_2W","p53_mdivi_aga","p53_mdivi_ctrl","KRAS_2W",'KRAS_aga',"KRAS_ctrl","KRAS_mdivi_2W",'KRAS_mdivi_aga',"KRAS_mdivi_ctrl")


transparent <- rgb(0, 0, 0, 0)

# Make sure you set your WD to where your MitoGraph output is
GnetsFolder <- '/Users/granthussey/Lab/10_23_19_MdiviPilotWork/NoGauss/'

Summary <- read.csv(paste(GnetsFolder,"output-summary.csv",sep=""))

# Conditions will appear in the same order as in the CSV summary file
Summary$Condition <- as.character(Summary$Condition)
Summary$Condition <- factor(Summary$Condition, levels=unique(Summary$Condition))

medSummary <- aggregate(data=Summary,.~Condition,FUN=median)
stdSummary <- aggregate(data=Summary,.~Condition,FUN=sd)
names(stdSummary)[-c(1,2)] <- paste(names(stdSummary)[-c(1,2)],'_sd',sep='')

Summary_MED_STD <- cbind(medSummary[,-2],stdSummary[,-c(1,2)])

# Expands the number of color palette options to fit the number of conditions in the dataset.
# To see all available choices simply attach the package with library(RColorBrewer)
# and run display.brewer.all() to display all palette options

nc <- length(levels(Summary$Condition))
getPalette = colorRampPalette(brewer.pal(9, "Set1")) #adjust the last parameter with # colors in the palette & color brewer name

# Here is a loop that creates 4 graphs where the X and Y variable are listed accordingly.
PlotsToBeMade <- c("Total_Connected_Components_Norm_to_Length_um","Avg_Edge_Length_um",
                   "Avg_Degree","Total_Edge_Norm_to_Length_um",
                   "PHI","Total_Connected_Components_Norm_to_Length_um",
                   "Volume_from_voxels_um3", "Average_width_um")

AxisLabels <- c("Total Connected Components\nNormalized to Total Length (um)","Avg Edge Length (um)",
                "Avg Degree","Total Edge #\nNormalized to Total Length (um)",
                "PHI","Total Connected Components\nNormalized to Total Length (um)",
                "Volume from Voxels (um3)","Med Mitochondrial Width (um)")

for (p in seq(1,length(PlotsToBeMade),2)) {

  feature1 <- PlotsToBeMade[p+0]
  feature2 <- PlotsToBeMade[p+1]

  dx_min <- paste(feature1,"-",feature1,"_sd",sep="")
  dx_max <- paste(feature1,"+",feature1,"_sd",sep="")
  dy_min <- paste(feature2,"-",feature2,"_sd",sep="")
  dy_max <- paste(feature2,"+",feature2,"_sd",sep="")

  # Adjust to modify error bar width
  error <- c(0.03,0.05,
             0.03,0.025,
             0.02,0.05,
             8,0.005)

  plot(ggplot(data=Summary_MED_STD,aes_string(x=feature1, y=feature2, color="Condition")) + geom_point(size=5) +
         geom_errorbar(aes_string(ymin=dy_min, ymax=dy_max), width=error[p], show.legend=FALSE) +
         geom_errorbarh(aes_string(xmin=dx_min, xmax=dx_max), height=error[p+1], show.legend=FALSE) +
         labs(x = feature1, y = feature2) +
         scale_color_manual(values = getPalette(nc), labels=DataLabels) +
         theme_bw() +
         theme(axis.text = element_text(size = 12, color = "black"),
               panel.grid.major = element_blank(),
               panel.grid.minor = element_blank(),
               panel.border = element_blank(),
               panel.background = element_blank(),
               axis.line.x = element_line(color = "black", size = 0.5, linetype = 1),
               axis.line.y = element_line(color = "black", size = 0.5, linetype = 1),
               legend.title = element_blank(),
               legend.justification = c(0, 1),
               legend.position = c(.75, 1),
               legend.text = element_text(size = 12, color = "black")
         ) +
         xlab(AxisLabels[p]) +
         ylab(AxisLabels[p+1])
  )

  ggsave(paste(GnetsFolder,"Plot-",p,"median_graph.png",sep=""), width = 14, height = 16, units = "cm", dpi = 300)

}

#
# SUMMARY CATEGORY BAR CHART
#

VarNames <- c("PHI", "Avg_Edge_Length_um", "Total_Edge_Norm_to_Length_um", "Total_Node_Norm_to_Length_um", "Total_Connected_Components_Norm_to_Length_um", "Free_Ends", "three_way_junction", "four_way_junction", "Avg_Degree")

medSummary_long <- melt(medSummary[,-2], id.vars=c("Condition"))
stdSummary_long <- melt(stdSummary[,-2], id.vars=c("Condition"))

Summary_MED_STD_long <- cbind(medSummary_long,data.frame("value_sd"=stdSummary_long$value))

Vars <- which(!is.na(match(Summary_MED_STD_long$variable,VarNames)))

Summary_MED_STD_long <- Summary_MED_STD_long[Vars,]

ggplot(Summary_MED_STD_long, aes(fill = Condition, x = variable, y = value)) +
  geom_col(position = position_dodge (width = 0.9)) +
  scale_fill_manual(values = getPalette(nc), labels=DataLabels) +
  geom_errorbar(aes(ymin=value-value_sd, ymax=value+value_sd), position=position_dodge(width = 0.9), width=0.5, color="grey30", size=0.5, show.legend=FALSE) +
  labs(x = "MitoGraph Measurement Metric", y = "Value") +
  scale_x_discrete(labels = c("PHI" = "PHI",
                              "Avg_Edge_Length_um" ="Avg Edge\nLength\n(um)",
                              "Total_Edge_Norm_to_Length_um" = "Total\nEdge\n(Norm\nto Length\n(um)",
                              "Total_Node_Norm_to_Length_um" = "Total\nNode\n(Norm\nto Length\n(um)",
                              "Total_Connected_Components_Norm_to_Length_um" = "Connected\nComponents\n(Norm\nto Length\n(um)",
                              "Free_Ends" = "Degree\nDist\nk=1\nfree-ends",
                              "three_way_junction" = "Degree\nDist\nk=3\n3-way\nJunction",
                              "four_way_junction" = "Degree\nDist\nk=4\n4-way\nJunction",
                              "Avg_Degree" = "Med\nDegree")) +
  theme_bw() +
  theme(axis.text.x = element_text(size = 8, color = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(),
        axis.line.x = element_line(color = "grey50", size = 0.5, linetype = 1),
        axis.line.y = element_line(color = "grey50", size = 0.5, linetype = 1),
        legend.title = element_blank(),
        legend.justification = c(0, 1),
        legend.position = "right",
        legend.text = element_text(size = 12, color = "black")
  )

ggsave(paste(GnetsFolder,"MED_SD_metricsmedian_graph.png",sep=""), width = 18, height = 16, units = "cm", dpi = 300)

#
# ALL METRICS BOX and Scatter PLOTS
#

Summary_long <- melt(Summary[,-1], id.vars=c("Condition"))

Vars <- which(!is.na(match(Summary_long$variable,VarNames)))

Summary_long <- Summary_long[Vars,]

ggplot(Summary_long, aes(fill=Condition, x=variable, y=value)) +
  stat_boxplot(geom = "errorbar", colour = "grey15", width = 0.5, position = position_dodge (width = 1)) +
  geom_boxplot (outlier.size = 0, colour = "grey15", position = position_dodge (width = 1)) +
  scale_fill_manual(values = getPalette(nc), labels=DataLabels) +
  geom_point (aes(colour = Condition, x=variable, y=value), pch=20, position=position_jitterdodge(jitter.width=0.75, jitter.height=0, dodge.width=1)) +
  scale_colour_manual(values=rep("grey20",nc), labels=DataLabels) +
  geom_vline(xintercept = c(1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5), colour = "grey65", linetype = "dotted") +
  labs(x = "MitoGraph Measurement Metric", y = "Value") +
  scale_x_discrete(labels = c("PHI" = "PHI",
                              "Avg_Edge_Length_um" ="Avg Edge\nLength\n(um)",
                              "Total_Edge_Norm_to_Length_um" = "Total\nEdge\n(Norm\nto Length\n(um)",
                              "Total_Node_Norm_to_Length_um" = "Total\nNode\n(Norm\nto Length\n(um)",
                              "Total_Connected_Components_Norm_to_Length_um" = "Connected\nComponents\n(Norm\nto Length\n(um)",
                              "Free_Ends" = "Degree\nDist\nk=1\nfree-ends",
                              "three_way_junction" = "Degree\nDist\nk=3\n3-way\nJunction",
                              "four_way_junction" = "Degree\nDist\nk=4\n4-way\nJunction",
                              "Avg_Degree" = "Avg\nDegree")) +
  theme_bw() +
  theme(axis.text.x = element_text(size = 8, color = "black"),
        axis.text.y = element_text(size = 8, color = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(),
        axis.line.x = element_line(color = "grey75", size = 0.5, linetype = 1),
        axis.line.y = element_line(color = "grey75", size = 0.5, linetype = 1),
        legend.title = element_blank(),
        legend.justification = c(0, 1),
        legend.position = "right",
        legend.text = element_text(size = 8, color = "black")
  )

ggsave(paste(GnetsFolder,"All_metricsmedian_graph.png",sep=""), width = 20, height = 16, units = "cm", dpi = 300)

ggplot(Summary, aes(fill = Condition, x = Condition, y = MitoGraph_Connectivity_Score)) +
  stat_boxplot(geom = "errorbar", width = 0.5, colour = "grey15") +
  geom_boxplot(colour = "grey15") +
  scale_fill_manual(values = getPalette(nc), labels=DataLabels) +
  geom_point (aes(colour = Condition, x = Condition, y = MitoGraph_Connectivity_Score),
              pch = 19, position =
                position_jitterdodge(jitter.width = 0.75, jitter.height = 0)) +
  scale_colour_manual(values=rep("grey20",nc), labels=DataLabels) +
  labs(x = "Treatment Condition", y = "MitoGraph Connectivity Score") +
  theme_bw() +
  theme(axis.text.x = element_text(size = 12, color = "black"),
        axis.text.y = element_text(size = 12, color = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.border = element_blank(),
        panel.background = element_blank(),
        axis.line.x = element_line(color = "grey75", size = 0.5, linetype = 1),
        axis.line.y = element_line(color = "grey75", size = 0.5, linetype = 1),
        legend.title = element_blank(),
        legend.justification = c(0, 1),
        legend.position = "right",
        legend.text = element_text(size = 12, color = "black")
  )

ggsave(paste(GnetsFolder,"MitoGraph_Connectivity_scoremedian_graph.png",sep=""), width = 20, height = 16, units = "cm",
       dpi = 300)

write.table(Summary_MED_STD_long, file = paste(GnetsFolder,"Summary_MED_STD.csv",sep=""), sep = ",", quote = FALSE, row.names = F)
formattable(Summary_MED_STD_long, row.names = F, list( " " = FALSE))

#Analysis of Variance:

AOV_Stats_New <- NULL
for (var in seq(3,21,1)) {
  Temp <- data.frame('Condition'=Summary$Condition,'Var'=Summary[,var])
  Test <- TukeyHSD(aov(data=Temp, Var~Condition))
  AOV_Stats_New <- rbind(AOV_Stats_New,data.frame('Comparison'=row.names(Test$Condition),'Variable'=names(Summary)[var],'p.value'=Test$Condition[4]))
}

head(AOV_Stats_New)
write.csv(AOV_Stats_New, paste(GnetsFolder,"AOV_stats_new.csv",sep=""))
#Adjust the following for color coded signficance: Green = p < 0.05 & Red = p > 0.05
sign_formatter <- sign_formatter <- formatter("span", style = x ~ style(color = ifelse(x > 0.05, "red", ifelse(x < 0.05, "green", "black"))))
sign_formatter(c(-1, 0, 1))
formattable(AOV_Stats_New, list(p.value = sign_formatter))
