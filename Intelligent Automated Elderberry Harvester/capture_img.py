import pyrealsense2 as rs
import numpy as np
import cv2
import my_globals

# Set up
pipeline = rs.pipeline()
config = rs.config()
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

# Enable stream
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming with config configurations
pipeline.start(config)

path = 'C:/Users/gian-/OneDrive/Documentos/PAAL/data/{}'
rgb_file_name = 'color_test_{}.png' 
depth_file_name = 'depth_test_{}.png'

try:
    '''
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    rgb_frame = frames.get_color_frame()
    depth_map = np.asanyarray(depth_frame.get_data())
    rgb_img = np.asanyarray(rgb_frame.get_data())

    print('depth frame type: ', type(depth_frame))
    print('depth data type: ', type(depth_frame.get_data()))
    print('depth map type: ', type(depth_map))
    print('rgb frame type: ', type(rgb_frame))
    print('rgb data type: ', type(rgb_frame.get_data()))
    print('rgb image type: ', type(rgb_img))
    print('\ndepth map array:\n', depth_map)
    '''
    while True:
        # Get frames
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        rgb_frame = frames.get_color_frame()
        if not depth_frame or not rgb_frame:
            print('Could not process image')

        # Transforming data into numpy array
        depth_img = np.asanyarray(depth_frame.get_data())
        rgb_img = np.asanyarray(rgb_frame.get_data())
        # Convert depth image to 8-bit per pixel
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha=0.03), cv2.COLORMAP_JET)

        # If depth and color resolutions are different, resize color image to match depth image for display
        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = rgb_img.shape
        if depth_colormap_dim != color_colormap_dim:
            resized_rgb_img = cv2.resize(rgb_img, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_rgb_img, depth_colormap))
        else:
            images = np.hstack((rgb_img, depth_colormap))

        # Show real time frames
        cv2.namedWindow('Press "c" to capture images or ESC to exit', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('Press "c" to capture images or ESC to exit', images)

        key = cv2.waitKey(1)
        # Save image if c is pressed
        if key == 99: # key 99 = 'c'
            my_globals.num_of_files += 1
            cv2.imwrite(path.format(rgb_file_name.format(my_globals.num_of_files)), rgb_img)
            cv2.imwrite(path.format(depth_file_name.format(my_globals.num_of_files)), depth_colormap)
        # Exit program
        if key == 27: # key 27 = 'ESC'
            break
    
finally:
    # Stop stream
    pipeline.stop()
    