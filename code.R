dir()
df <- read.csv(file = 'merged_stanford_berkeley_breadth_study_clean.csv')
head(df)
df$job
#recoding job positions
df$job[grepl("(?i)(Chief|CEO|CFO|CIO|Vice President|VP|President|Senior|Sr.|Sr|Head|Principal)", df$job)] <- "Senior"
df$job[!is.na(df$job) & df$job != "Senior"] <- "Rank_File"
write.csv(df, 'recoded.csv')
#filter for qsort cond 2
library(dplyr)
df <- filter(df, Qsort_cond == 2)
#finding OCP levels
df_sr <- filter(df, job == "Senior")
df_rf <- filter(df, job == "Rank_File")
levels <- colMeans(select(df_sr, "innovative": "customer_oriented")) - 
  colMeans(select(df_rf, "innovative": "customer_oriented"))
levels <- as.numeric(levels)
column_names <- c("innovative_level", "risk_taking_level", 
               "acting_autonomy_level", "collaborative_level", 
               "detail_oriented_level", "performance_oriented_level", 
               "transparent_level", "feedback_oriented_level",
               "supportive_level", "individualistic_level", "results_oriented_level", 
               "decisive_level", "flexible_level", "people_talent_level", 
               "inclusive_level", "courageous_level", "selfless_level",
               "confronting_conflict_level", "having_integrity_level",
               "customer_oriented_level")
levels_df <- t(data.frame(levels))
colnames(levels_df) <- column_names
levels_df
#storing data in excel
install.packages("xlsx")
library("xlsx")
write.xlsx(levels_df, file = "OCPlevels.xlsx")

#visualizations
levels_df_t <- as.data.frame(t(levels_df))
levels_df_t
top_5 <- as.data.frame(head(sort(levels,decreasing=TRUE), n = 5))
top_5
bottom_5 <- as.data.frame(head(sort(levels,decreasing=FALSE), n = 5))
bottom_5

#barchart
colnames(bottom_5)[1] <- "values"
top_5
top_5_asc<- top_5[seq(dim(top_5)[1],1),]
top_5_asc <- as.data.frame(top_5_asc)
colnames(top_5_asc)[1] <- "values"
top_5_asc
bottom_5
all <- rbind(bottom_5, top_5_asc)
all
all$OCP <- c("Supportive Level", "Inclusive Level",
           "People Talent Level", "Collaborative Level", 
           "Feedback Oriented Level", 
           "Selfless Level", 
           "Confronting Conflict Level", "Detail Oriented Level", 
           "Risk Taking Level", "Results Oriented Level")
all
all$state <-c('Greatest Decrease','Greatest Decrease','Greatest Decrease','Greatest Decrease','Greatest Decrease','Greatest Increase','Greatest Increase','Greatest Increase','Greatest Increase','Greatest Increase')
all$OCP <- factor(all$OCP, levels = all$OCP[order(all$values)])
barchart <- ggplot(all, aes(x=OCP, y=values, group = state, fill = state)) + 
  geom_bar(stat = "identity") +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1), 
        axis.title.y = element_text(face="bold"),
        axis.title.x = element_text(face="bold"), 
        plot.title = element_text(hjust = 0.5), 
        strip.placement = "outside", 
        legend.position = "none") +
  xlab('Cultural Attribute') + ylab('Average Difference') +
  ggtitle("Top Five Most Positively and Negatively
          Miscalibrated Organizational Culture Attributes 
          Between Senior Managers and Rank-and-File Employees") + 
  scale_fill_manual(values=c("red","blue"))
barchart
