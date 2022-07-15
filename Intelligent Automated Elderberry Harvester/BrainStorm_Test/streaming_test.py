import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline() #creates the context object, grabs the data produced by the camera and manages it or output it.    #The class abstracts the camera configuration and streaming, and the vision modules triggering and threading
config = rs.config() #Config provides its users a way to set the filters and test if there is no conflict with the pipeline requirements from the device
#It also allows the user to find a matching device for the config filters and the pipeline, in order to select a device explicitly, and modify its controls before streaming starts.

#some info about the library:
'''my_realsense_serial_num = '203522252121' '''
'''config.enable_device(my_realsense_serial_num)''' #selects realsense device by serial number
'''type_of_stream = rs.stream''' #if its depth, rgb, etc.
'''stream_width = 640'''
'''stream_height = 480'''
'''stream_format = rs.format''' #how binary data is encoded within a frame
'''stream_framerate = 30''' #30 frames/second
'''config.enable_stream(type_of_stream.depth, stream_width, stream_height, stream_format.z16, stream_framerate)'''

#Getting devicce product line and stream configuration:
pipeline_wrapper = rs.pipeline_wrapper(pipeline) #necessary to get the pipeline profile, device profile and information.
pipeline_profile = config.resolve(pipeline_wrapper) #class able to extract info from device being used.
#config.resolve Resolve the configuration filters, to find a matching device and streams profiles. The method resolves the user configuration filters for the device and streams.
my_realsense = pipeline_profile.get_device() #returns the device usde by the pipeline.
my_realsense_product_line = str(my_realsense.get_info(rs.camera_info.product_line)) #returns the product line of my realsense device

print('My realsense device product line is: ', my_realsense_product_line)
for i in my_realsense.sensors:
    print(i.get_info(rs.camera_info.name))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30) #config depth stream
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30) #config RGB stream

pipeline.start(config) #Start the pipeline streaming according to the configuraion.
#It gets streaming data, but it doesnt output anything yet

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame() #get the frame, specifically the depth frame.
        rgb_frame = frames.get_color_frame() #get the frame, specifically the RGB frame.
        #continue the loop if dont get the frames
        if not depth_frame or not rgb_frame:
            continue
        
        # Converting images into numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        rgb_image = np.asanyarray(rgb_frame.get_data())


        #weird configs in order to stream in OpenCV
        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
        # If depth and color resolutions are different, resize color image to match depth image for display
        depth_colormap_dim = depth_colormap.shape
        rgb_colormap_dim = rgb_image.shape
        if depth_colormap_dim != rgb_colormap_dim:
            resized_rgb_image = cv2.resize(rgb_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_rgb_image, depth_colormap))
            cv2.imshow("depth frame", depth_colormap)
            cv2.imshow("rgb frame", resized_rgb_image)
        else:
            images = np.hstack((rgb_image, depth_colormap))
        
        # Show images:
        cv2.imshow("depth frame", depth_colormap)
        cv2.imshow("rgb frame", rgb_image)
        
        key = cv2.waitKey(1)
        if key == 27: #key 27 is ESC button on keyboard
            break

finally:
    pipeline.stop() #stop the stream