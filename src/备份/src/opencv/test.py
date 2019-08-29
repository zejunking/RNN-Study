import aircv as ac
import cv2

# src = '/Users/zejun/Public/DeepLearning/example/sliceImage/189/b82e1cc0-8ce2-11e9-8c84-f018980779c1.png'
# sch = 'images/imgBg/0-2200/testBg559.png'

# src = 'test2.png'
# sch = 'test1.png'
# src = 'sliceImage/110/53b11a94-8d79-11e9-9b5d-f018980779c1.png'
src = 't1.png'
sch = 't2.png'

imsrc = ac.imread(src)  # 原始图像
imsch = ac.imread(sch)  # 带查找的部分
print(src, sch)
res2 = ac.find_all_sift(imsrc, imsch)
print(res2)
res1 = ac.find_all_template(imsrc, imsch, threshold=0.1, maxcnt=0, rgb=False, bgremove=True)
cur = res1[0]
for final in res1:
    if cur['confidence'] < final['confidence']:
        cur = final
print('cur-->', cur)
print(res1)
res = ac.find_template(imsrc, imsch)
print(res)
# print(ac.find_all_sift(imsrc, imsch))


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        param += 1
        xy = "%d,%d" % (x, y)
        cv2.circle(imsrc, (x, y), 1, (255, 0, 0), thickness=-1)
        cv2.putText(imsrc, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    1.0, (0, 0, 0), thickness=1)
        cv2.imshow("Python opencv", imsrc)


# cv2.setMouseCallback
cv2.namedWindow("Python opencv")
length = 0
# cv2.setMouseCallback("Python opencv", on_EVENT_LBUTTONDOWN, length)
cv2.imshow("Python opencv", imsrc)
print(length)
k = cv2.waitKey(0)
if k == 27:  # 如果按键是ESC
    cv2.destroyAllWindows()
else:
    cv2.destroyAllWindows()

cv2.destroyAllWindows()
