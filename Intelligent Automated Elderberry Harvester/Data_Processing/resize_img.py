from PIL import Image

file_path = ''

for i in range(10):
    image = Image.open(file_path + '' + '.png')
    cropped_pic = image.crop((160,0,1120, 720))
    new_pic = image.resize((640,480))
    new_pic.save('resized' + i + '.png')
    


    

