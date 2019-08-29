import cv2
import pymysql
import numpy as np

db = pymysql.connect('localhost', 'root', '', 'rnn')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")


def ImgToData(imgUrl, num):
    path = 'static/newSliceImage/{num}/{imgUrl}'.format(num=num, imgUrl=imgUrl)
    imsrc = cv2.imread(path, 0)
    im = cv2.resize(imsrc, (56, 56), interpolation=cv2.INTER_AREA)
    image = np.array(im)
    return image


def dealImage():
    cursor.execute('SELECT * FROM TAB_SLICE_IMG_INFO_NEW')
    result = cursor.fetchall()
    images = []
    labels = []
    length = 0
    for row in result:
        imgData = ImgToData(row[1], row[2])
        images.append(imgData)
        labels.append(row[2])
        length += 1
    images = np.array(images)
    labels = np.array(labels)
    return (images, labels)


if __name__ == "__main__":
    dealImage()
