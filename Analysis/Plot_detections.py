#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import libraries
import os
import cv2
import csv
import shutil
import numpy as np
import pandas as pd
from os import path


# In[ ]:


#PREPARE DETECTIONS CSV FILE


# In[9]:


#Convert txt to csv
item = 'C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BaltimoreImagesA.txt'
item2 = 'C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BaltimoreImagesA.csv'

with open(item, 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open(item2, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('name', 'labels','bboxs'))
        writer.writerows(lines)        


# In[10]:


#read csv file
df = pd.read_csv('C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BaltimoreImagesA.csv',skip_blank_lines=True)


# In[11]:


#TRY TO READ TXT LINE BY LINE AND PUT THEM ON CSV FILE- CORRECT COLUMN
L = ["m", "c","p","r"]
df["label"] = df.loc[df['name'].str.startswith(tuple(L)), 'name']
df.loc[:, 'label'] = df.label.shift(-1)

#M = ["(0."] for Kampala
M = ["0."]
df["bboxs"] = df.loc[df['name'].str.startswith(tuple(M)), 'name']
df.loc[:, 'bboxs'] = df.bboxs.shift(-2)

df[['name', 'time']] = df['name'].str.split(':', 1, expand=True)
#df[['label', 'info']] = df['labels'].str.split('(', 1, expand=True)

df[['x', 'y','w','h']] = df['bboxs'].str.split( expand=True)


# In[6]:


#print(df)


# In[12]:


df = df[["name","label","bboxs","x","y","w","h"]]
df.to_csv("C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BaltimoreImagesA.csv")


# In[ ]:


#READ DETECTIONS CSV FILE AND PLOT THEM


# In[11]:


#read detection csv output file with correct columns format
#IMPORTANT: Manually fix format and save as ***_PRO.csv

df2 = pd.read_csv("C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BaltimoreImagesA_PRO.csv")
#delete NA
df2.dropna(subset = ['bboxs'], inplace=True)

df2.to_csv("C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BaltimoreImagesA_PRO2.csv")


# In[12]:


df2 = pd.read_csv("C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BogotaImagesA_PRO2.csv")
df2.dropna(subset = ['bboxs'], inplace=True)
source_path = 'C:/Users/Kyriaki Kokka/Desktop/final_Bogota/'


#Create folder "detections"


#Copy detection images in a new file in order to prepare them for plots
for i in df2["name"].T.ravel().tolist():
    shutil.copy(os.path.join(source_path,i),os.path.join(source_path,'detections')) 


# In[15]:


#print(df2)
df2 = pd.read_csv("C:/Users/Kyriaki Kokka/Desktop/CSV_clean_cities/BogotaImagesA_PRO2.csv")
df2.dropna(subset = ['bboxs'], inplace=True)


# In[16]:


save_path = 'C:/Users/Kyriaki Kokka/Desktop/final_Bogota/detections/' 


#Read images from the new directory and create plots
j= 0
for i in df2["name"].T.ravel().tolist():
    img = cv2.imread(os.path.join(save_path,i))
    label = df2.iloc[j].label
    x = df2.iloc[j].x
    y = df2.iloc[j].y
    w = df2.iloc[j].w
    h = df2.iloc[j].h
    
    dh, dw, _ = img.shape
    
    l = int((x - w / 2) * dw)
    r = int((x + w / 2) * dw)
    t = int((y - h / 2) * dh)
    b = int((y + h / 2) * dh)
     
    if l < 0:
        l = 0
    if r > dw - 1:
        r = dw - 1
    if t < 0:
        t = 0
    if b > dh - 1:
        b = dh - 1
    
    j = j+1

    cv2.rectangle(img, (l, t), (r, b), (255,192,203), 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str(label), (l, t), font, 0.6, (255,192,203), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(save_path,i),img)    


# In[257]:


#SAVE plots based on predicted label

#save_path = 'C:/Users/Kyriaki Kokka/Desktop/final_TelAviv/detections/pedal/' 
save_path = 'C:/Users/Kyriaki Kokka/Desktop/final_TelAviv/detections/' 

#Read images from the new directory and create plots
j= 0
for i in df2["name"].T.ravel().tolist():
    #if df2["label"].tolist().startswith(["p"]):
    #if df2.loc[df2['label'].str.startswith(tuple("p")), 'label']== True :
        img = cv2.imread(os.path.join(save_path,i))
        label = df2.iloc[j].label
        x = df2.iloc[j].x
        y = df2.iloc[j].y
        w = df2.iloc[j].w
        h = df2.iloc[j].h
    
        dh, dw, _ = img.shape
    
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)
     
        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1
    
        j = j+1

        cv2.rectangle(img, (l, t), (r, b), (255,192,203), 1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(label), (l, t), font, 0.6, (255,192,203), 2, cv2.LINE_AA)
        cv2.imwrite(os.path.join(save_path,i),img) 


# In[198]:


label = df2.iloc[1].label
print(label)


# In[ ]:





# In[ ]:





# In[2]:


##Correct
from os import path
source_path = 'C:/Users/Kyriaki Kokka/Desktop/final_TelAviv/'
image_path = '32.13277565977162_34.848080742860475_270_0.jpg'
img = cv2.imread(path.join(source_path,image_path))
#img = cv2.resize(img, (608, 608))#depending the hyper parameters

label = 'pedal: 48%'
x = 0.624539
y = 0.629882
w = 0.095061
h = 0.171269
          
dh, dw, _ = img.shape
    
l = int((x - w / 2) * dw)
r = int((x + w / 2) * dw)
t = int((y - h / 2) * dh)
b = int((y + h / 2) * dh)
    
if l < 0:
    l = 0
if r > dw - 1:
    r = dw - 1
if t < 0:
    t = 0
if b > dh - 1:
    b = dh - 1
    
save_path = 'C:/Users/Kyriaki Kokka/Desktop/final_TelAviv/detections/'    


# In[4]:


#pedal
cv2.rectangle(img, (l, t), (r, b), (255, 51, 153), 1)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, label, (l, t), font, 0.8, (255,192,203), 2, cv2.LINE_AA)
cv2.imwrite(path.join(save_path,image_path),img)


# In[36]:


#motor
cv2.rectangle(img, (l, t), (r, b), (255,192,203), 1)
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, label, (l, t), font, 0.8, (255,192,203), 2, cv2.LINE_AA)
cv2.imwrite(path.join(save_path,image_path),img)


# In[ ]:


#rickshaw
cv2.rectangle(img, (l, t), (r, b), (0,255,0), 1)
cv2.putText(img, label, (l, t), font, 0.8, (255,192,203), 2, cv2.LINE_AA)
cv2.imwrite(path.join(save_path,image_path),img)


# In[ ]:


#cargo
cv2.rectangle(img, (l, t), (r, b), (255,255,0), 1)
cv2.putText(img, label, (l, t), font, 0.8, (255,192,203), 2, cv2.LINE_AA)
cv2.imwrite(path.join(save_path,image_path),img)


# In[ ]:


#Dokimazontas kwdika
#Read images from the new directory and create plots
for i in df2["name"].T.ravel().tolist():
    img = cv2.imread(path.join(source_path,i))
    label = df2[name == i].label
    x = 
    y =
    w = 
    h = 
    
    dh, dw, _ = img.shape
    
    int((x - w / 2) * dw)
r = int((x + w / 2) * dw)
t = int((y - h / 2) * dh)
b = int((y + h / 2) * dh)
    
if l < 0:
    l = 0
if r > dw - 1:
    r = dw - 1
if t < 0:
    t = 0
if b > dh - 1:
    b = dh - 1


# In[ ]:


#Read images
for row, col in df.iterrows():
    if df.loc[df[row+1].str.startswith(tuple(L))]:
        df[labels]


# In[ ]:


for i in df2["name"].T.ravel().tolist():
    #img = cv2.imread(os.path.join(source_path,i))
    #label = df2['label'].where(df2['name'] == i)
    ##label = df2.loc[df2.name==i].iteritems()
    ##label = df2.loc[df2.name==i].index.values
    label = df2.loc[df2.name==i].label.tolist()
    #label = list(label)
    
print(label[0])

