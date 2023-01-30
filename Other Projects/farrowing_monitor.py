import pyrealsense2 as rs
import numpy as np
import time
import cv2

#ratio of 8:2
active = 4
down = 1

saving_dir = '/home/pi/Desktop/SingleLiDAR_Robot/test/frames/'

# Configure depth and IR streams:
pipeline = rs.pipeline()
config = rs.config()
#pipeline_wrapper = rs.pipeline_wrapper(pipeline)
#pipeline_profile = config.resolve(pipeline_wrapper)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 5)
config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 5) #Left IR = 1

spat_filter = rs.spatial_filter()   # Spatial    - edge-preserving spatial smoothing
temp_filter = rs.temporal_filter()  # Temporal   - reduces temporal noise

# Keep Running:
while True:
    print('CYCLE START')
    start = time.time()
    d_frame_list = []
    
    # Start streaming
    profile = pipeline.start(config)
    time.sleep(1) # Camera warmup
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    depth_sensor.set_option(rs.option.emitter_enabled,0)
    laser_on = False
    
    t1 = time.time()
    while time.time()-start <= active:
        # Wait for frames
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        ir_frame = frames.get_infrared_frame()
        if not depth_frame or not ir_frame:
            continue
        
        # Apply Depth filter to reduce noise
        depth_filtered = spat_filter.process(depth_frame)
        depth_filtered = temp_filter.process(depth_filtered)
        
        # Convert images to numpy arrays
        ir_image = np.asanyarray(ir_frame.get_data())
        depth_image = np.asanyarray(depth_filtered.get_data())
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        # Save to list
        d_frame_list.append(depth_colormap)
        if laser_on == False:
            save_ir = ir_image
            depth_sensor.set_option(rs.option.emitter_enabled,1)
            laser_on = True
            #time.sleep(1)

    tf = time.time() - t1
    # Stop streaming
    pipeline.stop()
    # Save images
    date_time = time.strftime('%H_%M_%S_')
    cv2.imwrite(saving_dir + date_time + '_infrared.jpg', save_ir)
    k = 1
    for d_img in d_frame_list:
        cv2.imwrite(saving_dir + date_time + str(k) + '_depth.jpg', d_img)
        k += 1
    # Sleep
    time.sleep(down)
    stop = time.time() - start
    print('CYCLE END')
    print('CYCLE TIME: ', stop)
    print('Loop time: ', tf)