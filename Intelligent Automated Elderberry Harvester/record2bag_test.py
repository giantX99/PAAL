import pyrealsense2 as rs
import time

serial_num_1 = '203522252121' # Old camera d455 (Yellow)
serial_num_2 = '213522252513' # New camera d455 (Green)

# camera 1:
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_cam1.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

# camera 2 (green):
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config_cam2.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)

#Pipe profiles by pipe.start():
pipe_prof1 = pipe_cam1.start(config_cam1)
pipe_prof2 = pipe_cam2.start(config_cam2)

#Get device and turn Auto-Exposure on RGB off:
cam1 = pipe_prof1.get_device()
cam1.query_sensors()[1].set_option(rs.option.auto_exposure_priority, 0.0)
cam2 = pipe_prof2.get_device()
cam2.query_sensors()[1].set_option(rs.option.auto_exposure_priority, 0.0)

#Setting recorders:
#1
recorder1 = rs.recorder('cam1_1.bag', cam1)
recorder1.as_recorder()
recorder1.pause()
print('recorder1 created, paused')
#2
recorder2 = rs.recorder('cam2_1.bag', cam2)
recorder2.as_recorder()
recorder2.pause()
print('recorder2 created, paused\n')


try:
    print('while loop about to start, recording about to start!')
    recorder1.resume()
    print('camera1 recording...')
    recorder2.resume()
    print('camera2 recording...')
    
    start = time.time()
    
    while time.time() - start < 10:
        pipe_cam1.wait_for_frames()
        pipe_cam2.wait_for_frames()
        
        
finally:
    recorder1.pause()
    recorder2.pause()
    print('Recording Stopped!')
    pipe_cam1.stop()
    pipe_cam2.stop()

'''for s in cam1.sensors:
    print(s)
pipe_cam1.stop()'''