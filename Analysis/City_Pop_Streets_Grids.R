
#################################Description########################################

# This script is developed to identify built up area along street network in 71 cities
# These cities are selected to extract 
# Google Street view data along these streets and built up areas
# This script use data from OSMnx data source and Global Built Up Layers 
# Main data sources:
# GHSL data: https://ghsl.jrc.ec.europa.eu/datasets.php
# OSMnx data: https://dataverse.harvard.edu/dataverse/global-urban-street-networks

##############################Libraries##########################################
library(sf) # v ‘0.9.6’ 
library(sp) # v ‘1.4.4’
library(rgdal) # v ‘1.5.18’
library(rgeos) 
library(raster)
library(ggmap)

##############################Set Up ##########################################

rm (list = ls())

Globalpath<- "C:/Users/Kyriaki Kokka/Desktop/GSV_GLASST/"

setwd("C:/Users/Kyriaki Kokka/Desktop/GSV_GLASST")

########################## Read data ##########################################

worldpop <- raster("GHS_POP_E2015_GLOBE_R2019A_4326_9ss_V1_0/GHS_POP_E2015_GLOBE_R2019A_4326_9ss_V1_0.tif")
#EPSG 4326
crs(worldpop)

######################### Main operation ######################################


citynames <- read.csv(paste0(Globalpath, "cityfolders_July2021.csv")) #put the csv file with the city name folder

for (cn in 1:length(citynames$citynames)) {
  
  city <- as.character(citynames$citynames[cn])
  
  print(city)
  
  listcityfiles <- list.files(path = paste0(Globalpath, "Cities", "/", city), pattern = "*.gpkg", full.names = TRUE, recursive = TRUE)
  
  for (fl in listcityfiles){
    ctiyroad <- readOGR(fl, layer = 'edges')
    print("success!")
  }
  
  croad <- ctiyroad
  City_built <- raster::crop(worldpop, croad)
  City_built_grids <- rasterToPolygons(City_built, fun=NULL, n=4, na.rm=TRUE, digits=12, dissolve=FALSE)
  CbuitGrid <- st_as_sf (City_built_grids)
  CBR <- raster::intersect(City_built_grids, croad)
  
  print(CBR)
  
  #CBR <- st_intersection (CbuitGrid, croad)
  
  #CBRS <- st_as_sf (CBR)
  
  dsn <- paste0(Globalpath, "CityGrids")
  
  gridname <- paste0(city, "_", "grid")
  
  print (gridname)
  
  writeOGR(CBR, dsn, layer = gridname, driver="ESRI Shapefile", overwrite_layer = TRUE)
  
  
}


#------------------------CODE FOR LARGE CITIES-----------------------------------------


#################################Description########################################

# This script is developed to identify built up area along street network in 71 cities
# These cities are selected to extract 
# Google Street view data along these streets and built up areas
# This script use data from OSMnx data source and Global Built Up Layers 
# Main data sources:
# GHSL data: https://ghsl.jrc.ec.europa.eu/datasets.php
# OSMnx data: https://dataverse.harvard.edu/dataverse/global-urban-street-networks

##############################Libraries##########################################
library(sf) # v ‘0.9.6’ 
library(sp) # v ‘1.4.4’
library(rgdal) # v ‘1.5.18’
library(rgeos) 
library(raster)
library(ggmap)
library(qgisprocess)
options(qgisprocess.path = "path/to/qgis_process")
#"C:/Users/Kyriaki Kokka/AppData/Roaming/Microsoft/Windows/Start Menu/Programsath/to/qgis_process"
#other path "C:/Program Files/QGIS 3.20.3/bin/qgis_process-qgis.bat"
options(qgisprocess.path = "C:/Program Files/QGIS 3.20.3/bin/qgis_process-qgis.bat")
#C:/Users/Kyriaki Kokka/AppData/Roaming/Microsoft/Windows/Start Menu/Programs
qgis_configure()

##############################Set Up ##########################################

rm (list = ls())

Globalpath<- "C:/Users/Kyriaki Kokka/Desktop/GSV_GLASST/"

setwd("C:/Users/Kyriaki Kokka/Desktop/GSV_GLASST")

########################## Read data ##########################################

worldpop <- raster("GLOBE_PoP2015.tif")
#worldpop <- raster("GHS_POP_E2015_GLOBE_R2019A_4326_9ss_V1_0/GHS_POP_E2015_GLOBE_R2019A_4326_9ss_V1_0.tif")
######################### Main operation ######################################


citynames <- read.csv(paste0(Globalpath, "cityfolders_largecities3.csv")) #put the csv file with the city name folder

for (cn in 1:length(citynames$citynames)) {
  
  city <- as.character(citynames$citynames[cn])
  
  print(city)
  
  listcityfiles <- list.files(path = paste0(Globalpath, "Cities", "/", city), pattern = "*.gpkg", full.names = TRUE, recursive = TRUE)
  
  for (fl in listcityfiles){
    ctiyroad <- readOGR(fl, layer = 'edges')
    print("success!")
  }
  
  #if useing rgeos and raster for main operation comment out the following line
  #croad <- ctiyroad
  croad <-st_as_sf(ctiyroad) #use this for for sf object based QGIS operation below
  
  City_built <- crop(worldpop, croad)
  
  City_built_grids <- rasterToPolygons(City_built, fun=NULL, n=4, na.rm=TRUE, digits=12, dissolve=FALSE)
  
  CbuitGrid <- st_as_sf (City_built_grids) #use this for for sf object based QGIS operation below
  
  #This is for smaller cities where the memory issue does not occur, either run this for all cities or two different scripts for small vs large cities
  #CBR <- raster::intersect(City_built_grids, croad)
  
  #This is a QGIS process that allwos extracting grids that intersect with road network
  CBRint <- qgis_run_algorithm(
    "native:extractbylocation",
    INPUT = CbuitGrid,
    INTERSECT = croad,
    PREDICATE = "intersect" # overly operators: "intersect", "contain", "disjoint", "equal", "touch", "overlap", "are within", "cross")
  )
  
  #obtain the QGIS temporary output as sf object
  CBR <- sf::read_sf(qgis_output(CBRint, "OUTPUT"))
  
  #print(CBR)
  
  dsn <- paste0(Globalpath, "CityGrids")
  
  gridname <- paste0(city, "_", "grid")
  
  print (gridname)
  
  #writeOGR(CBR, dsn, layer = gridname, driver="ESRI Shapefile", overwrite_layer = TRUE)
  st_write(CBR, dsn, layer = gridname, driver="ESRI Shapefile", overwrite_layer = TRUE)
  
}


