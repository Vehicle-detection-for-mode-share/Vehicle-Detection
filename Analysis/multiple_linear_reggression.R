library(readxl)
library('dplyr')
library('tidyverse')
library(ggplot2)

#dir_path <- "C://Users//Kyriaki Kokka//Desktop"
dir_path <- "C://Users//Kyriaki Kokka//OneDrive - University of Cambridge//ComputerVision//Rdataset"
df <- read.csv(paste0(dir_path, "/CVdataset.csv"),stringsAsFactors = FALSE,header = TRUE)

#delete NA
data <- na.omit(df[,-c(3,8)])
#------------------------------------------MOTORS-------------------------------------------------
model1 <- lm(data = data,data$mmode ~ data$motor + data$PopDensity_new + 0)
summary(model1)

#Manually extract estimates from summary(model1) and create a new column Y with predicted values
data$Y <- (0.0212184 * data$motor) - (0.0004304 * data$PopDensity_new)

#plots for motors
a <- ggplot(data, aes(x = motor, y = mmode,label = city,color = country))+
  xlab("Number of motors from GSV") +
  ylab("Motor mode share") +
  geom_point(aes(x = motor, y = Y, color = country))+
  geom_point(alpha = 1) + # Show dots #1 full opacity,0 for transparent
  geom_text(vjust = 1,size = 2.5)+
  geom_smooth(method = "lm", se=FALSE,aes(group = 1), color="black") +
  ggtitle('Trend for all data')


a + geom_text(vjust = 1,size = 2.5) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

#zoom in
a + geom_text(vjust = 1,size = 2.5) + xlim(0,200) + ylim(0,2) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

d <- data[,c(1,7,8)]


data <- na.omit(df[,-c(4,9)])
#------------------------------------------CYCLES-------------------------------------------------
model2 <- lm(data = data,data$cmode ~ data$pedal + data$PopDensity_new + 0)
summary(model2)

#Manually extract estimates from summary(model2) and create a new column Z with predicted values
data$Z <- (0.0304539 * data$pedal) - (0.0002159 * data$PopDensity_new)

#plots for motors
a <- ggplot(data, aes(x = pedal, y = cmode,label = city,color = country))+
  xlab("Number of cycles from GSV") +
  ylab("Cycle mode share") +
  geom_point(aes(x = pedal, y = Z, color = country))+
  geom_point(alpha = 1) + # Show dots #1 full opacity,0 for transparent
  geom_text(vjust = 1,size = 2.5)+
  geom_smooth(method = "lm", se=FALSE,aes(group = 1), color="black") +
  ggtitle('Trend for all data')


a + geom_text(vjust = 1,size = 2.5) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

#zoom in
a + geom_text(vjust = 1,size = 2.5) + xlim(0,200) + ylim(0,7.5) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

d2 <- data[,c(1,7,8)]




#-------------------------------------------- fraction : GSV counts / population density -------------------------------

#delete NA
data <- na.omit(df[,-c(3,8)])
#data$fraction <- data$motor / log(data$PopDensity_new)
data$fraction <- data$motor / data$PopDensity_new
#------------------------------------------MOTORS-------------------------------------------------
model3 <- lm(data = data,data$mmode ~ data$fraction + 0)
summary(model3)

#Manually extract estimates from summary(model1) and create a new column Y with predicted values
#with log
data$Y <- 0.15080 * data$fraction
#without log
data$Y <- 84.508  * data$fraction

#plots for motors
a <- ggplot(data, aes(x = motor, y = Y,label = city,color = country))+
  xlab("Number of motors from GSV") +
  ylab("Predicted Motor mode share") +
  geom_point(aes(x = motor, y = Y, color = country))+
  geom_point(alpha = 1) + # Show dots #1 full opacity,0 for transparent
  geom_text(vjust = 1,size = 2.5)+
  geom_smooth(method = "lm", se=FALSE,aes(group = 1), color="black") +
  ggtitle('Trend for all data')


a + geom_text(vjust = 1,size = 2.5) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

#zoom in
a + geom_text(vjust = 1,size = 2.5) + xlim(25,200) + ylim(0,10) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

d <- data[,c(1,7,8)]


data <- na.omit(df[,-c(4,9)])
#data$fraction <- data$pedal / log(data$PopDensity_new)
data$fraction <- data$pedal / data$PopDensity_new
#------------------------------------------CYCLES-------------------------------------------------
model4 <- lm(data = data,data$cmode ~ data$fraction)
summary(model4)

#Manually extract estimates from summary(model2) and create a new column Z with predicted values
#with log
data$Z <- 0.23989 * data$fraction
#without log
data$Z <- 91.424 * data$fraction

#my.formula <- data$Z ~ data$pedal + 0


#plots for motors
a <- ggplot(data, aes(x = pedal, y = Z,label = city,color = country))+
  xlab("Number of cycles from GSV") +
  ylab("Predicted Cycle mode share") +
  geom_point(aes(x = pedal, y = Z, color = country))+
  geom_point(alpha = 1) + # Show dots #1 full opacity,0 for transparent
  geom_text(vjust = 1,size = 2.5)+
  geom_smooth(method = "lm", se=FALSE,aes(group = 1), color="black") +
  ggtitle('Trend for all data')


a + geom_text(vjust = 1,size = 2.5) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

#zoom in
a + geom_text(vjust = 1,size = 2.5) + xlim(0,200) + ylim(0,7) + geom_point(aes( size = data$PopDensity_new), alpha = 0.5) +
  scale_size(range = c(0.5, 12))

d2 <- data[,c(1,7,8)]

