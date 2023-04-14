#1st ADD vulva AND tail
#2nd CROP image from 640x480 to 480x480
import os
from PIL import Image
import numpy as np

main_root = 'D:/Code_Run/'

list_of_roots = [main_root + folder + '/' for folder in os.listdir(main_root) if folder.startswith('VULVA_DETECT_')]

saving_root = 'D:/Vulva_Mask/'
vulva_suffix = "__v.ome.tiff"
tail_suffix = "__t.ome.tiff"
vt_suffix = "__v_t.ome.tiff"


for root in list_of_roots:

    vulva_files = []
    tail_files = []
    one_label_files =[]

    for file in os.listdir(root):
        if file.endswith(vulva_suffix):
            vulva_files.append(file)
        if file.endswith(tail_suffix):
            tail_files.append(file)
    vulva_files.sort()
    tail_files.sort()

    for v in vulva_files:
        t_file = v.split('__')[0] + tail_suffix
        if t_file in tail_files:
            continue
        else:
            one_label_files.append(v)
            vulva_files.remove(v)
    for t in tail_files:
        v_file = t.split('__')[0] + vulva_suffix
        if v_file in vulva_files:
            continue
        else:
            one_label_files.append(t)
            tail_files.remove(t)

    print('Folder: ', root)
    print('# of files without vulva or tail annotation: ', len(one_label_files))

    for v, t in zip(vulva_files, tail_files):
        
        raw_mask_vulva = Image.open(root + v)
        raw_mask_vulva = np.asarray(raw_mask_vulva)
        
        raw_mask_tail = Image.open(root + t)
        raw_mask_tail = np.asarray(raw_mask_tail)

        mask = raw_mask_vulva + raw_mask_tail
        Image.fromarray(mask).save(saving_root + v.split('__')[0] + vt_suffix)
    print('Number of masks created from ', root, ': ', len(vulva_files))

