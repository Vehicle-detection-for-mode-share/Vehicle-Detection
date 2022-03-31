#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import the packages
import networkx as nx # networkx package
import osmnx as ox
import pandas as pd #Base package for data analysis and manipulation
import geopandas as gpd #A more flexible package to work with geospatial data in python
import shapely.geometry #python package for basic spatial operation
from osgeo import ogr #GDAL package
from pyproj import CRS #package for your projection management
import requests #Google Street View 
from pathlib import Path #Path modification package
import os #operating system package

import matplotlib.pyplot as plt #package for plotting

#configure in notebook
get_ipython().run_line_magic('matplotlib', 'inline')
#print the version
ox.__version__ 


# In[2]:


#city = 'Abuja'
city = 'Enugu'
#city = 'Mombasa'
#city = 'Arica'
#city = 'Kisumu'
#city = 'Helsinki'
#city = 'San Miguel de Tucuman'
#city = 'Cordoba'
#city = 'Vienna'


# In[3]:


source_path = 'C:/Users/Kyriaki Kokka/Desktop/newImages/'
#path for maps
directory = source_path + 'maps/'
#directory = source_path 
#path for 2200 locations metadata 
loc_path = 'C:/Users/Kyriaki Kokka/Desktop/newImages/' + '2200locations' + city + '.csv'
#path for images
path = source_path + city + '/'
#path for metadata
cityname = source_path + 'Metadata/' + city + '.csv'


# In[4]:


#Read excel file as panda data frame (need openpyxl dependency)
#list of cities to download
citynames = pd.read_excel('C:/Users/Kyriaki Kokka/Desktop/cities.xlsx')
pd.set_option('display.max_rows', 500)
#citynames


# In[5]:


#Automation
#Read city names out of excel file in order to get city names
#Store within list to be able to iterate

#Specify which cities to be extracted from pd df
#name= citynames.loc[72:80]['city']
name = citynames.loc[0:0]['city']
#name = citynames["city"]

citynames_l = name.tolist()

#Checking working directory and creating path
#maybe specify the location
#directory = os.getcwd() #use working directory or desired location
connect = "/"
print(name)


# In[9]:


#city = 'San Miguel de Tucuman'
#city = 'Arica'
city = 'Mombasa'
gdf1 = ox.geocode_to_gdf(city)
gdf1.plot()


# In[6]:


#get maps based on road network
for city in citynames_l:
    folder = city
    path = directory + connect + folder

    if not os.path.exists(path):
        os.makedirs(path)
    else:
        continue
    
    os.chdir(path)
    
    # download/model a street network for some city
    G = ox.graph_from_place(city, network_type = "drive")
  
    
    # Retrieve only edges from the graph
    nodes_proj, edges = ox.graph_to_gdfs(G, nodes = True, edges = True)
    
    #Get the bounding box of all the edges, this will be the are of interest for each city
    #convex_hull = edges.unary_union.convex_hull
    bbox_env = edges.unary_union.envelope
    
    #Saving this bbox to your folder
    poly = bbox_env

    # Now convert it to a shapefile with OGR    [Copied from one post in Stake Exchange]
    driver = ogr.GetDriverByName('ESRI Shapefile') #for ESRI shapefile
    ds = driver.CreateDataSource('citybound.shp') #Name of the file 
    layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    # Add one attribute
    layer.CreateField(ogr.FieldDefn('id', ogr.OFTString))
    defn = layer.GetLayerDefn()

    # Create a new feature (attribute and geometry)
    feat = ogr.Feature(defn)
    feat.SetField('id', city)

    # Make a geometry, from Shapely object
    geom = ogr.CreateGeometryFromWkb(poly.wkb)
    feat.SetGeometry(geom)

    layer.CreateFeature(feat)
    feat = geom = None 

    ds = layer = feat = geom = None

    #Re-project the saved bounding box
    bboxnprj = gpd.read_file('citybound.shp')
    # define crs for the shapefile
    bboxprj = bboxnprj.set_crs(epsg = 4326)
    # write shp file
    bboxprj.to_file('citybound_WGS84.shp')

    #Save the graph to your directory as geopackage
    ox.save_graph_geopackage(G, "network.gpkg")

    #Save the graph to your directory as graphml file, this is a graph file that can be used later for other works
    ox.io.save_graphml (G, "network.graphml") 
    
    print(city + " is finished")


# In[2]:


##if the above code fails, run this to check the network
#place = "Amsterdam, Netherlands"
#G = ox.graph_from_place(place, network_type = "drive")


# In[60]:


graph = ox.graph_from_place('Abuja Federal Capital Territory', network_type = 'drive')
fig, ax = ox.plot_graph(graph)


# In[ ]:


#cf = '["highway"~"motorway|motorway_link|trunk|trunk_link"]'
#cf = '["highway"~"tertiary"]'
#cf = '["highway"~"residential"]'
#cf = '["highway"~"secondary"]'
cf = '["highway"~"primary"]'
G = ox.graph_from_place('Abuja Federal Capital Territory', network_type = "drive", custom_filter = cf)
fig, ax = ox.plot_graph(G, node_size = 0)


# In[7]:


#sample 2200 locations
points = ox.utils_geo.sample_points(ox.get_undirected(G), 2200)
#points
df = gpd.GeoDataFrame(geometry = points, crs = 'epsg:4326')
#df = gpd.GeoSeries(points, crs = 'epsg:4326')
#gdf.crs = G_proj.graph['crs']
df = ox.project_gdf(df, to_latlong = True)

#clean df
df[['c1', 'c2']] = df['geometry'].astype(str).str.split('(', 1, expand = True)
df[['lat', 'long']] = df['c2'].astype(str).str.split(' ', 1, expand = True)
df[['lon','c3']] = df['long'].astype(str).str.split(')', 1, expand = True)

# drop by Name
df = df[['lat','lon']]

sampling_path = 'C:/Users/Kyriaki Kokka/Desktop/newImages/' + '2200locations/' + city + '_sampling.csv'
df.to_csv(sampling_path) 


# In[8]:


#GOOGLE STREET VIEW
meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
#don't share api_key with anyone
api_key = 

import json

df5 = pd.DataFrame(columns = ['copyright','date','location.lat','location.lng','pano_id','status'])

#check google metadata if the images exist in the 2200 selected locations
for i in range(len(df)):
    location = str(df.iloc[i].lon) + ', ' + str(df.iloc[i].lat)
    meta_params = {'key': api_key,'location': location}
    meta_response = requests.get(meta_base, params = meta_params)
    json_string = meta_response.json()
    dataframe = pd.json_normalize(json_string)
    df5.loc[i] = dataframe.loc[0]
loc_path = 'C:/Users/Kyriaki Kokka/Desktop/newImages/' + '2200locations/' + city + '.csv'
df5.to_csv(loc_path)  


# In[99]:





# In[78]:


#keep locations with status "OK" and copyright from Google
df5 = df5[df5.status == 'OK']
df5 = df5[df5.copyright == '© Google']
print(len(df5))
#random sampling to get 2000 loc
final_df = df5.sample(n = 20)
final_df = final_df.rename(columns={"location.lng": "lng", "location.lat": "lat"})

final_df.to_csv(cityname)


# In[81]:


#TRY-WORKS WELL
df7 = pd.read_csv(cityname)


for i in range(len(df7)):
    #0_0
    location = str(df7.lat[i]) + ',' + str(df7.lng[i])
    image_name = path + str(df7.lat[i]) + '_' + str(df7.lng[i])+ '_0_0.jpg'
    pic_params = {'key': api_key,'location': location,'size': "640x640", 'heading': 0}
    pic_response = requests.get(pic_base, params = pic_params)
    with open(image_name, 'wb') as file:
        file.write(pic_response.content)
    # remember to close the response connection to the API
    pic_response.close()
    
    #90_0
    location = str(df7.lat[i]) + ',' + str(df7.lng[i])
    image_name = path + str(df7.lat[i]) + '_' + str(df7.lng[i])+ '_90_0.jpg'
    pic_params = {'key': api_key,'location': location,'size': "640x640", 'heading': 90}
    pic_response = requests.get(pic_base, params = pic_params)
    with open(image_name, 'wb') as file:
        file.write(pic_response.content)
    # remember to close the response connection to the API
    pic_response.close()
    
    #180_0
    location = str(df7.lat[i]) + ',' + str(df7.lng[i])
    image_name = path + str(df7.lat[i]) + '_' + str(df7.lng[i])+ '_180_0.jpg'
    pic_params = {'key': api_key,'location': location,'size': "640x640", 'heading': 180}
    pic_response = requests.get(pic_base, params = pic_params)
    with open(image_name, 'wb') as file:
        file.write(pic_response.content)
    # remember to close the response connection to the API
    pic_response.close()
    
    #270_0
    location = str(df7.lat[i]) + ',' + str(df7.lng[i])
    image_name = path + str(df7.lat[i]) + '_' + str(df7.lng[i])+ '_270_0.jpg'
    pic_params = {'key': api_key,'location': location,'size': "640x640", 'heading': 270}
    pic_response = requests.get(pic_base, params = pic_params)
    with open(image_name, 'wb') as file:
        file.write(pic_response.content)
    # remember to close the response connection to the API
    pic_response.close()
    
    
#End of code
