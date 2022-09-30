import os

dir = 'D:/field_08_25_22/color_test/'
counter = 1

for file in os.listdir(dir):
    if file.endswith('.bag'): 
        old_file = dir + file
        new_file = dir + str(counter) + '_color_test.bag'
        os.rename(old_file, new_file)
        print('File #', counter, ' renamed.')
        counter += 1
    else:
        continue