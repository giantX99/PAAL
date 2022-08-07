import pyrealsense2 as rs
import time

#Constants:
#1
serial_num_1 = '203522252121' # Old camera d455 (Yellow)
cam1_file_name = '{}/pos{}_cam1__'
#2
serial_num_2 = '213522252513' # New camera d455 (Green)
cam2_file_name = '{}/pos{}_cam2__'
#general
dir = 'C:/Users/gian-/OneDrive/Documentos/PAAL/Field_DATA'


#PIPELINE SETUP:
# camera 1 (yellow):
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 5)
config_cam1.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 5)

# camera 2 (green):
pipe_cam2 = rs.pipeline()
config_cam2 = rs.config()
config_cam2.enable_device(serial_num_2)
config_cam2.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 5)
config_cam2.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 5)

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
        
        pos = input('Enter position number to capture frame as .bag; Or "q" to quit. ')
        
        if pos == '1' or pos == '2' or pos == '3':
            start = time.time()

            cam1_saver = rs.save_single_frameset(cam1_file_name.format(dir, pos))
            cam2_saver = rs.save_single_frameset(cam2_file_name.format(dir, pos))

            #get frames
            frames1 = pipe_cam1.wait_for_frames()
            frames2 = pipe_cam2.wait_for_frames()
            #process the alignment of frames
            aligned_frames1 = align1.process(frames1)
            aligned_frames2 = align2.process(frames2)

            cam1_saver.process(aligned_frames1)
            cam2_saver.process(aligned_frames2)

            end = time.time()
            print('Capturing time = ', end-start, 's')
            print('Position #', pos, ' captured.')
            break
        elif pos == 'q':
            print('quiting...')
            break
        else:
            print('Enter 1 for position 1, 2 for position 2, 3 for position 3.')
            continue
      
#WRAP UP:
finally:
    print('Next step is extract ply, save as posX_camX.ply')
    pipe_cam1.stop()
    pipe_cam2.stop()
