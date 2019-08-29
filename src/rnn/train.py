import os
import sys
import numpy as np
from keras.utils import np_utils
from keras.datasets import mnist
from keras.layers import Activation, Dense, Dropout, TimeDistributed, Embedding
from keras.layers.recurrent import SimpleRNN
from keras.models import Sequential
from keras.optimizers import SGD, Adam, RMSprop

sys.path.append(os.path.join(os.getcwd(), 'src/opencv'))
from dealImages import dealImage


def main():

    # 追捕数据集
    imgData = dealImage()
    (x_train, y_train) = imgData
    print('x_shape:', x_train.shape)
    print('y_shape', y_train.shape)

    x_train = x_train.reshape(x_train.shape[0], 56, -1).astype('float') / 255.0
    # 转换labels为one hot格式
    num_classes = 170
    y_train = np_utils.to_categorical(y_train, num_classes=num_classes)
    print('x_shape:', x_train.shape)
    print('y_shape', y_train.shape)

    # 创建模型 keras模型分为顺序模型和函数式API模型
    # 顺序模型是多个网络层的线性堆叠，可以帮助我们快速创建一些简单的模型，是我们最常使用的模型
    # 函数式API模型是用来定义复杂模型(多输出模型、有向无环图、具有共享层的模型)的方法
    model = Sequential()  # 创建顺序模型

    cell_size = 300  # 输出数据的维度(当前层神经元的数目)

    # 循环神经网络
    model.add(SimpleRNN(
        units=cell_size,  # 输出数据的维度(当前层神经元的数目)
        activation='tanh',  # 激活函数，默认即tanh
        return_sequences=True,
        input_shape=(56, 56)  # 输入数据的维度(shape)
    ))

    # 如果当前层的输入维度与前一层的输出维度一致，可以不写输入维度
    model.add(SimpleRNN(units=cell_size, return_sequences=True))
    model.add(SimpleRNN(units=cell_size, return_sequences=True))
    # 每层SimpleRNN之间必须设置return_sequences=True(默认是False)
    # return_sequences 是返回输出序列的最后一个输出(False)，还是返回全部序列(True)
    # return_sequences=True 表示我们需要完整的编码序列，而不仅仅是最终总结状态

    # return_sequences=True 返回的是个多维数组，如果下一层无法接收该种多维数组，则层需要设置为return_sequences=True或者不设置取默认值
    model.add(SimpleRNN(units=cell_size))
    # 添加全连接层作为输出层
    model.add(Dense(num_classes, activation='softmax'))

    # 定义优化器
    adam = Adam(lr=1e-4)
    # sgd = SGD(lr=0.2)
    # rms = RMSprop(lr=0.001)

    # 定义优化器，loss function，训练过程中计算准确率
    model.compile(
        optimizer=adam,  # 优化器
        loss='categorical_crossentropy',  # 损失函数 mse 均方差 categorical_crossentropy 交叉熵(多分类)
        metrics=['accuracy']  # 训练和测试期间的模型评估标准
    )

    # 开始训练模型，调用model.fit()方法，方法采用时序后向传播算法训练模型
    # 以给的数目的轮次训练模型，到第epochs轮结束训练，每轮多个批次，每批次大小batch_size
    model.fit(x_train, y_train, batch_size=32, epochs=20)
    # 预测模型的损失值和准确率
    loss, accuracy = model.evaluate(x_train, y_train)
    print('test loss', loss)
    print('accuracy', accuracy)
    # 保存模型，以便使用时加载
    model.save('model/rnn1.hdf5')
    model.save_weights('model/rnn1_weight.h5')


if __name__ == "__main__":
    main()
