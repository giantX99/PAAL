import pyrealsense2 as rs
from datetime import datetime
import time
import shutil

#Constants:
#1
serial_num_1 = '203522252121' # Old camera d455 (Yellow)
cam1_file_name = '{}/{}_{}_cam1.bag'
#2
serial_num_2 = '213522252513' # New camera d455 (Green)
cam2_file_name = '{}/{}_{}_cam2.bag'
#general
SSD_dir = 'D:\Test'
cur_dir = 'C:/Users/gian-/OneDrive/Documentos/GitHub/PAAL/Intelligent Automated Elderberry Harvester'
saving_counter = 0


#PIPELINE SETUP:
# camera 1 (yellow):
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
config_cam1.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 15)

# camera 2 (green):
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
config_cam2.enable_stream(rs.stream.color, 640, 480, rs.format.rgb8, 15)

try:
    #Pipe profiles by pipe.start():
    pipe_prof1 = pipe_cam1.start(config_cam1)
    pipe_prof2 = pipe_cam2.start(config_cam2)

    #Get device and turn Auto-Exposure on RGB off:
    cam1 = pipe_prof1.get_device()
    cam1.query_sensors()[1].set_option(rs.option.auto_exposure_priority, 0.0)
    cam2 = pipe_prof2.get_device()
    cam2.query_sensors()[1].set_option(rs.option.auto_exposure_priority, 0.0)

    #align all frames:
    align1_to = rs.stream.color
    align1 = rs.align(align1_to)
    align2_to = rs.stream.color
    align2 = rs.align(align2_to)


    #START STREAMING:
    while True:
        
        choice = input('Press ENTER to capture Frame as .bag; Or "q" to quit. ')
        
        if choice == '':
            start = time.time()

            date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
            cam1_saver = rs.save_single_frameset(cam1_file_name.format(cur_dir, date, saving_counter+1))
            cam2_saver = rs.save_single_frameset(cam2_file_name.format(cur_dir, date, saving_counter+1))
            
            #get frames
            frames1 = pipe_cam1.wait_for_frames()
            frames2 = pipe_cam2.wait_for_frames()
            #process the alignment of frames
            aligned_frames1 = align1.process(frames1)
            aligned_frames2 = align2.process(frames2)

            cam1_saver.process(aligned_frames1)
            cam2_saver.process(aligned_frames2)

            end = time.time()
            print('Capturing time = ', round(end-start), 's')
            saving_counter += 1
            
            #Transfer file to SSD
            print('Transfering files to SSD...')
            shutil.move(cam1_file_name.format(cur_dir, date, saving_counter+1), cam1_file_name.format(SSD_dir, date, saving_counter+1)) #Source file must have same name as destination file!!
            shutil.move(cam2_file_name.format(cur_dir, date, saving_counter+1), cam2_file_name.format(SSD_dir, date, saving_counter+1))
            end2 = time.time()
            print('Files transfered! Transfering duration: ', end2-end)
       
        elif choice == 'q':
            print('Quiting script...')
            break
        else:
            continue
      
#WRAP UP:
finally:
    print('Number of frames saved: ', saving_counter)
    pipe_cam1.stop()
    #pipe_cam2.stop()
