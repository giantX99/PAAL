"""
OpenCV and Numpy Point cloud Software Renderer
Usage:
The moment the stream start, the program will be saving
the pointcloud in .ply format every x amount of seconds.
------
Mouse: 
    Drag with left button to rotate around pivot (thick small axes), 
    with right button to translate and the wheel to zoom.
Keyboard: 
    [r]     Reset View
    [p]     Pause Stream
    [q\ESC] Quit
"""
import sys
import math
import cv2
import numpy as np
import pyrealsense2 as rs
import AppState
import projection_functions
import pointcloud_function


state = AppState.AppState()

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()


config.enable_stream(rs.stream.depth, rs.format.z16, 30)
config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

# Get stream profile and camera intrinsics
profile = pipeline.get_active_profile()
depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
depth_intrinsics = depth_profile.get_intrinsics()
w, h = depth_intrinsics.width, depth_intrinsics.height

# Processing blocks
pc = rs.pointcloud()
decimate = rs.decimation_filter()
decimate.set_option(rs.option.filter_magnitude, 2 ** state.decimate)
colorizer = rs.colorizer()

# Creates an empty array with dimensions (h, w, 3) 3 for rgb values I imagine
out = np.empty((h, w, 3), dtype=np.uint8)

# Mouse event funtion
def mouse_cb(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        state.mouse_btns[0] = True

    if event == cv2.EVENT_LBUTTONUP:
        state.mouse_btns[0] = False

    if event == cv2.EVENT_RBUTTONDOWN:
        state.mouse_btns[1] = True

    if event == cv2.EVENT_RBUTTONUP:
        state.mouse_btns[1] = False

    if event == cv2.EVENT_MBUTTONDOWN:
        state.mouse_btns[2] = True

    if event == cv2.EVENT_MBUTTONUP:
        state.mouse_btns[2] = False

    if event == cv2.EVENT_MOUSEMOVE:

        height_intr, width_intr = out.shape[:2]
        dx, dy = x - state.prev_mouse[0], y - state.prev_mouse[1]

        if state.mouse_btns[0]:
            state.yaw += float(dx) / width_intr * 2
            state.pitch -= float(dy) / height_intr * 2

        elif state.mouse_btns[1]:
            dp = np.array((dx / width_intr, dy / height_intr, 0), dtype=np.float32)
            state.translation -= np.dot(state.rotation, dp)

        elif state.mouse_btns[2]:
            dz = math.sqrt(dx**2 + dy**2) * math.copysign(0.01, -dy)
            state.translation[2] += dz
            state.distance -= dz

    if event == cv2.EVENT_MOUSEWHEEL:
        dz = math.copysign(0.1, flags)
        state.translation[2] += dz
        state.distance -= dz

    state.prev_mouse = (x, y)
# End mouse function 

# User input to proceed
rate_of_saving = 30
choice = input('Press ENTER to proceed with the PointCloud Export (rate is 1 ply every %dsec).\nOr press "q" to exit.' %(rate_of_saving/30))
if choice == 'q':
    sys.exit()
print('System running, press "p" to pause or "q" or ESC key to exit.') 

# Creates window and point cloud visualization 
cv2.namedWindow(state.WIN_NAME, cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow(state.WIN_NAME, w, h)
cv2.setMouseCallback(state.WIN_NAME, mouse_cb)

# saving pointcloud variables
num_frames = 1
ply_file_path = 'C:/Users/gian-/OneDrive/Documentos/PAAL/data/ply/'
ply_file_name = 'ply_data_{}.ply'

while True:
    # Grab camera data
    if not state.paused:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        depth_frame = decimate.process(depth_frame)

        # Grab new intrinsics (may be changed by decimation)
        depth_intrinsics = rs.video_stream_profile(
            depth_frame.profile).get_intrinsics()
        w, h = depth_intrinsics.width, depth_intrinsics.height

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_colormap = np.asanyarray(
            colorizer.colorize(depth_frame).get_data())

        if state.color:
            mapped_frame, color_source = color_frame, color_image
        else:
            mapped_frame, color_source = depth_frame, depth_colormap

        points = pc.calculate(depth_frame)
        pc.map_to(mapped_frame)

        # Pointcloud data to arrays
        v, t = points.get_vertices(), points.get_texture_coordinates()
        verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
        texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv

    # Render

    out.fill(0)

    projection_functions.grid(state, out, (0, 0.5, 1), size=1, n=10)
    projection_functions.frustum(state, out, depth_intrinsics)
    projection_functions.axes(out, projection_functions.view(state, [0, 0, 0]), state.rotation, size=0.1, thickness=1)

    if not state.scale or out.shape[:2] == (h, w):
        pointcloud_function.pointcloud(state, out, verts, texcoords, color_source)
    else:
        tmp = np.zeros((h, w, 3), dtype=np.uint8)
        pointcloud_function.pointcloud(state, tmp, verts, texcoords, color_source)
        tmp = cv2.resize(
            tmp, out.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)
        np.putmask(out, tmp > 0, tmp)

    if any(state.mouse_btns):
        projection_functions.axes(out, projection_functions.view(state, state.pivot), state.rotation, thickness=4)

    # Show pointcloud
    cv2.setWindowTitle(state.WIN_NAME, "PointCloud Stream")
    cv2.imshow(state.WIN_NAME, out)
    
    # Save pointcloud every rate_of_saving frames (stream rate = 30 frames/sec)
    if not state.paused:
        if num_frames % rate_of_saving == 0:
            points.export_to_ply(ply_file_path+ply_file_name.format(int(num_frames/rate_of_saving)), mapped_frame)
            print(ply_file_name.format(int(num_frames/rate_of_saving)), 'was saved.')
        num_frames += 1
    key = cv2.waitKey(1)

    if key == ord("r"):
        state.reset()

    if key == ord("p"):
        state.paused ^= True

    if key in (27, ord("q")) or cv2.getWindowProperty(state.WIN_NAME, cv2.WND_PROP_AUTOSIZE) < 0:
        break

# Stop streaming
pipeline.stop()