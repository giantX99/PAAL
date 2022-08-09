import pyrealsense2 as rs
import numpy as np
import cv2
import os

dir_path = 'D:/field_08_08_22/'
rgb_path = 'rgb_extracted_field_08_08_22/'
counter = 1
rgb_file_name = rgb_path + 'row1_rgb_' + str(counter) + '.png'

for bag_file in os.listdir(dir_path):
    
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device_from_file(bag_file, repeat_playback=False)
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 6)

    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            #depth_frame = frames.get_depth_frame()
            rgb_frame = frames.get_color_frame()
            if not rgb_frame : #or not depth_frame :
                print('Could not process image')
                continue
            
            rgb_img = np.asanyarray(rgb_frame.get_data())
            rgb_flipped = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
            cv2.imwrite(rgb_file_name, rgb_flipped) #cv2 uses bgr instead of rgb
            counter += 1
            break
    finally:
        pipeline.stop()
