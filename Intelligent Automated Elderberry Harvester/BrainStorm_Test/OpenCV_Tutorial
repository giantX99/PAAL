import cv2

presenting_format = -1
img_file = 'Data_Test/lav1_rgb_Color.png'

img = cv2.imread(img_file, presenting_format) #read image.

''' 2nd parameter of cv2.imread:
-1, cv2.imread_color : Loads a color image. Any transparency of image will be neglected. Its default.
0, cv2.imread_grayscale : loads image in grayscale mode.
1, cv2.imread_unchanged : loads image as such including alpha channel.
'''

window_label = 'Image' #label the created window that is gonna be displayed by cv2.imshow

cv2.imshow(window_label, img) #displays image
cv2.waitKey(0) #wait a key to be pressed for x seconds, if x seconds passes, program continues. 0 means infinite time
cv2.destroyAllWindows() #destroys all windows displayed or loaded