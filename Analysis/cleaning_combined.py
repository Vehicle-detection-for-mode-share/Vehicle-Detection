import pandas as pd
import numpy as np
from os import path
import shutil
import zipfile
import os
import sys

source_path = '/rds/user/kk704/hpc-work/CITIES/Belgrade/'
dir_del =  '/rds/user/kk704/hpc-work/CITIES/Belgrade/Belgrade_dir/'



df = pd.read_csv(path.join(source_path, "Belgrade_2000sampled_folders.csv"))

#df = pd.read_csv(path.join(source_path, "detections.csv"))

df2 = df.copy()


##Extract images in one folder
##maybe create a file in ELpaso, so source path ends in ELPAso
#for folder in pd.unique(df2["Folder"]).tolist(): 
#    archive = zipfile.ZipFile(path.join(dir_del, folder))  
#    for file in archive.namelist():
#        archive.extract(file,path.join(dir_del, "images/"))
        
##delete images with 0_90, 0_270 in the extracted folder
#img_dir = path.join(dir_del, "images/")
#for filename in os.listdir(img_dir):
#    filepath = os.path.join(img_dir, filename)
#    if filepath.endswith('_270.jpg'):
#        os.remove(filepath)
#    if filepath.endswith('_90.jpg'):    
#        os.remove(filepath)        


# creating copy for extraction purposes
#extr = df2.copy()

# creating file paths for extraction
#extr['rot1'] = extr.name.astype(str) + '_0_0.jpg'
#extr['rot2'] = extr.name.astype(str) + '_90_0.jpg'
#extr['rot3'] = extr.name.astype(str) + '_180_0.jpg'
#extr['rot4'] = extr.name.astype(str) + '_270_0.jpg'


#copy only sampled images in the folder "sampled_images        
#extr3 = extr.copy()
#extr3 = extr3.drop(["Folder","name"],axis = 1)
#extr3.lat = str(extr3.lat)
#extr3.lon = str(extr3.lon)

#source = path.join(source_path, "images/")
#destination = path.join(source_path, "sampled_images/")
#files = sorted(extr.iloc[:, -4:].values.T.ravel().tolist())
##files = sorted(extr3.iloc[:, :].values.T.ravel().tolist())
#files =  sorted(extr.values.T.ravel().tolist())  
        
#for f in files:
#    try:
#        shutil.copy(path.join(path.join(source_path, "final_images/"), f), path.join(source_path, "sampled_images/"))
#    except FileNotFoundError as not_found:
#        print('CANNOT FIND: ', not_found.filename)


#df2.Folder = str(df2.Folder)
#for folder in pd.unique(df["Folder"]).tolist(): 
#    archive = zipfile.ZipFile(path.join(dir_del, folder))
#print("No error in opening zipped folders")

for folder in pd.unique(df2["Folder"]).tolist():
    print(folder)
#for folder in df2["Folder"].tolist(): 
    archive = zipfile.ZipFile(path.join(dir_del, folder)) 
    for files in archive.namelist():
        img = df2.loc[df2['Folder'] == folder, 'name']
        for image in img.tolist():
            if files.startswith(str(image)):
               archive.extract(files,path.join(source_path, "final_images/"))



#def fixBadZipfile(zipFile):  
# f = open(zipFile, 'r+b')  
# data = f.read()  
# pos = data.find(dir_del) # End of central directory signature  
# if (pos > 0):  
#     self._log("Trancating file at location " + str(pos + 22)+ ".")  
#     f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
#     f.truncate()  
#     f.close()  
# else:  
     # raise error, file is truncated
#     print(f)

#for folder in pd.unique(df2["Folder"]).tolist(): 
    #archive = zipfile.ZipFile(path.join(dir_del, folder))  
#    fix = fixBadZipfile(path.join(dir_del, folder))


#delete images with 0_90, 0_270 in the extracted folder "images"
img_dir = path.join(source_path, "final_images/")
for filename in os.listdir(img_dir):
    filepath = os.path.join(img_dir, filename)
    if filepath.endswith('_270.jpg'):
        os.remove(filepath)
    if filepath.endswith('_90.jpg'):    
        os.remove(filepath)    
           
    
print("done")
