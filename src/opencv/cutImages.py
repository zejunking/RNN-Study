import os
import cv2


def cutImg(path, resPath):  # 裁剪图片,去除slice图片背景为0的部分,方便做图片模板匹配
    try:
        # 读取一张图片并显示出来
        img = cv2.imread(path, 0)
        if img is None:
            return
        height, width = img.shape
        top, bottom, left, right = 0, 100000, 10000, 0
        for i in range(height):
            for j in range(width):
                if img[i, j] > 0:
                    if top <= i:
                        top = i
                    if bottom >= i:
                        bottom = i
                    if left >= j:
                        left = j
                    if right <= j:
                        right = j
        print(bottom, top, left, right)
        cropped = img[bottom:top, left:right]
        cv2.imwrite(resPath, cropped)
        print('write img to ', resPath)
    except (ValueError, RuntimeError, FileNotFoundError):
        print('error --> ', index)
        pass
    else:
        pass
    finally:
        pass


def saveImg(path, resPath):  # 保存图片
    try:
        # 读取一张图片并显示出来
        img = cv2.imread(path, 0)
        if img is None:
            return
        print(img)
        cv2.imwrite(resPath, img)
        print('origin write img to ', resPath)
    except (ValueError, RuntimeError, FileNotFoundError):
        print('error save --> ', index)
        pass
    else:
        pass
    finally:
        pass


def deleteImg(path):  # 删除图片
    try:
        os.remove(path)
    except (ValueError, RuntimeError, FileNotFoundError):
        print('error save --> ', index)
        pass
    else:
        pass
    finally:
        pass


for index in range(10505, 21451):
  path = '/Users/zejun/Downloads/testBg{index}.png'.format(index=index)
  resPath = 'images/imgBg/testBg{index}.png'.format(index=index)
  print(index, path)
  cutImg(path, resPath)
  path1 = '/Users/zejun/Downloads/test{index}.png'.format(index=index)
  resPath1 = 'images/img/test{index}.png'.format(index=index)
  saveImg(path1, resPath1)
  deleteImg(path)
  deleteImg(path1)

k = cv2.waitKey(0)  # 如果不添最后一句，在IDLE中执行窗口直接无响应。在命令行中执行的话，则是一闪而过。
if k == 27:  # 如果按键是ESC
    cv2.destroyAllWindows()  # 最后的销毁窗口是一个好的习惯
cv2.destroyAllWindows()
