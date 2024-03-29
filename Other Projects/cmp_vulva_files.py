import shutil
import os

annotation_folder = "D:/vulva_annotations/"
data_folder = "E:/PIG_RGB_UNET/"
labeled_folder = "E:/PIG_RGB_UNET/Labeled_Data/"

annot_files = [annotation.split('__')[0] for annotation in os.listdir(annotation_folder)]
file_names = [os.path.splitext(file)[0] for file in os.listdir(data_folder)]
file_names = [name[:-1] for name in file_names] 

labeled_files = [file for file in annot_files + file_names if file in annot_files and file in file_names]

for file in os.listdir(data_folder):
    file_name = os.path.splitext(file)[0]
    file_name = file_name[:-1]
    if file_name in labeled_files:
        print("\n", file, " moved to ", labeled_folder, "\n")
        shutil.move(data_folder + file, labeled_folder + file)
        continue
    else:
        print("No match for ", file)
        continue