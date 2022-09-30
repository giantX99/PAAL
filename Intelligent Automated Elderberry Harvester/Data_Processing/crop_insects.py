from PIL import Image

file_path = 'E:/test/6.20.2.jpg'
resized_path = 'E:/test/resized_img.jpg'

#for image in file_path:
if True:   
    rgb = Image.open(file_path)
    cropped_pic = rgb.crop((160,0,1120, 720))
    new_pic = cropped_pic.resize((640,480))
    resized_name = resized_path
    new_pic.save(resized_name)

