import cv2
import numpy as np
import pymysql

db = pymysql.connect('localhost', 'root', '', 'rnn')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")


def imgToData(imgUrl, num):
    path = 'sliceImage/{num}/{imgUrl}'.format(num=num, imgUrl=imgUrl)
    imsrc = cv2.imread(path, 0)
    im = cv2.resize(imsrc, (56, 56), interpolation=cv2.INTER_AREA)
    image = np.array(im)
    return image


def dealImage():
    cursor.execute('SELECT * FROM TAB_SLICE_IMG_INFO')
    # row = cursor.fetchone()
    # imgToData(row[1], row[2])
    # print(row)
    # return (row, 0)
    result = cursor.fetchall()
    images = []
    labels = []
    length = 0
    for row in result:
        imgData = imgToData(row[1], row[2])
        images.append(imgData)
        labels.append(row[2] - 43)
        length += 1
        # if length == 123:
            # print('pred-->', row[1], row[2])
    # print(labels)
    images = np.array(images)
    labels = np.array(labels)
    return (images, labels)


def imgToData1(imgUrl, num):
    path = 'sliceTestImage/{num}/{imgUrl}'.format(num=num, imgUrl=imgUrl)
    imsrc = cv2.imread(path, 0)
    im = cv2.resize(imsrc, (56, 56), interpolation=cv2.INTER_AREA)
    image = np.array(im)
    return image


def dealTestImage():
    cursor.execute('SELECT * FROM TAB_SLICE_IMG_TEST_INFO')
    # row = cursor.fetchone()
    # imgToData(row[1], row[2])
    # print(row)
    # return (row, 0)
    result = cursor.fetchall()
    images = []
    labels = []
    length = 0
    for row in result:
        imgData = imgToData1(row[1], row[2])
        images.append(imgData)
        labels.append(row[2] - 43)
        length += 1
        # if length == 123:
            # print('pred-->', row[1], row[2])
    # print(labels)
    images = np.array(images)
    labels = np.array(labels)
    return (images, labels)


if __name__ == "__main__":
    dealImage()
