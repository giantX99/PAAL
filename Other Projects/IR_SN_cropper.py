import os
from PIL import Image

#constants:
x0_L = 0
x1_L = 424
y0 = 0      #upper
y1 = 480    #bottom
x0_R = x1_L
x1_R = 848

folder = 'E:/farrow_data/IR_SN/'
saving_path = 'E:/farrow_data/IR_SN_R/'

total_files = len(os.listdir(folder))
i = 1
for file in os.listdir(folder):
    original_img = Image.open(folder + file)

    left_img = original_img.crop(x0_L, y0, x1_L, y1)
    right_img = original_img.crop(x0_R, y0, x1_R, y1)

    left_img.save(saving_path + 'RL_' + file)
    right_img.save(saving_path + 'RR_' + file)
    print(str(i) + '/' + str(total_files) + ' from ' + folder + ' saved.')
    i += 1