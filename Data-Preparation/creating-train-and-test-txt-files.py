import os

full_path_to_images = '/rds/user/kk704/hpc-work/CITIES/SanFrancisco/final_images/'

os.chdir(full_path_to_images)
p = []

for current_dir, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.jpg'):
            path_to_save_into_txt_files = full_path_to_images + '/' + f
            p.append(path_to_save_into_txt_files + '\n')

p_test = p[:int(len(p))]

with open('/rds/user/kk704/hpc-work/YOLOv4/darknet/data/SanFrancisco_images.txt', 'w') as test_txt:
    for e in p_test:
        test_txt.write(e)
