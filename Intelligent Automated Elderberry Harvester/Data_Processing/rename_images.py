import os

dir = 'D:/field_08_25_22/rgb_extracted/'
counter = 1

for file in os.listdir(dir):
    if file.endswith('.jpg'): 
        old_file = dir + file
        new_file = dir + 'row5_rgb_' + str(counter) + '.jpg'
        os.rename(old_file, new_file)
        print('File #', counter, ' renamed.')
        counter += 1
    else:
        continue
