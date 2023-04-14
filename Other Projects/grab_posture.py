import shutil
import os

#sow = 'RR' #CHANGE THIS ACCORDING WITH SOW

# data_root = "D:/DP_FARROW_CROPPED/R_Cropped/DP_SN/RR/Initial_Frame/"
# data_dirs = [data_root + dirs + '/' for dirs in os.listdir(data_root)]
# data_files = []
# for dir in data_dirs:
#     for file in os.listdir(dir):
#         if file.endswith(".png"):
#             nfile = file.strip(sow + "_frameI_")
#             os.rename(dir + file, dir + nfile)
#             data_files.append(nfile)
#             shutil.move(dir + nfile, data_root + nfile)

data_root = "D:/DP_FARROW_CROPPED/L_Cropped/DP_SN/LR/Initial_Frame/"
data_files = [file for file in os.listdir(data_root) if file.endswith(".png")]


posture_root = "D:/FARROW_POSTURE/6C_LR/"
posture_dirs = [posture_root + dirs + "/" for dirs in os.listdir(posture_root)]
Pfiles_per_dir = [os.listdir(dir) for dir in posture_dirs]


labeled_root = "D:/FARROW_POSTURE/DP_FRAME/6C_LR/"
labeled_dirs = [labeled_root + dir + "/" for dir in os.listdir(labeled_root)]

dir_counter = 0
for dir in Pfiles_per_dir:
    for file in dir:
        file = file.replace('.avi', '.png')
        if file in data_files:
            if file in os.listdir(labeled_dirs[dir_counter]):
                print(file, " already in ", labeled_dirs[dir_counter])
                continue
            else:
                shutil.copy(data_root + file, labeled_dirs[dir_counter] + file)
                print(file, ' now in ', labeled_dirs[dir_counter])
    dir_counter += 1