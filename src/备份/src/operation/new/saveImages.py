import os
import cv2
import time
import aircv as ac
import pymysql

db = pymysql.connect('localhost', 'root', '', 'rnn')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")
nofind = 0


def saveSql(distance, sign, index):
    pwd = os.path.abspath('.')
    cur = os.path.join(pwd, 'sliceImage/{distance}'.format(distance=distance))
    if os.path.exists(cur) is False:
        os.makedirs(cur)

    resultPath = 'sliceImage/{distance}/test{uid}.png'.format(uid=index, distance=distance)
    print(resultPath)
    img = cv2.imread(path, 0)  # 原始图像
    cv2.imwrite(resultPath, img)
    curTime = int(time.time())
    cursor.execute('INSERT INTO TAB_SLICE_IMG_INFO (imgUrl, imgNum, createdTime, sign) VALUES ("test{uid}.png", {distance}, {curTime}, {sign})'.format(uid=index, distance=distance, curTime=curTime, sign=sign))
    db.commit()


def saveImage(path, bgPath, index):
    try:
        img = cv2.imread(path, 0)
        cv2.imwrite(path, img)
        # 读取一张图片并显示出来
        imsrc = ac.imread(path)  # 原始图像
        if imsrc is None:
            return
        imsch = ac.imread(bgPath)  # 带查找的部分
        res1 = ac.find_all_template(imsrc, imsch, threshold=0.5, maxcnt=0, rgb=False, bgremove=True)
        res = None
        if(len(res1) > 0):
            res = res1[0]
            for final in res1:
                if res['confidence'] < final['confidence']:
                    res = final
        print('res-->', res, len(res1))
        # res = ac.find_template(imsrc, imsch, threshold=0.5, bgremove=True)
        print(index, res)
        distance = -1
        if res is None:
            global nofind
            nofind += 1
            return
            print('none --->', index, path, bgPath)

            def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    param += 1
                    xy = "%d,%d" % (x, y)
                    cv2.circle(imsrc, (x, y), 1, (255, 0, 0), thickness=-1)
                    cv2.putText(imsrc, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                                1.0, (0, 0, 0), thickness=1)
                    cv2.imshow("Python opencv", imsrc)
                    distance = x
                    print('x--->', x)
                    saveSql(distance, 1, index)
            cv2.namedWindow("Python opencv")
            length = 0
            cv2.setMouseCallback("Python opencv", on_EVENT_LBUTTONDOWN, length)
            cv2.imshow("Python opencv", imsrc)

            k = cv2.waitKey(0)
            if k == 27:  # 如果按键是ESC
                cv2.destroyAllWindows()
            return
        else:
            distance = res['rectangle'][0][0]

        # return
        saveSql(distance, 0, index)
        # pwd = os.path.abspath('.')
        # cur = os.path.join(pwd, 'sliceImage/{distance}'.format(distance=distance))
        # if os.path.exists(cur) is False:
        #     os.makedirs(cur)

        # uid = uuid.uuid1()
        # resultPath = 'sliceImage/{distance}/{uid}.png'.format(uid=uid, distance=distance)
        # print(resultPath)
        # img = cv2.imread(path, 0)  # 原始图像
        # cv2.imwrite(resultPath, img)
        # curTime = int(time.time())
        # cursor.execute('INSERT INTO TAB_SLICE_IMG_INFO (imgUrl, imgNum, createdTime) VALUES ("{uid}.png", {distance}, {curTime})'.format(uid=uid, distance=distance, curTime=curTime))
    except (ValueError, RuntimeError):
        print(index)
        pass
    else:
        pass
    finally:
        pass


# 2553
# for index in range(0, 2200):
for index in range(2201, 6770):
    path = 'images/img/test{index}.png'.format(index=index)
    resPath = 'images/imgBg/testBg{index}.png'.format(index=index)
    # path = 'images/img/0-2200/test{index}.png'.format(index=index)
    # resPath = 'images/imgBg/0-2200/testBg{index}.png'.format(index=index)
    # print(index, path)
    saveImage(path, resPath, index)
    print(nofind)

k = cv2.waitKey(0)  # 如果不添最后一句，在IDLE中执行窗口直接无响应。在命令行中执行的话，则是一闪而过。
if k == 27:  # 如果按键是ESC
    cv2.destroyAllWindows()  # 最后的销毁窗口是一个好的习惯
cv2.destroyAllWindows()
