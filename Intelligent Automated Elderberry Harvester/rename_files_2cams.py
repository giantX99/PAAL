import os

dir = 'C:/Users/gian-/OneDrive/Documentos/PAAL/data/test/'
saving_count = 1
counter = 1

for file in os.listdir(dir):
    
    old_file = dir + file

    if counter % 2 == 0 : 
        new_file = dir + 'pcd_data_' + str(saving_count) + '_cam2.pcd'
        saving_count +=1
    else:
        new_file = dir + 'pcd_data_' + str(saving_count) + '_cam1.pcd'

    os.rename(old_file, new_file)
    counter += 1
