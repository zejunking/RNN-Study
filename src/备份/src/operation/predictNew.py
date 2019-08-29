import numpy as np
import aircv as ac
import cv2

from keras.utils import np_utils
from keras.models import load_model
from new.dealImages import dealImage

model = load_model('model/rnn_new.hdf5')
# model = load_model('model/rnn1Eb.hdf5')

# img = image.load_img('test2.png', target_size=(40, 65))
# img = np.array(img)
src = 't1.png'
sch = 't2.png'

imsrc = ac.imread(src)  # 原始图像
imsch = ac.imread(sch)  # 带查找的部分
print(src, sch)
res1 = ac.find_all_template(imsrc, imsch, threshold=0.5, maxcnt=0, rgb=False, bgremove=True)
print(res1)
res = ac.find_template(imsrc, imsch)
print(res)

# path = 'sliceImage/{num}/{imgUrl}'.format(num=num, imgUrl=imgUrl)
# path = 'test.png'
# path = 't1.png'
# path = 'newSliceImage/113/0054c0fa-9191-11e9-be10-f018980779c1.png'

# path = 'test.png'
path = '/Users/zejun/Downloads/test1.png'
print(path)
imsrc = cv2.imread(path, 0)
im = imsrc
cv2.namedWindow("Python opencv")
length = 0
# cv2.setMouseCallback("Python opencv", on_EVENT_LBUTTONDOWN, length)
cv2.imshow("Python opencv", imsrc)
k = cv2.waitKey(0)
if k == 27:  # 如果按键是ESC
    cv2.destroyAllWindows()
else:
    cv2.destroyAllWindows()

cv2.destroyAllWindows()


im = cv2.resize(imsrc, (56, 56), interpolation=cv2.INTER_AREA)
img = np.array(im)
print('before-->', img.shape)
img = img.reshape(56, -1).astype('float') / 255.0
# img = img.reshape(-1).astype('float') / 255.0
print('after-->', img.shape)

(x_test, y_test) = dealImage()
pred = model.predict(np.array([img]))
print('x_shape:', x_test.shape)
print('y_shape', y_test.shape)
x_test = x_test[:2000]
y_test = y_test[:2000]
x_test = x_test.reshape(x_test.shape[0], 56, -1).astype('float') / 255.0
num_classes = 220
y_test = np_utils.to_categorical(y_test, num_classes=num_classes)
loss, accuracy = model.evaluate(x_test, y_test)
print('test loss', loss)
print('accuracy', accuracy)
print([final.argmax() for final in pred])
