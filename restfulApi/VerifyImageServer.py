import os
import cv2
import flask
import sys
import aircv as ac
import numpy as np

from keras.utils import np_utils
from keras.models import load_model
sys.path.append(os.path.join(os.getcwd(), 'src/opencv'))
from dealImages import dealImage
from filterImages import filterImage
app = flask.Flask(__name__)

model = load_model('model/rnn1.hdf5')
# 预测图像中滑块位置
def PredictImage(imsrc):
    im = cv2.resize(imsrc, (56, 56), interpolation=cv2.INTER_AREA)
    img = np.array(im)
    print('before-->', img.shape)
    img = img.reshape(56, -1).astype('float') / 255.0
    # img = img.reshape(-1).astype('float') / 255.0
    print('after-->', img.shape)

    pred = model.predict(np.array([img]))
    print(pred)
    print([final.argmax() for final in pred])
    return str([final.argmax() for final in pred][0])


im = cv2.imread('/Users/zejun/Downloads/xxx.png', 0)
PredictImage(im)


# 预测接口
@app.route("/predict", methods=["POST"])
def predict():
    data = {"success": False}
    if flask.request.method == "POST":
        print(flask.request.form)
        if flask.request.form:

            # test = flask.request.form.getlist('test')[0]
            # testBg = flask.request.form.getlist('testBg')[0]

            # imsrc = ac.imread(test)  # 原始图像
            # imsch = ac.imread(testBg)
            # res1 = ac.find_all_template(imsrc, imsch, threshold=0.5, maxcnt=0, rgb=False, bgremove=True)
            # print('1: ', res1)
            # res = ac.find_template(imsrc, imsch)
            # print('2: ', res)

            # # decode image
            # print('path: ', test, testBg)
            (path, left) = filterImage('/Users/zejun/Downloads/')
            print(path)
            image = cv2.imread(path, 0)
            data['predict'] = PredictImage(image)
            data['left'] = left
            data['success'] = True

    return flask.jsonify(data)


# 默认路由接口
@app.route('/delete', methods=['get'])
def delete():
    test = '/Users/zejun/Downloads/test.png'
    testBg = '/Users/zejun/Downloads/testBg.png'

    im1 = cv2.imread(test)
    im2 = cv2.imread(testBg)
    if im1 is None:
        pass
    else:
        cv2.imwrite('/Users/zejun/Downloads/test-bei.png', im1)
        os.remove(test)
    if im2 is None:
        pass
    else:
        cv2.imwrite('/Users/zejun/Downloads/testBg-bei.png', im2)
        os.remove(testBg)
    return flask.jsonify('Success!')


# 默认路由接口
@app.route('/', methods=['get'])
def home():
    return flask.jsonify('Welcome to VerifyImageServer!')


# 默认路由接口
@app.route('/testOther', methods=['get'])
def testOther():
    (path, left) = filterImage('/static/otherImages/')
    print(path)
    image = cv2.imread(path, 0)
    predict = PredictImage(image)
    print(left, predict)
    return flask.jsonify('Welcome to VerifyImageServer!')
# 主程序
if __name__ == '__main__':
    app.run()
