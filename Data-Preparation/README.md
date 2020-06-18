# Data Preparation

This folder contains all notebooks related to the data preparation process. Here is a summary of its contents:

- **[`folder_sort.ipynb`](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/blob/master/Data-Preparation/folder_sort.ipynb)**: notebook that sorts through a directory composed of archived files containing GSV images for a given city, then identifies and deletes files that contain GSV images with coordinates outside the project's area of interest

- **[`csv_sort.ipynb`](https://github.com/Vehicle-detection-for-mode-share/Vehicle-Detection/blob/master/Data-Preparation/csv_sort.ipynb)**: notebook that sorts through a csv file containing coordinates of all archived GSV images for a given city along with the name of their directory, identifies directory names containing GSV images with coordinates within the project's area of interest and exports this list of directory names of interest to the project
