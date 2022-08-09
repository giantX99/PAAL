import os

dir = 'C:/Users/gian-/OneDrive/Documentos/PAAL/field_08_08_22/'
counter = 1

for file in os.listdir(dir):
    old_file = dir + file
    new_file = dir + 'row1_frame' + str(counter) + '.bag'
    os.rename(old_file, new_file)
    counter += 1