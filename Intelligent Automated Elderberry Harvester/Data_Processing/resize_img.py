#crop 1280x720 image from center to 640x480 (w,h)
from PIL import Image

file_path = 'C:/Users/gian-/OneDrive/Documentos/PAAL/rgb_extracted_field_08_08_22/'
resized_path = 'C:/Users/gian-/OneDrive/Documentos/PAAL/rgb_extracted_field_08_08_22/resized_640_480/'

for counter in range(1, 106):
    img_name = file_path + 'row1_rgb_' + str(counter) + '.png'
    image = Image.open(img_name)
    cropped_pic = image.crop((160,0,1120, 720))
    new_pic = image.resize((640,480))
    resized_name = resized_path + 'resized_row1_rgb_' + str(counter) + '.png'
    new_pic.save(resized_name)
