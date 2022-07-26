import pyrealsense2 as rs
from datetime import datetime
import time
import shutil

#Constants:
serial_num_1 = '203522252121' # Old camera d455 (Yellow)
serial_num_2 = '213522252513' # New camera d455 (Green)
SSD_dir = '/Elderberry/'
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
cam1_file_name = '{}_cam1.bag'.format(date)
cam2_file_name = '{}_cam2.bag'.format(date)


#PIPELINE SETUP:
# camera 1 (yellow):
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16h, 15)
config_cam1.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 15)
config_cam1.enable_record_to_file(cam1_file_name)

# camera 2 (green):
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16h, 15)
config_cam2.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 15)
config_cam2.enable_record_to_file(cam2_file_name)

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

#RECORDING BAG FILE:
try:
    print('while loop about to start, recording about to start!')
    recorder1.resume()
    print('camera1 recording...')
    recorder2.resume()
    print('camera2 recording...')
    
    start1 = time.time()
    
    #Collect frames concurrently 
    while time.time() - start1 < 10:
        pipe_cam1.wait_for_frames().keep()
        pipe_cam2.wait_for_frames().keep()

#WRAP UP:
finally:
    recorder1.pause()
    recorder2.pause()
    end1 = time.time()
    pipe_cam1.stop()
    pipe_cam2.stop()
    print('Recording Stopped! Recording duration: ', end1-start1)
    print('Transfering files to SSD...')
    start2 = time.time()
    shutil.move(cam1_file_name, SSD_dir)
    shutil.move(cam2_file_name, SSD_dir)
    end2 = time.time()
    print('Files transfered! Transfering duration: ', end2-start2)