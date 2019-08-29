import os
import cv2
import pandas as pd


table = []


def Read_Data(dir, file):

    imagepath = dir + '/' + file
    # 读取图片
    image = cv2.imread(imagepath, 0)
    # 二值化
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # 显示图片
    bin_values = [1 if pixel == 255 else 0 for pixel in thresh.ravel()]
    label = dir.split('/')[-1]
    table.append(bin_values + [label])


def main():
    for num in range(260):
      pwd = os.path.abspath('.')
      cur = os.path.join(pwd, 'result1/{distance}/'.format(distance=num))
      if os.path.exists(cur) is True:
        print(cur)
        for file in os.listdir(cur):
            Read_Data(cur, file)
    # chars = '123456789ABCDEFGHJKLNPQRSTUVXYZ'
    # dirs = ['/%s' % char for char in chars]
    # print(dirs)
    # for dir in dirs:
    #     for file in os.listdir(dir):
    #         Read_Data(dir, file)

    features = ['v' + str(i) for i in range(1, 16 * 20 + 1)]
    label = ['label']
    df = pd.DataFrame(table, columns=features + label)
    # print(df.head())

    df.to_csv('data.csv', index=False)


main()
