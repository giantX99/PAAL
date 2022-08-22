import pyrealsense2 as rs
import numpy as np
import cv2

def extract_rgb_from_bag(bag_file, rgb_file_name):   
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device_from_file(bag_file)
    #pipe_wrapper = rs.pipeline_wrapper(pipeline)
    #pipe_profile = config.resolve(pipe_wrapper)
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 6)
    pipeline.start(config)
    #playback = pipe_profile.get_device().as_playback()
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
        print(rgb_file_name, ' saved.')
        break
    pipeline.stop()

bag_path = 'D:/field_08_18_22/row4/'
rgb_path = 'D:/field_08_18_22/rgb_extracted/'
total_frames = 245

for counter in range(1, total_frames+1):
    bag_file = bag_path + 'row4_frame' + str(counter) + '.bag'
    rgb_file_name = rgb_path + 'row4_rgb_' + str(counter) + '.jpg'
    extract_rgb_from_bag(bag_file, rgb_file_name)