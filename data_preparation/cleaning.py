# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import libraries
from pathlib import Path
from datetime import datetime
from collections import namedtuple
import pandas as pd

file = namedtuple("file","name path size modified_date") #Create file namedtuple
files,final = [],[] #create empty list
p = Path(r"C:\\Users\\Kyriaki Kokka\\Desktop\\bang\\") #create starting path

#iterate through path objects,store them in a df
for item in p.glob("**/*"):
    if item.suffix in ([".jpg"]):
        name = item.name
        path = Path.resolve(item).parent
        size = item.stat().st_size
        modified = datetime.fromtimestamp(item.stat().st_mtime) 
        files.append(file(name,path,size,modified))

df = pd.DataFrame(files)
df_coord =  df.name.str.split("_", expand=True,)
frames = [df_coord,df]
result = pd.concat(frames,axis = 1)
result.drop(result.columns[[2, 3,6, 7]], axis = 1, inplace = True)
result.drop_duplicates(subset=[0])
result.to_csv("final_locations.csv", index = False)

#Bangkok
# lat = 13.72
# long = 100.53
# dist = 12.89417616

# from functools import partial
# import pyproj
# from shapely.ops import transform
# from shapely.geometry import Point

# proj_wgs84 = pyproj.Proj('+proj=longlat +datum=WGS84')

# aeqd_proj = '+proj=aeqd +lat_0={lat} +lon_0={lon} +x_0=0 +y_0=0'
# project = partial(pyproj.transform,pyproj.Proj(aeqd_proj.format(lat=lat, lon=lon)),proj_wgs84)
# buf = Point(0, 0).buffer(dist * 1000)  # distance in metres
# ret = transform(project, buf).exterior.coords[:]

# # Example
# b = geodesic_point_buffer(centre_x, centre_y, Radius)

# print(b) 