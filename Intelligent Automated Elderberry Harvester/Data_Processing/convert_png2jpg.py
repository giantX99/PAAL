import cv2
import os

path_png = 'D:/YOLO/keras_yolo3_position_estimation/VOCdevkit/VOC2007/PNGImages/'
path_jpg = 'D:/YOLO/keras_yolo3_position_estimation/VOCdevkit/VOC2007/jpgImages/'

for file in os.listdir(path_png):
    png_file = path_png + file
    jpg_file = path_jpg + file
    # Load .png image
    png_image = cv2.imread(png_file)
    # Save .jpg image
    cv2.imwrite(jpg_file.replace('.png', '.jpg'), png_image, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    print(jpg_file.replace('.png', '.jpg'), ' saved.')