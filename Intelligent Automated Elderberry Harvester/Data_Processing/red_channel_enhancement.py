import cv2

old_dir = 'E:/test/18.18.4.jpg'
new_dir = 'E:/test/no_red3.jpg'

rgb_img = cv2.imread(old_dir, cv2.IMREAD_UNCHANGED)
new_img = rgb_img[:,:,2]
cv2.imwrite(new_dir, new_img)
print('done.')
#cv2.imshow('rgb channel', rgb_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()