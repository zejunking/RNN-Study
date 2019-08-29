import numpy as np
from keras.datasets import mnist
from keras.layers import Activation, Dense, Dropout, TimeDistributed, Embedding
from keras.layers.recurrent import SimpleRNN
from keras.models import Sequential
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
from img.dealImages import dealImage


def main():
    myData = dealImage()
    (x_train, y_train) = myData
    print('x_shape:', x_train.shape)
    print('y_shape', y_train.shape)
    x_train = x_train[:1000]
    y_train = y_train[:1000]
    x_train = x_train.reshape(x_train.shape[0], -1).astype('float') / 255.0
    # 转换labels为one hot格式
    num_classes = 150
    y_train = np_utils.to_categorical(y_train, num_classes=num_classes)
    print('x_shape:', x_train.shape)
    print('y_shape', y_train.shape)

    # 创建模型
    model = Sequential()

    cell_size = 200  # 1260

    # 嵌入层，处理输入数据
    model.add(Embedding(3136, output_dim=56))

    # 循环神经网络
    model.add(SimpleRNN(
        units=cell_size,  # 输出
        # input_dim=124800
        # activation='sigmoid',
        return_sequences=True,
        # input_shape=(56, 56)
    ))

    model.add(SimpleRNN(units=cell_size, return_sequences=True))
    model.add(SimpleRNN(units=cell_size))

    # 输出层
    model.add(Dense(num_classes, activation='softmax'))

    # 定义优化器
    adam = Adam(lr=1e-4)
    # sgd = SGD(lr=0.2)
    # rms = RMSprop(lr=0.001)

    # 定义优化器，loss function，训练过程中计算准确率
    model.compile(
        optimizer=adam,
        # optimizer=sgd,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # model = Sequential([
    #     Dense(units=num_classes, input_dim=124800),
    #     Dense(units=num_classes),
    #     Dense(units=num_classes, bias_initializer='one', activation='softmax')
    # ])
    # sgd = SGD(lr=0.2)
    # model.compile(
    #     optimizer=sgd,
    #     loss='categorical_crossentropy',  # mse 均方差 categorical_crossentropy 交叉熵
    #     metrics=['accuracy']
    # )
    model.fit(x_train, y_train, batch_size=32, epochs=10)
    loss, accuracy = model.evaluate(x_train, y_train)
    print('test loss', loss)
    print('accuracy', accuracy)
    model.save('model/rnn1Eb.hdf5')
    model.save_weights('model/rnn1Eb_weight.h5')
    pred = model.predict(np.array([x_train[123]]))
    print([final.argmax() for final in pred])


if __name__ == "__main__":
    main()
