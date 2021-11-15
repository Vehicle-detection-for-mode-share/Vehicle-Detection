import pandas as pd
import geopy.distance
import numpy as np
from os import path
import shutil
import zipfile
import os
import sys

source_path = '/rds/user/kk704/hpc-work/sampling/'
# read in city csv file
#city = pd.read_csv(path.join(source_path, "Telaviv_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Elpaso_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Rome_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Portland_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "SanFrancisco_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Richmond_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Buffalo_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Bonn_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Minneapolis_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Kampala_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Hamburg_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "LosAngeles_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Boston_focused_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Frankfurt_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Bogota_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "CambridgeMass_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Nantes_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Ghent_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "SaltLakeCity_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "SanJose_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Barcelona_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Brussels_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Washington_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Seattle_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Cleveland_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Sofia_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "HongKong_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Johannesburg_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Bucharest_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Belgrade_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Baltimore_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Fresno_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Madrid_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Dublin_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Tucson_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Tampa_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Philadelphia_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Warsaw_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Bangkok_final_locations.csv"))
#city = pd.read_csv(path.join(source_path, "Kiev_final_locations.csv"))
city = pd.read_csv(path.join(source_path, "Santiago_final_locations.csv"))

# extract folder name
#city['Folder'] = city.FileName.str.extract(r'(\d+_\d+)', expand = True)

# extract lat and lon
city['lat'] = city["lat"]
city['lon'] = city["lon"]

# groupby lat and lon
city = city.groupby(['lat', 'lon']).first().reset_index()


citycop = city.copy()

# enter required sample size
sample_size = 2000

city.head()



# create sample 1 within boundaries
df = citycop.sample(n = 1)


# sampling loop
for i in range(sample_size-1):
    # shuffle df
    citycop = citycop.sample(frac=1)
    # resample
    sam = citycop.sample(n = 1)
    
    # condition is for over 100 meters and within city boundaries
    while not(df.apply(lambda row:(geopy.distance.distance((float(row.lat),float(row.lon)),(float(sam.lat),float(sam.lon))).km > 0.1)
                      ,axis=1).all()):
        sam = citycop.sample(n = 1)
    else:
        df = pd.concat([df, sam])


df.to_csv(path.join(source_path,'Santiago_2000sampled_folders.csv'), index = False)

