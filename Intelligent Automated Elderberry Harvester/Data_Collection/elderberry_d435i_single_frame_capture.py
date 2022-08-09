import pyrealsense2 as rs
import time

#Constants:
#serial_num_d455 = '203522252121' # camera #1 d455 
#1
serial_num_1 = '141722071529' # camera d435i
cam1_file_name = '{}/row{}_{}_cam1_'
#general
row = input('Insert row number: ')
dir = 'C:/Users/gian-/OneDrive/Documentos/GitHub/PAAL/Intelligent Automated Elderberry Harvester/Data_Collection'
saving_counter = 0


#PIPELINE SETUP:
# camera d435i :
pipe_cam1 = rs.pipeline()
config_cam1 = rs.config()
config_cam1.enable_device(serial_num_1)
config_cam1.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)
config_cam1.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 6)

try:
    #Pipe profiles by pipe.start():
    pipe_prof1 = pipe_cam1.start(config_cam1)

    '''
    #Get device and turn Auto-Exposure on RGB off:
    cam1 = pipe_prof1.get_device()
    cam1.query_sensors()[1].set_option(rs.option.auto_exposure_priority, 0.0)
    '''

    #align all frames:
    align1_to = rs.stream.color
    align1 = rs.align(align1_to)
  
    begin = time.time()

    #START STREAMING:
    while True:
        
        choice = input('Press ENTER to capture Frame as .bag; Or "q" to quit. ')
        
        if choice == '':
            start = time.time()
            #camera saver class
            cam1_saver = rs.save_single_frameset(cam1_file_name.format(dir, row, saving_counter+1))
           
            #get frames
            frames1 = pipe_cam1.wait_for_frames()
            #process the alignment of frames
            aligned_frames1 = align1.process(frames1)
            #save processed frame
            cam1_saver.process(aligned_frames1)
            
            #user feedback
            end = time.time()
            saving_counter += 1
            print('frame #', saving_counter, ' captured')
            print('Capturing time = ', round(end-start), 's')
            
        elif choice == 'q':
            print('Quiting...')
            break
        else:
            continue
      
#WRAP UP:
finally:
    print('Number of frames saved for row #', row, ': ', saving_counter)
    print('Time spent collecting: ', time.time()-begin)
    pipe_cam1.stop()