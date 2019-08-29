import os
import cv2
import uuid
import time
import pymysql
import numpy as np

db = pymysql.connect('localhost', 'root', '', 'rnn')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")
nofind = 0

allData = []
maxHeight = 0
minHeight = 160


def loopImgHight(img, height, left, curLeft):
    res = []
    for j in range(left, curLeft):
        newArr = []
        for i in range(height):
            tmp = np.insert(img[i][0: len(img[i]) - 1], 0, img[i][len(img[i]) - 1:])
            # img[i] = tmp
            newArr.append(tmp)
        res = newArr
        img = newArr
    return np.array(img)


def loopImgBottom(img):
    img = img
    for i in range(10):
        img = np.concatenate((img[1:], img[0:1]))
    return img


def loopImgTop(img):
    img = img
    for i in range(10):
        np.concatenate((img[len(img) - 1:], img[0: len(img) - 1]))
    return img


def saveToData(distance, img):
    pwd = os.path.abspath('.')
    cur = os.path.join(pwd, 'newSliceImage/{distance}'.format(distance=distance))
    if os.path.exists(cur) is False:
        os.makedirs(cur)
    uid = uuid.uuid1()
    resultPath = 'newSliceImage/{distance}/{uid}.png'.format(uid=uid, distance=distance)
    # print(resultPath)
    cv2.imwrite(resultPath, img)
    curTime = int(time.time())
    cursor.execute('INSERT INTO TAB_SLICE_IMG_INFO_NEW (imgUrl, imgNum, createdTime, sign) VALUES ("{uid}.png", {distance}, {curTime}, 0)'.format(uid=uid, distance=distance, curTime=curTime))
    db.commit()


def cutImg(path):  # 裁剪图片,去除slice图片背景为0的部分,方便做图片模板匹配
    try:
        # 读取一张图片并显示出来
        img = cv2.imread(path, 0)
        if img is None:
            return
        height, width = img.shape
        top, bottom, left, right = 0, 100000, 10000, 0
        imgBF = img.copy()
        # imgBF = img
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
                    imgBF[i][j] = 0
                else:
                    imgBF[i][j] = 255

        global minHeight, maxHeight
        if top > maxHeight:
            maxHeight = top
        if top < minHeight:
            minHeight = top
        # return
        for data in allData:
            if (np.array_equal(data, imgBF)):
                global nofind
                nofind += 1
                return
        np.append(allData, imgBF)
        print(bottom, top, left, right)

        saveToData(left, img)
        # showImg(img)
        newImg = img

        # while right < 190:
        #     right += 1
        #     left += 1
        #     if left > 43:
        #         newImg = loopImgHight(newImg, height)
        #         saveToData(left, newImg)

        curBottom = bottom

        img1 = img

        while curBottom > 33:
            curBottom -= 10
            img1 = loopImgBottom(img1)
            curRight = right
            curLeft = left
            while curRight < 190:
                curRight += 10
                curLeft += 10
                if curLeft > 43 and curLeft < 250:
                    img3 = loopImgHight(img1, height, left, curLeft)
                    saveToData(curLeft, img3)
                    # showImg(img3)

        img2 = img
        while top < 145:
            top += 10
            img2 = loopImgTop(img2)
            curRight = right
            curLeft = left
            while curRight < 190:
                curRight += 10
                curLeft += 10
                if curLeft > 43 and curLeft < 250:
                    img4 = loopImgHight(img2, height, left, curLeft)
                    saveToData(curLeft, img4)

        # showImg(newImg)

    except (ValueError, RuntimeError, FileNotFoundError):
        print('error -->')
        pass
    else:
        pass
    finally:
        pass


def showImg(img):
    cv2.namedWindow("Python opencv")
    cv2.imshow("Python opencv", img)
    k = cv2.waitKey(0)  # 如果不添最后一句，在IDLE中执行窗口直接无响应。在命令行中执行的话，则是一闪而过。
    if k == 27:  # 如果按键是ESC
        cv2.destroyAllWindows()  # 最后的销毁窗口是一个好的习惯
    cv2.destroyAllWindows()


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


# imgList = os.listdir('/Users/zejun/Public/DeepLearning/example/images/dealing')

# for name in imgList:
#   path = '/Users/zejun/Downloads/{name}'.format(name=name)
#   resPath = 'images/imgBg/{name}'.format(name=name)
#   print(path, nofind)
#   cutImg(path)
# print(nofind)
# # 10712
allData = np.array(allData)
for index in range(10561, 11079):
  path = '/Users/zejun/Downloads/testBg{index}.png'.format(index=index)
  resPath = 'images/imgBg/testBg{index}.png'.format(index=index)
  print(index, path, nofind, minHeight, maxHeight)
  cutImg(path)
print(nofind, minHeight, maxHeight)
#   deleteImg(path)
#   deleteImg(path1)

# k = cv2.waitKey(0)  # 如果不添最后一句，在IDLE中执行窗口直接无响应。在命令行中执行的话，则是一闪而过。
# if k == 27:  # 如果按键是ESC
#     cv2.destroyAllWindows()  # 最后的销毁窗口是一个好的习惯
# cv2.destroyAllWindows()
