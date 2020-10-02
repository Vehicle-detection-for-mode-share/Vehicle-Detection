# Import library
import os

path = '/rds/user/kk704/hpc-work/darknetAlexeyAB/Custom-Data/'
os.chdir(path)

a = []
for cdir, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.jpg'):
            path_to_save = path + '/' + f
            a.append(path_to_save + '\n')

# 15% of elements in test.txt file
test = a[:int(len(a) * 0.15)]

# Delete from list 15% of elements
a = a[int(len(a) * 0.15):]

# Create train.txt(85% of lines)
with open('train.txt', 'w') as train_txt:
    for e in a:
        train_txt.write(e)

# Create test.txt(15% of lines)
with open('test.txt', 'w') as test_txt:
    for e in test:
        test_txt.write(e)
