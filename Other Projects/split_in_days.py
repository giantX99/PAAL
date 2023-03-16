import shutil
import os

root_folder = "D:/DP_FARROW_CROPPED/R_Cropped/DP_CROPPED/RL/"
root_file = "RL_202211"

Day_folders = []
[Day_folders.append(root_folder + "Day_" + str(i) + "/") for i in range(16,27)]

Day_files = []
[Day_files.append(root_file + str(i)) for i in range(16,27)]

for file in os.listdir(root_folder):
    if file.endswith('.avi'):
        for day in range(10):
            if file.startswith(Day_files[day]):
                shutil.move(root_folder + file, Day_folders[day] + file)
                print(file, "moved to", Day_folders[day])
            else:
                continue
    else:
        continue
