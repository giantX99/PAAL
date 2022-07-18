#TO HAVE A DOUBLE STREAM USB-3.0 IS NECESSARY!

import pyrealsense2 as rs
import numpy as np
import cv2

serial_num_1 = '203522252121' # Old camera d455 yellow 203522252121
serial_num_2 = '213522252513' # New camera d455 green 213522252513

# camera 1:
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, rs.format.z16, 30)
config_cam1.enable_stream(rs.stream.color, rs.format.bgr8, 30)

# camera 2:
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_stream(rs.stream.depth, rs.format.z16, 30)
config_cam2.enable_stream(rs.stream.color, rs.format.bgr8, 30)

# start both camera streams:
pipe_cam1.start(config_cam1)
pipe_cam2.start(config_cam2)


#i = 1
try:
    while True:
        #print('cycle number = %d' %(i))
        #i += 1

        # Camera 1:
        # Wait for a coherent pair of frames: depth and color
        frames_1 = pipe_cam1.wait_for_frames()
        depth_frame_1 = frames_1.get_depth_frame()
        color_frame_1 = frames_1.get_color_frame()
        # Convert images to numpy arrays
        depth_img1 = np.asanyarray(depth_frame_1.get_data())
        color_img1 = np.asanyarray(color_frame_1.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_img1, alpha=0.03), cv2.COLORMAP_JET)
        
        # Stack all images 1 horizontally
        depth_colormap1_dim = depth_colormap_1.shape
        color_colormap1_dim = color_img1.shape
        if depth_colormap1_dim != color_colormap1_dim:
            resized_rgb_img1 = cv2.resize(color_img1, dsize=(depth_colormap1_dim[1], depth_colormap1_dim[0]), interpolation=cv2.INTER_AREA)
            images1 = np.hstack((resized_rgb_img1, depth_colormap_1))
        else:
            images1 = np.hstack((color_img1, depth_colormap_1))
        

        # Camera 2:
        # Wait for a coherent pair of frames: depth and color
        frames_2 = pipe_cam2.wait_for_frames()
        depth_frame_2 = frames_2.get_depth_frame()
        color_frame_2 = frames_2.get_color_frame()
        # Convert images to numpy arrays
        depth_img2 = np.asanyarray(depth_frame_2.get_data())
        color_img2 = np.asanyarray(color_frame_2.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_img2, alpha=0.03), cv2.COLORMAP_JET)
        
        # Stack all images 2 horizontally
        depth_colormap2_dim = depth_colormap_2.shape
        color_colormap2_dim = color_img2.shape
        if depth_colormap2_dim != color_colormap2_dim:
            resized_rgb_img2 = cv2.resize(color_img2, dsize=(depth_colormap2_dim[1], depth_colormap2_dim[0]), interpolation=cv2.INTER_AREA)
            images2 = np.hstack((resized_rgb_img2, depth_colormap_2))
        else:
            images2 = np.hstack((color_img2, depth_colormap_2))
        
        #images = np.hstack((images1, images2))

        # Show images from camera 1
        cv2.namedWindow('RealSense 1', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense 1', depth_colormap_1)
        
        # Show images from camera 2
        cv2.namedWindow('RealSense 2', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense 2', depth_colormap_2)
        
        key = cv2.waitKey(1)

        # Capture images and depth maps from both cameras by pressing 'c'
        if key == ord('c'):
            #cv2.imwrite("my_image_1.jpg",color_img1)
            cv2.imwrite("my_depth_1.jpg",depth_colormap_1)
            #cv2.imwrite("my_image_2.jpg",color_img2)
            cv2.imwrite("my_depth_2.jpg",depth_colormap_2)
            print("Save")
            break
            
        # Exit program; bug, break is being called after first cycle, its like there's no if statement.
        #if key == 27 or ord('q'): # key 27 = 'ESC'
        #    print('break was called')
        #    break

finally:
    # Stop streaming
    pipe_cam1.stop()
    pipe_cam2.stop()

'''
i = 1
try:
    while True:
        print('cycle number = ', i)
        i += 1
        # Camera 1
        # Wait for a coherent pair of frames: depth and color
        frames_1 = pipe_cam1.wait_for_frames()
        depth_frame_1 = frames_1.get_depth_frame()
        color_frame_1 = frames_1.get_color_frame()
        if not depth_frame_1 or not color_frame_1:
            continue
        # Convert images to numpy arrays
        depth_image_1 = np.asanyarray(depth_frame_1.get_data())
        color_image_1 = np.asanyarray(color_frame_1.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_1, alpha=0.03), cv2.COLORMAP_JET)

        # Camera 2
        # Wait for a coherent pair of frames: depth and color
        frames_2 = pipe_cam2.wait_for_frames()
        depth_frame_2 = frames_2.get_depth_frame()
        color_frame_2 = frames_2.get_color_frame()
        if not depth_frame_2 or not color_frame_2:
            continue
        # Convert images to numpy arrays
        depth_image_2 = np.asanyarray(depth_frame_2.get_data())
        color_image_2 = np.asanyarray(color_frame_2.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap_2 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image_2, alpha=0.03), cv2.COLORMAP_JET)

        # Stack all images horizontally
        images = np.hstack((color_image_1, depth_colormap_1,color_image_2, depth_colormap_2))

        # Show images from both cameras
        cv2.namedWindow('RealSense', cv2.WINDOW_NORMAL)
        cv2.imshow('RealSense', images)
        ch = cv2.waitKey(1)

        # Save images and depth maps from both cameras by pressing 's'
        #ch = cv2.waitKey(25)
        
        if ch == 27 or ord('q'):
            print('quit the program was called')
            break
        
        if ch==115:
            cv2.imwrite("my_image_1.jpg",color_image_1)
            cv2.imwrite("my_depth_1.jpg",depth_colormap_1)
            cv2.imwrite("my_image_2.jpg",color_image_2)
            cv2.imwrite("my_depth_2.jpg",depth_colormap_2)
            print ("Save")
finally:
    # Stop streaming
    pipe_cam1.stop()
    pipe_cam2.stop()
'''

