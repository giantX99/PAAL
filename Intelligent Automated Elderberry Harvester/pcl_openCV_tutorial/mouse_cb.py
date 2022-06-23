import math
import cv2
import numpy as np

def mouse_cb(app_state, out, event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        app_state.mouse_btns[0] = True

    if event == cv2.EVENT_LBUTTONUP:
        app_state.mouse_btns[0] = False

    if event == cv2.EVENT_RBUTTONDOWN:
        app_state.mouse_btns[1] = True

    if event == cv2.EVENT_RBUTTONUP:
        app_state.mouse_btns[1] = False

    if event == cv2.EVENT_MBUTTONDOWN:
        app_state.mouse_btns[2] = True

    if event == cv2.EVENT_MBUTTONUP:
        app_state.mouse_btns[2] = False

    if event == cv2.EVENT_MOUSEMOVE:

        height_intr, width_intr = out.shape[:2]
        dx, dy = x - app_state.prev_mouse[0], y - app_state.prev_mouse[1]

        if app_state.mouse_btns[0]:
            app_state.yaw += float(dx) / width_intr * 2
            app_state.pitch -= float(dy) / height_intr * 2

        elif app_state.mouse_btns[1]:
            dp = np.array((dx / width_intr, dy / height_intr, 0), dtype=np.float32)
            app_state.translation -= np.dot(app_state.rotation, dp)

        elif app_state.mouse_btns[2]:
            dz = math.sqrt(dx**2 + dy**2) * math.copysign(0.01, -dy)
            app_state.translation[2] += dz
            app_state.distance -= dz

    if event == cv2.EVENT_MOUSEWHEEL:
        dz = math.copysign(0.1, flags)
        app_state.translation[2] += dz
        app_state.distance -= dz

    app_state.prev_mouse = (x, y)