import numpy as np
import aircv as ac
import cv2

from keras.utils import np_utils
from keras.models import load_model

model = load_model('model/rnn1.hdf5')

path = '/Users/zejun/Downloads/test1.png'
print(path)
imsrc = cv2.imread(path, 0)
im = cv2.resize(imsrc, (56, 56), interpolation=cv2.INTER_AREA)
img = np.array(im)
print('before-->', img.shape)
img = img.reshape(56, -1).astype('float') / 255.0
# img = img.reshape(-1).astype('float') / 255.0
print('after-->', img.shape)
pred = model.predict(np.array([img]))
print([final.argmax() for final in pred])
