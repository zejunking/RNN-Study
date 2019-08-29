# -*- coding: UTF-8 -*-

import cv2
import numpy as np
import aircv as ac


def ImgToData(imgUrl, num):
    path = 'static/newSliceImage/{num}/{imgUrl}'.format(num=num, imgUrl=imgUrl)
    imsrc = cv2.imread(path, 0)
    im = cv2.resize(imsrc, (56, 56), interpolation=cv2.INTER_AREA)
    image = np.array(im)
    return image


def filterImage(base):
    test = base + 'test.png'
    testBg = base + 'testBg.png'
    imsrc = cv2.imread(test, 0)  # 原始图像
    imsch = cv2.imread(testBg, 0)

    print(imsch.shape)
    height, width = imsch.shape
    print(height, width)
    top, bottom, left, right = 0, 100000, 10000, 0
    for i in range(height):
        for j in range(width):
            if imsch[i][j] > 0:
                if top <= i:
                    top = i
                if bottom >= i:
                    bottom = i
                if left >= j:
                    left = j
                if right <= j:
                    right = j

    imsch1 = imsch[bottom:top, left:right]

    cv2.imwrite(base + 'testBg1.png', imsch1)

    imsch2 = ac.imread(base + 'testBg1.png')
    imsrc2 = ac.imread(test)
    res1 = ac.find_all_template(imsrc2, imsch2, threshold=0.5, maxcnt=0, rgb=False, bgremove=True)
    print(res1)
    res = None
    if(len(res1) > 0):
        res = res1[0]
        for final in res1:
            if res['confidence'] < final['confidence']:
                res = final
    else:
        return base+'test.png'
    left = res['rectangle'][0][0]
    right = left + 50
    print('res-->', res, len(res1), res['rectangle'][0][0])
    print('1: ', res1)
    res = ac.find_template(imsrc2, imsch2)
    print('2: ', res)

    height1, width1 = imsrc.shape
    # left = res['rectangle'][0][0]
    # right = left + 50
    print(height1, width1)
    for i in range(height1):
        for j in range(width1):
            if i <= top and i >= bottom and j >= left and j <= right:
                # print('ixj: ', i, ' ', j)
                pass
            else:
                imsrc[i][j] = 0
    print(top, bottom, left, right)
    cv2.imwrite(base+'test1.png', imsrc)
    return (base+'test1.png', left)


if __name__ == "__main__":
    filterImage()
