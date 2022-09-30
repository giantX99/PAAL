import pyrealsense2 as rs
import numpy as np
import time
import cv2

#ratio of 8:2
active = 8
down = 2

sn = '207522073378' #D435i serial number

# Configure depth and IR streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_device(sn)

config.enable_stream(rs.stream.depth, rs.format.z16, 10)
config.enable_stream(rs.stream.infrared, 1, rs.format.y8, 10)   #Left IR = 1
config.enable_stream(rs.stream.infrared, 2, rs.format.y8, 10)   #Right IR = 2

while True:
    # Start streaming
    pipeline.start(config)
    start = time.time()

    while time.time()-start <= active:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        ir1_frame = frames.get_infrared_frame(1)
        ir2_frame = frames.get_infrared_frame(2)

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        ir1_image = np.asanyarray(ir1_frame.get_data())
        ir2_image = np.asanyarray(ir2_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Show images
        cv2.namedWindow('ir_left', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('ir_left', ir1_image)

        cv2.namedWindow('ir_right', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('ir_right', ir2_image)

        cv2.namedWindow('depth_image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('depth_image', depth_colormap)

        cv2.waitKey(1)
    
    # Stop streaming
    pipeline.stop()
    time.sleep(down)