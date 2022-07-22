import pyrealsense2 as rs
import time
import threading

serial_num_1 = '203522252121' # Old camera d455 (Yellow)
serial_num_2 = '213522252513' # New camera d455 (Green)

# camera 1 (yellow):
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16h, 30)
config_cam1.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config_cam1.enable_record_to_file('cam1_2.bag')

# camera 2 (green):
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16h, 30)
config_cam2.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 30)
config_cam2.enable_record_to_file('cam2_2.bag')


#Pipe profiles by pipe.start():
pipe_prof1 = pipe_cam1.start(config_cam1)
pipe_prof2 = pipe_cam2.start(config_cam2)


#Setting recorders:
#1
recorder1 = pipe_prof1.get_device().as_recorder()
recorder1.pause()
print('recorder1 created, paused')
#2
recorder2 = pipe_prof2.get_device().as_recorder()
recorder2.pause()
print('recorder2 created, paused\n')


#Get device and turn Auto-Exposure on RGB off:
cam1 = pipe_prof1.get_device()
cam1.query_sensors()[1].set_option(rs.option.auto_exposure_priority, 0.0)
cam2 = pipe_prof2.get_device()
cam2.query_sensors()[1].set_option(rs.option.auto_exposure_priority, 0.0)


#define collecting frame process
def wait_frames(pipeline):
    pipeline.wait_for_frames().keep()

try:
    t_frames1 = threading.Thread(target=wait_frames, args=(pipe_cam1,))
    t_frames2 = threading.Thread(target=wait_frames, args=(pipe_cam2,))
    print('while loop about to start, recording about to start!')
    recorder1.resume()
    print('camera1 recording...')
    recorder2.resume()
    print('camera2 recording...')
    
    start = time.time()
    
    #Collect frames concurrently 
    while time.time() - start < 10:
        t_frames1.start()
        t_frames2.start()
        t_frames1.join()
        t_frames2.join()
      
finally:
    recorder1.pause()
    recorder2.pause()
    end = time.time()
    print('Recording Stopped! Recording duration: ', end-start)
    pipe_cam1.stop()
    pipe_cam2.stop()