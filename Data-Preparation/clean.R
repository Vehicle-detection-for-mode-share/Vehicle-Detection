#install.packages("osmdata")
#install.packages("sf")
#install.packages("tidyverse")
#install.packages("ggmap")
#install.packages("rgdal")
#install.packages("leaflet")
#install.packages("tidyverse")
#install.packages("rgeos")
#install.packages("raster")
#install.packages("ggplot2")
#install.packages("sf")
#install.packages("mapview")
#install.packages("maptools")
#install.packages("sp")
#install.packages("readxl")
#install.packages("readr")
#install.packages("grid")
#install.packages("gridExtra")
#install.packages("xtable")
#install.packages("knitr")
#install.packages("plyr")


#install.packages("tidyverse", repos='http://cran.uk.r-project.org')
#install.packages("rgdal", repos='http://cran.uk.r-project.org')
#install.packages("raster", repos='http://cran.uk.r-project.org')
#install.packages("sp", repos='http://cran.uk.r-project.org')
#install.packages("readxl", repos='http://cran.uk.r-project.org')
#install.packages("readr", repos='http://cran.uk.r-project.org')
#install.packages("rgeos", repos='http://cran.uk.r-project.org')

#library(osmdata)
#library(sf)
#library(ggmap)

#install.packages("rgdal", repos='http://cran.uk.r-project.org')
library(rgdal)
#library(leaflet)
library(raster)
#library(ggplot2)
#install.packages("sf", repos='http://cran.uk.r-project.org')
#library(sf)
#library(mapview)
#library(maptools)
library(sp)
library(readxl)
library(readr)
#library(grid)
#library(gridExtra)
#library(xtable)
#library(knitr)
library(crs)
library(plyr)
library(tidyverse)
library(rgeos)

intersect_data <-function(data,zone){
  #Create planar(cartesian) projection 
  crs <- CRS( "+proj=utm +zone=32 +ellps=WGS72 +units=m +no_defs")     # UTM zone = 32 N
  wgs84 <- CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")  # long/lat
  
  options(digits=14)
  data$lat <- as.numeric(data$lat)
  data$lon <- as.numeric(data$lon)
  
  zone <- spTransform(zone,crs)
  coords <- data.frame(as.numeric(data$lon),as.numeric(data$lat))
  data <-  spTransform(SpatialPointsDataFrame(coords = coords,proj4string = wgs84,data = as.data.frame(data)), crs)
  
  proj4string(data) <- proj4string(zone)
  counts2 <- raster::intersect(data,zone) 
  return(counts2@data)
}

clean_data <-function(data){
  data <- data[,-c(2,4)]
  data <- data[,-c(2)]
  a <- data.frame(str_split_fixed(data$FileName, "/", 7))
  d <- data.frame(str_split_fixed(a$X7, ".txt", 2))
  b <- data.frame(str_split_fixed(data$V4, "_", 5))
  c <- data.frame(str_split_fixed(b$X4, ".jpg", 2))
  f <- cbind(d,b,c)
  colnames(f) <- c("Folder","no","lat","lon","direction1","nothing","noth","direction2")
  f <- f[,-c(2,6,7,9)]
  f <- f %>% filter(f$direction2 %in% c(0))
  return(f)
}


intersect_data <-function(data,zone){
  #Create planar(cartesian) projection 
  crs <- CRS( "+proj=utm +zone=32 +ellps=WGS72 +units=m +no_defs")     # UTM zone = 32 N
  wgs84 <- CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")  # long/lat
  
  options(digits=16)
  data$lat <- as.numeric(data$lat)
  data$lon <- as.numeric(data$lon)
  
  zone <- spTransform(zone,crs)
  coords <- data.frame(as.numeric(data$lon),as.numeric(data$lat))
  data <-  spTransform(SpatialPointsDataFrame(coords = coords,proj4string = wgs84,data = as.data.frame(data)), crs)
  
  proj4string(data) <- proj4string(zone)
  counts2 <- raster::intersect(data,zone) 
  return(counts2@data)
}


gdb_path <- "/rds/user/kk704/hpc-work/sampling/"
city <- readOGR(dsn = gdb_path,layer= "Kiev_grid", verbose = FALSE)
#Transform to long/lat
city <- spTransform(city, "+init=epsg:4326")
#leaflet(city) %>% addTiles() %>% addPolygons()
tokyo <- gUnaryUnion(city)
print("read map")

dir_path <- "/rds/user/kk704/hpc-work/sampling/"
rome_df <- read.csv(paste0(dir_path, "/Kiev.csv"),stringsAsFactors = FALSE)
copy <- rome_df
rome_copy <- clean_data(rome_df)
df <- unique(rome_copy[,-c(4,5)])

df$lat <- as.character(df$lat)
df$lon <- as.character(df$lon)
df$name <- paste(df$lat,df$lon,sep="_")

final <- intersect_data(df,tokyo)
print("intersect done!")

fina <- unique(final["Folder"])

dir_path <- "/rds/user/kk704/hpc-work/sampling/"
write.csv(final[,-c(5)], file = paste0(dir_path, "/Kiev_final_locations.csv"),row.names = FALSE)

finalb <- unique(as.data.frame(final[,-c(2,3,4,5)]))
all_folders <- unique(as.data.frame(df[,-c(2:4)]))

#folders that are only in "all_folders and not in finalb"
delete <- all_folders[!(all_folders$`df[, -c(2:4)]` %in% finalb$`final[, -c(2, 3, 4, 5)]` ),]
delete <- as.data.frame(as.character(delete))


write.csv(delete, file = paste0(dir_path, "/Kiev_Folders_to_delete_final.csv"),row.names = FALSE)