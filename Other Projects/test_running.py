import pyrealsense2 as rs
import numpy as np
import time
import cv2

#ratio of 8:2
active = 8
down = 2

# Configure depth and IR streams:
pipeline = rs.pipeline()
config = rs.config()
#config.enable_device(sn)
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

print('okay')

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
config.enable_stream(rs.stream.infrared, 1, rs.format.y8, 15) #Left IR = 1

print('okay2')

device = pipeline_profile.get_device()
depth_sensor = device.query_sensors()[0]
depth_sensor.set_option(rs.option.emitter_on_off, 1) #Set laser to turn on and off every other frame

print('emitter_on_off activated')

dec_filter = rs.decimation_filter() # Decimation - reduces depth frame density
spat_filter = rs.spatial_filter()   # Spatial    - edge-preserving spatial smoothing
temp_filter = rs.temporal_filter()  # Temporal   - reduces temporal noise

# Keep Running:
while True:
    # Start streaming
    pipeline.start(config)
    align_to = rs.stream.depth
    align = rs.align(align_to)
    time.sleep(1) # Camera warmup
    start = time.time()
    print('cycle start')

    while time.time()-start <= active:
        # Wait for frames without laser: depth and infrared
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        ir1_frame = aligned_frames.get_infrared_frame(1)
        
        # Apply Depth filter to reduce noise:
        depth_filtered = dec_filter.process(depth_frame)
        depth_filtered = spat_filter.process(depth_filtered)
        depth_filtered = temp_filter.process(depth_filtered)
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_filtered.get_data())
        ir1_image = np.asanyarray(ir1_frame.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        # Show images
        cv2.namedWindow('ir_left', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('ir_left', ir1_image)
        
        cv2.namedWindow('depth_image', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('depth_image', depth_colormap)

        cv2.waitKey(1)
        
    # Stop streaming
    pipeline.stop()
    # Sleep
    print('cycle end')
    time.sleep(down)