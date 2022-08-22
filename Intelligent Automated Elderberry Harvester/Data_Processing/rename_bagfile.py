import os

dir = 'D:/field_08_18_22/row4/'
counter = 1

for file in os.listdir(dir):
    old_file = dir + file
    new_file = dir + 'row4_frame' + str(counter) + '.bag'
    os.rename(old_file, new_file)
    counter += 1