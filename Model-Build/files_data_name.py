# Create labelled_data.data and classes.names

full_path_to_images = '/rds/user/kk704/hpc-work/darknetAlexeyAB/Custom-Data/'

c = 0
# Create classes.names from classes.txt
with open(full_path_to_images + '/' + 'classes.names', 'w') as names, \
     open(full_path_to_images + '/' + 'classes.txt', 'r') as txt:
     for line in txt:
         names.write(line) 
         c += 1  

# Create labelled_data.data
with open(full_path_to_images + '/' + 'labelled_data.data', 'w') as data:
    data.write('classes = ' + str(c) + '\n')
    data.write('train = ' + full_path_to_images + '/' + 'train.txt' + '\n')
    data.write('valid = ' + full_path_to_images + '/' + 'test.txt' + '\n')
    data.write('names = ' + full_path_to_images + '/' + 'classes.names' + '\n')
    data.write('backup = backup')


