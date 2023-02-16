import os
import moviepy.editor as mp
import moviepy.video.fx.all as vfx

#constants:
original_width = 848
original_height = 480
half_width = original_width/2

#SPECIFY CORRECT FOLDERS
folder = 'E:/farrow_data/DP/'
saving_path = 'E:/farrow_data/DP_R/'

total_files = len(os.listdir(folder))
i=1
for file in os.listdir(folder):
    
    original_clip = mp.VideoFileClip(folder + file)
    left_clip = vfx.crop(original_clip, x1=0, y1=0, width=half_width, height=original_height)
    right_clip = vfx.crop(original_clip, x1=half_width, y1=0, width=half_width, height=original_height)

    left_clip.write_videofile(saving_path + 'RL_' + file, codec='libvpx')
    right_clip.write_videofile(saving_path + 'RR_' + file, codec='libvpx')
    print(str(i) + '/' + str(total_files) + ' from ' + folder + ' saved.')
    i += 1