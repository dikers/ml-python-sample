import keras
from keras import optimizers
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from keras.callbacks import LearningRateScheduler, TensorBoard
import cv2
import os
from sklearn import model_selection

IMAGE_DIMS = (140, 140, 3)
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input, decode_predictions

from keras.preprocessing import image
import numpy as np


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

    dir_list.append('/Users/mac/tmp/test_split_image/demo4/cut/')
    dir_list.append('/Users/mac/tmp/test_split_image/demo5/cut/')
    dir_list.append('/Users/mac/tmp/test_split_image/demo6/cut/')
    dir_list.append('/Users/mac/tmp/test_split_image/demo7/cut/')
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
    x_train, x_test, y_train, y_test = \
        model_selection.train_test_split(images, labels, test_size=0.9)

    print("================================== ")
    print(x_train.shape)
    print(x_test.shape)
    print(y_train.shape)
    print(y_test.shape)

    return x_train, x_test, y_train, y_test


model = load_model("target/lenet.h5")

print("Loaded model from disk")

x_train, x_test, y_train, y_test = load_data()

result = model.predict(x_test)
print(type(result))

total_count = len(result)

right_count = 0
for pre, real in zip(result, y_test):
    # print(pre, real)
    if np.argmax(pre) == np.argmax(real):
        right_count += 1
print('socre {} '.format(right_count*100/total_count))