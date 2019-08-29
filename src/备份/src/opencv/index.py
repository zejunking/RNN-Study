# import cv2


# def split_picture(imagepath):
#     gray = cv2.imread(imagepath, 0)  # 以灰度模式读取图片
#     height, width = gray.shape
#     for i in range(height):
#         for j in range(width):
#             pass
#             # print(gray[i,j], end = ' ')
#         # print('\n')
# #     cv2.imwrite('/Users/zejun/Desktop/test.png', )
#     cv2.namedWindow('input_image', cv2.WINDOW_AUTOSIZE)
#     cv2.waitKey(0)
#     cv2.imshow('input_image', gray)


# imagepath = '/Users/zejun/Public/DeepLearning/example/images/down.png'
# split_picture(imagepath)

import cv2

# 读取一张图片并显示出来
img = cv2.imread('test.png', 0)
if img is None:
    pass

print(img)
# cv2.imwrite('t2.png', img)

height, width = img.shape
for i in range(height):
    for j in range(width):
        pass
        # if img[i, j] > 0:
        #     img[i, j] = 255
        # else:
        #     img[i, j] = 0

# cv2.imwrite('test.png', img)
cv2.imshow("Python opencv", img)  # 在窗口中显示图片，第一个参数是显示图像的窗口的名字，第二个参数是要显示的图像（imread读入的图像），窗口大小自动调整为图片大小
k = cv2.waitKey(0)  # 如果不添最后一句，在IDLE中执行窗口直接无响应。在命令行中执行的话，则是一闪而过。
if k == 27:  # 如果按键是ESC
    cv2.destroyAllWindows()  # 最后的销毁窗口是一个好的习惯
cv2.destroyAllWindows()
