import pyrealsense2 as rs
import numpy as np
import time
import cv2

#ratio of 8:2
active = 4
down = 1

# Configure depth and IR streams:
pipeline = rs.pipeline()
config = rs.config()
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 15) #Left IR = 1

device = pipeline_profile.get_device()
depth_sensor = device.query_sensors()[0]
depth_sensor.set_option(rs.option.emitter_on_off, 0) #Set laser to turn on and off every other frame

spat_filter = rs.spatial_filter()   # Spatial    - edge-preserving spatial smoothing
temp_filter = rs.temporal_filter()  # Temporal   - reduces temporal noise

# Keep Running:
while True:
    loop_s = time.time()
    d_frame_list = []
    depth_sensor.set_option(rs.option.emitter_enabled, 0)

    # Start streaming
    pipe_s = time.time()
    pipeline.start(config)
    pipe_f = time.time() - pipe_s
    align_to = rs.stream.infrared
    align = rs.align(align_to)
    time.sleep(1) # Camera warmup
    
    frames = pipeline.wait_for_frames()
    frames = align.process(frames)
    ir1_frame = frames.get_infrared_frame(1)
    ir1_image = np.asanyarray(ir1_frame.get_data())

    sensor_s = time.time()
    depth_sensor.set_option(rs.option.emitter_enabled, 1)
    
    sensor_f = time.time()-sensor_s
    loop_f = time.time()-loop_s
    start = time.time()
    print('cycle start')
    d = 0
    while time.time()-start <= active:
        d += 1
        # Wait for frames
        frames = pipeline.wait_for_frames()
        frames = align.process(frames)
        frames.keep()
        
        # Get depth frame
        depth_frame = frames.get_depth_frame()
        # Apply Depth filter to reduce noise
        depth_filtered = spat_filter.process(depth_frame)
        depth_filtered = temp_filter.process(depth_filtered)
        
        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_filtered.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        # Save to list
        d_frame_list.append(depth_colormap)
    
    print('laser on duration: ', sensor_f)
    print('pipeline duration: ', pipe_f)
    print('First loop duration: ', loop_f)
    print('Second loop duration: ', time.time()-start)
    print('Total iterations: ', d, ' -> depth frames count')
    
    # Stop streaming
    pipeline.stop()
    
    # Save images
    date_time = time.strftime('%H_%M_%S_')
    cv2.imwrite(date_time + '_infrared.jpg', ir1_image)
    k = 1
    for d_img in d_frame_list:
        cv2.imwrite(date_time + str(k) + '_depth.jpg', d_img)
        k += 1
    
    # Sleep
    print('cycle end')
    time.sleep(down)
