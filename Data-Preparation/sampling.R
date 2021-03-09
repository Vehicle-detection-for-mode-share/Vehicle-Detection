library(osmdata)
library(sf)
library(tidyverse)
library(ggmap)

library(rgdal)
library(leaflet)
library(tidyverse)
library(rgeos)
library(raster)
library(ggplot2)
library(sf)
library(mapview)
library(maptools)
library(sp)
library(readxl)
library(readr)
library(grid)
library(gridExtra)
library(xtable)
library(knitr)
library(plyr)


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


clean_data <-function(data){
  #data <- data[,-c(2,4)]
  #data <- data[,-c(2)]
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

gdb_path <- "C://Users//Kyriaki Kokka//Desktop//CityGrids"
el_paso <- readOGR(dsn = gdb_path,layer="Elpaso_grid", verbose = FALSE)
#Transform to long/lat
el_paso <- spTransform(el_paso, "+init=epsg:4326")
#leaflet(el_paso) %>% addTiles() %>% addPolygons()

dir_path <- "C://Users//Kyriaki Kokka//Desktop"
#elpaso_df <- read.table(paste0(dir_path, "/elpaso_2000sampled_locations.csv"),stringsAsFactors = FALSE)
elpaso_df <- read.csv(paste0(dir_path, "/El_Paso.csv"),stringsAsFactors = FALSE)

elpaso_copy <- clean_data(elpaso_df)
elpaso_df <- unique(elpaso_copy[,-c(4,5)])

#el1 <- elpaso_df[1:300000,]
#el2 <- elpaso_df[300001:600000,]
#el3 <- elpaso_df[600001:930176,]

#elpaso_df$lat <- as.character(elpaso_df$lat)
#elpaso_df$lon <- as.character(elpaso_df$lon)


#a1 <- intersect_data(el1[1:100000,],el_paso)
#a2 <- intersect_data(el1[100001:150000,],el_paso)
#a3 <- intersect_data(el1[150001:200000,],el_paso)
#a4 <- intersect_data(el1[200001:300000,],el_paso)

#a5 <- intersect_data(el2[1:80000,],el_paso)
#a6 <- intersect_data(el2[80001:120000,],el_paso)
#a7 <- intersect_data(el2[120001:200000,],el_paso)
#a8 <- intersect_data(el2[200001:250000,],el_paso)
#a9 <- intersect_data(el2[250001:300000,],el_paso)

#a10 <- intersect_data(el3[1:80000,],el_paso)
#a11 <- intersect_data(el3[80001:120000,],el_paso)
#a12 <- intersect_data(el3[120001:200000,],el_paso)
#a13 <- intersect_data(el3[200001:250000,],el_paso)
#a14 <- intersect_data(el3[250001:300000,],el_paso)


#sum(nrow(a1),nrow(a2),nrow(a3),nrow(a4))
#sum(nrow(a5),nrow(a6),nrow(a7),nrow(a8),nrow(a9))
#sum(nrow(a10),nrow(a11),nrow(a12),nrow(a13),nrow(a14))


final <- rbind(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14)
final$lat <- as.numeric(final$lat)
final$lon <- as.numeric(final$lon)

final$lat <- (format(final$lat, digits=16))
final$lon <- (format(final$lon, digits=16))

final$name <- paste(final$lat,final$lon,sep="_")

write.csv(final[,-c(4)], file = paste0(dir_path, "/Elpaso_final_locations.csv"),row.names=FALSE)


finalb <- unique(as.data.frame(final[,-c(2,3,4)]))
#cat(finalb, file = "uniquefolder_keep.txt")


all_folders <- unique(as.data.frame(elpaso_df[,-c(2:3)]))

#folders that are only in "all_folders and not in finalb"
delete <- all_folders[!(all_folders$`elpaso_df[, -c(2:3)]` %in% finalb$`final[, -c(2, 3, 4)]` ),]
delete <- as.data.frame(as.character(delete))


write.csv(delete, file = paste0(dir_path, "/Folders_to_delete_final.csv"),row.names=FALSE)

dir_path <- "C://Users//Kyriaki Kokka//Desktop"
df <- read_csv(paste0(dir_path, "//new_elpaso_2000sampled_locations.csv"))

leaflet(el_paso) %>% addTiles() %>% addPolygons() %>% addCircleMarkers(lng = df$lon , lat = df$lat, color = "red" , radius = 2, stroke = FALSE, fillOpacity = 0.5)