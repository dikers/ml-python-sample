import cv2
import os
import numpy as np
from sklearn import model_selection
from keras.preprocessing.image import img_to_array
IMAGE_DIMS = (240, 100, 3)


def get_file_list(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.JPG':
                input_file_name = os.path.join(root, file)
                L.append(input_file_name)
    return L


def create_dataset_label(dir_list):
    data = []
    labels = []

    index =0
    for path_dir in dir_list:
        L = get_file_list(path_dir)

        for image_path in L:
            image = cv2.imread(image_path)
            image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
            image = img_to_array(image)
            data.append(image)

            labels.append(index)

        index += 1

    return data, labels
dir_list = []

dir_list.append('/Users/mac/tmp/test_split_image/demo/cut/')
dir_list.append('/Users/mac/tmp/test_split_image/demo2/cut/')
dir_list.append('/Users/mac/tmp/test_split_image/demo3/cut/')


data, labels = create_dataset_label(dir_list)

x_train0, x_test0, y_train0, y_test0 =  model_selection.train_test_split( data, labels, test_size=0.3)
print(y_test0)
print(len(y_train0))
print(len(y_test0))

