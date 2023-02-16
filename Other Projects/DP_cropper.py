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
saved_frames_path = ''

total_files = len(os.listdir(folder))
i=1
for file in os.listdir(folder):
    try:
        original_clip = mp.VideoFileClip(folder + file)

        #ADJUST FRAMES NAME:
        original_clip.save_frame(saved_frames_path + 'Rfirst_frame_' + file, t=1)
        original_clip.save_frame(saved_frames_path + 'Rlast_frame' + file, t=20)

        left_clip = vfx.crop(original_clip, x1=0, y1=0, width=half_width, height=original_height)
        right_clip = vfx.crop(original_clip, x1=half_width, y1=0, width=half_width, height=original_height)

        #MAKE SURE TO ADJUST FILE NAME FROM RX TO LX:
        left_clip.write_videofile(saving_path + 'RL_' + file, codec='libvpx')
        right_clip.write_videofile(saving_path + 'RR_' + file, codec='libvpx')
        print(str(i) + '/' + str(total_files))
        i += 1
    except KeyboardInterrupt:
        print("LAST CROPPED FILE: ", file)