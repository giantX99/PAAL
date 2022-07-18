import pyrealsense2 as rs

serial_num_1 = '203522252121' # Old camera d455 (Yellow)
serial_num_2 = '213522252513' # New camera d455 (Green)


# camera 1:
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, rs.format.z16, 30)
config_cam1.enable_stream(rs.stream.color, rs.format.rgb8, 30)

# camera 2 (green):
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_stream(rs.stream.depth, rs.format.z16, 30)
config_cam2.enable_stream(rs.stream.color, rs.format.rgb8, 30)

pipe_prof1 = pipe_cam1.start(config_cam1)
pipe_prof2 = pipe_cam2.start(config_cam2)

cam1 = pipe_prof1.get_device()
cam2 = pipe_prof2.get_device()

recorder1 = rs.recorder('cam1_test4.bag', cam1)
recorder1.as_recorder()
recorder1.pause()
print('recorder1 created, paused')

recorder2 = rs.recorder('cam2_test4.bag', cam2)
recorder2.as_recorder()
recorder2.pause()
print('recorder2 created, paused')


try:
    print('while loop about to start, recording about to start!')
    
    #print('camera1 recording...')
    #print('camera2 recording...')
    
    i = 1
    while True:
        recorder1.pause()
        recorder2.pause()
        pipe_cam1.wait_for_frames()
        pipe_cam2.wait_for_frames()
        recorder1.resume()
        recorder2.resume()
        print(i)
        i += 1
        
        

finally: #KeyboardInterrupt: #^c
    recorder1.pause()
    recorder2.pause()
    print('Recording Stopped!')
    pipe_cam1.stop()
    pipe_cam2.stop()
    pass
