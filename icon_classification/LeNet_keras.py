from keras import optimizers
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from keras.callbacks import LearningRateScheduler, TensorBoard
import cv2
import os
from keras.preprocessing.image import img_to_array
from sklearn import model_selection
import numpy as np
IMAGE_DIMS = (120, 120, 3)

def get_file_list(file_dir):
    """
    :param file_dir:
    :return:
    """
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.JPG':
                input_file_name = os.path.join(root, file)
                L.append(input_file_name)
    return L


def load_data():
    dir_list = []

    dir_list.append('/Users/mac/tmp/test_split_image/demo/cut/')
    dir_list.append('/Users/mac/tmp/test_split_image/demo2/cut/')
    dir_list.append('/Users/mac/tmp/test_split_image/demo3/cut/')
    images = []
    labels = []

    index = 0
    for path_dir in dir_list:
        L = get_file_list(path_dir)

        for image_path in L:
            image = cv2.imread(image_path)
            image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
            image = img_to_array(image)
            images.append(image)
            label_item = []
            for i in range(len(dir_list)):
                label_item.append(0)
            label_item[index] = 1

            labels.append(label_item)

        index += 1

    images = np.array(images, dtype='float')
    labels = np.array(labels, dtype='int')
    x_train, x_test, y_train , y_test= \
        model_selection.train_test_split(images, labels, test_size=0.3)

    print("================================== ")
    print(x_train.shape)
    print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)


    return x_train, x_test, y_train, y_test





def build_model():
    model = Sequential()
    model.add(Conv2D(6, (5, 5), padding='valid', activation = 'relu', kernel_initializer='he_normal', input_shape=IMAGE_DIMS))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    model.add(Conv2D(16, (5, 5), padding='valid', activation = 'relu', kernel_initializer='he_normal'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))
    model.add(Flatten())
    model.add(Dense(120, activation = 'relu', kernel_initializer='he_normal'))
    model.add(Dense(84, activation = 'relu', kernel_initializer='he_normal'))
    model.add(Dense(IMAGE_DIMS[2], activation = 'softmax', kernel_initializer='he_normal'))
    sgd = optimizers.SGD(lr=.1, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    return model

def scheduler(epoch):
    if epoch < 10:
        return 0.01
    if epoch < 20:
        return 0.005
    return 0.001

if __name__ == '__main__':

    # load data
    x_train, x_test, y_train, y_test = load_data()
    print(y_train[0])
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    x_train /= 255.0
    x_test /= 255.0

    print(x_train.shape)
    print(y_test[0])

    # build network
    model = build_model()
    print(model.summary())

    # set callback
    tb_cb = TensorBoard(log_dir='./target', histogram_freq=0)
    change_lr = LearningRateScheduler(scheduler)
    cbks = [change_lr,tb_cb]

    # start train
    model.fit(x_train, y_train,
              batch_size=50,
              epochs=10,
              callbacks=cbks,
              validation_data=(x_test, y_test),
              shuffle=True)

    # save model
    model.save('target/lenet.h5')

    result = model.predict(x_test)
    print(type(result))

    total_count = len(result)

    right_count = 0
    for pre, real in zip(result, y_test):
        # print(pre, real)
        if np.argmax(pre) == np.argmax(real):
            right_count += 1
    print('socre {} '.format(right_count * 100 / total_count))