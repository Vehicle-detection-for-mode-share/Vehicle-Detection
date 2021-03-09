import pandas as pd
import geopy.distance
import numpy as np
from os import path
import shutil
import zipfile
import os
import sys


#source_path = 'C:/Users/Kyriaki Kokka/Desktop/'
#dir_del = 'C:/Users/Kyriaki Kokka/Desktop/zip/'
#source_path = '/rds/user/kk704/hpc-work/ElPaso/ElPaso_26701-26868_53225-53397/'

source_path = '/rds/user/kk704/hpc-work/ElPaso/'
dir_del =  '/rds/user/kk704/hpc-work/ElPaso/ElPaso_26701-26868_53225-53397/'


# read in city csv file
city = pd.read_csv(path.join(source_path, "ElPaso_final_locations.csv"))

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

#df.to_csv(path.join(source_path,'new_elpaso_2000sampled_folders.csv'), index=False)


delete = pd.read_csv(path.join(source_path, "Folders_to_delete_final.csv"))
for i in delete["Folder"].tolist():
    os.remove(path.join(dir_del,i))

#Read folder names to extract - sampled locations is the df 
df = pd.read_csv(path.join(source_path, "new_elpaso_2000sampled_folders.csv"))
df2 = df.copy()    

# creating copy
extr = df2.copy()
# creating file paths for extraction
extr['rot1'] = extr.name.astype(str) + '_0_0.jpg'
extr['rot2'] = extr.name.astype(str) + '_90_0.jpg'
extr['rot3'] = extr.name.astype(str) + '_180_0.jpg'
extr['rot4'] = extr.name.astype(str) + '_270_0.jpg'

#Extract images in one folder
for folder in pd.unique(df2["Folder"]).tolist(): 
    archive = zipfile.ZipFile(path.join(source_path, folder))  
    for file in archive.namelist():
        archive.extract(file,path.join(source_path, "images/"))

#delete images with 0_90, 0_270 in the extracted folder
img_dir = path.join(source_path, "images/")
for filename in os.listdir(img_dir):
    filepath = os.path.join(img_dir, filename)
    if filepath.endswith('_270.jpg'):
        os.remove(filepath)
    if filepath.endswith('_90.jpg'):    
        os.remove(filepath)

extr3 = extr.copy()
extr3 = extr3.drop(["Folder","name"],axis = 1)
extr3.lat = str(extr3.lat)
extr3.lon = str(extr3.lon)
files = sorted(extr3.iloc[:, -4:].values.T.ravel().tolist())

#write full image path in txt
with open('new_elpaso_8000sampled_images.txt',"w") as f:
    for item in files:
        f.write("%s\n" % item)

#copy only the 8000 sampled images in "sampled_images" folder        
for f in files:
    shutil.copy(path.join(path.join(source_path, "images/"), f), path.join(source_path, "sampled_images/"))         
