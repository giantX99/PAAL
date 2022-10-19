import pyrealsense2 as rs
import numpy as np
import time
import cv2

#ratio of 8:2
active = 8
down = 2

#cameras serial numbers
sn = '207522073378' #D435
sn_i = '141722071529'#D435i
sn_55 = '203522252121' #D455 cam1 (yellow)

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
    
    d_frame_list = []
    depth_time = []

    # Start streaming
    depth_sensor.set_option(rs.option.emitter_enabled, 0)
    pipeline.start(config)
    align_to = rs.stream.depth
    align = rs.align(align_to)
    time.sleep(1) # Camera warmup
    
    start = time.time()
    print('cycle start')

    i = 0
    d = 0
    while time.time()-start <= active:
        i += 1
        if i<2:
            laser_on = False
        else:
            depth_sensor.set_option(rs.option.emitter_enabled, 1)
            laser_on = True
        # Wait for frames without laser: depth and infrared
        frames = pipeline.wait_for_frames()
        frames = align.process(frames)
        frames.keep()

        if not laser_on:
            print('laser on? ', laser_on)
            ir1_frame = frames.get_infrared_frame(1)
            ir1_image = np.asanyarray(ir1_frame.get_data())
    
        else:
            d += 1
            depth_time.append(time.time())
            d_interval = time.time()
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
            d_interval = time.time() - d_interval

    # Stop streaming
    pipeline.stop()
    # Save images
    date_time = time.strftime('%H_%M_%S_')
    cv2.imwrite(date_time + '_infrared.jpg', ir1_image)
    k = 1
    for d_img in d_frame_list:
        cv2.imwrite(date_time + str(k) + '_depth.jpg', d_img)
        k += 1
    
    print('Time spent in depth: ', depth_time[-1] - depth_time[0])
    print('1 depth interval: ', d_interval)
    print('Total iterations: ', i)
    print('Depth iterations: ', d, ' -> frame count')

    # Sleep
    print('cycle end')
    time.sleep(down)

'''1st time spent in depth = 3.128681182861328'''
'''
2nd test, w/ laser modifications in loop:
Time spent in depth:  3.527531623840332
1 depth interval:  0.10596728324890137
Total iterations:  9
Depth iterations:  8 -> frame count
'''
'''
3rd test, NO laser modifications in loop:
Time spent in depth:  3.9136221408843994
1 depth interval:  0.09110903739929199
Total iterations:  31
Depth iterations:  30 -> frame count
'''
'''
4th test, NO laser modifications in loop, frames.keep():
Time spent in depth:  3.8202297687530518
1 depth interval:  0.10848236083984375
Total iterations:  41
Depth iterations:  40  -> frame count
'''
'''
5th test, same as 4th DID NOT TOUCHED THE CAMERA, CAMERA WAS STILL:
Time spent in depth:  3.940720319747925
1 depth interval:  0.058007240295410156
Total iterations:  52
Depth iterations:  51  -> frame count
'''
'''
6th test, same as 5th:
Time spent in depth:  3.878298044204712
1 depth interval:  0.06233787536621094
Total iterations:  46
Depth iterations:  45  -> frame count
'''
'''
7th test, same as 3rd test only difference DID NOT TOUCHED THE CAMERA, CAMERA WAS STILL:
Time spent in depth:  3.879300832748413
1 depth interval:  0.0670919418334961
Total iterations:  42
Depth iterations:  41  -> frame count
'''
'''
8th test, same as 4th, MOVED THE CAMERA A LOT, seems that frames.keep() is good:
Time spent in depth:  3.8348331451416016
1 depth interval:  0.05629372596740723
Total iterations:  45
Depth iterations:  44  -> frame count
'''
'''
9th test, same as 8th but no frames.keep():
Time spent in depth:  3.9455394744873047
1 depth interval:  0.08095693588256836
Total iterations:  37
Depth iterations:  36  -> frame count
'''
'''
10th test, w/ laser modifications in loop, CAMERA STILL:
Time spent in depth:  3.338069438934326
1 depth interval:  0.0870051383972168
Total iterations:  14
Depth iterations:  13  -> frame count
'''
'''
11th test, same as 10th but  a LOT of camera movement:
Time spent in depth:  2.8570525646209717
1 depth interval:  0.07605886459350586
Total iterations:  9
Depth iterations:  8  -> frame count
'''
