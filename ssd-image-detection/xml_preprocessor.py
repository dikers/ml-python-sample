import numpy as np
import os
from xml.etree import ElementTree
import json

class XML_preprocessor(object):

    def __init__(self, data_path, label_list, json_save_path='./dataset/'):
        self.path_prefix = data_path
        self.num_classes = 2
        self.data = dict()
        self._label_list = label_list
        self._json_save_path = json_save_path
        self._preprocess_XML()

    def _preprocess_XML(self):
        filenames = os.listdir(self.path_prefix)
        for filename in filenames:

            if filename.startswith('.'):
                continue
            if not filename.endswith('.xml'):
                continue


            tree = ElementTree.parse(self.path_prefix + filename)
            root = tree.getroot()
            bounding_boxes = []
            one_hot_classes = []
            size_tree = root.find('size')
            width = float(size_tree.find('width').text)
            height = float(size_tree.find('height').text)
            for object_tree in root.findall('object'):
                for bounding_box in object_tree.iter('bndbox'):
                    xmin = float(bounding_box.find('xmin').text)/width
                    ymin = float(bounding_box.find('ymin').text)/height
                    xmax = float(bounding_box.find('xmax').text)/width
                    ymax = float(bounding_box.find('ymax').text)/height
                bounding_box = [xmin,ymin,xmax,ymax]
                bounding_boxes.append(bounding_box)
                class_name = object_tree.find('name').text
                one_hot_class = self._to_one_hot(class_name)
                one_hot_classes.append(one_hot_class)
            image_name = root.find('filename').text
            bounding_boxes = np.asarray(bounding_boxes)
            one_hot_classes = np.asarray(one_hot_classes)
            image_data = np.hstack((bounding_boxes, one_hot_classes))
            self.data[image_name] = image_data

    def _to_one_hot(self,name):
        one_hot_vector = [0] * self.num_classes

        _index = self._label_list.index(name)

        if _index < 0:
            print('Annotations 中的label 和配置文件中 不一致 unknown label: %s' % name)
        one_hot_vector[_index] = 1
        return one_hot_vector

    def _save_file(self, json_object, path):
        with open(path, "w") as f:
            json.dump(json_object, f)
        print("save {} success . ".format(path))


    def to_json(self):

        train_val_list = list()

        filenames = os.listdir(self.path_prefix)

        for filename in filenames:

            if filename.startswith('.'):
                continue
            if not filename.endswith('.xml'):
                continue

            json_object = dict()
            tree = ElementTree.parse(self.path_prefix + filename)
            root = tree.getroot()
            size_tree = root.find('size')
            image_name = root.find('filename').text
            json_object['file'] = image_name

            width = int(size_tree.find('width').text)
            height = int(size_tree.find('height').text)

            annotations = list()
            categories = list()

            for object_tree in root.findall('object'):

                annotation = dict()
                category = dict()
                _top = 0
                _left = 0
                _width = 0
                _height = 0

                for bounding_box in object_tree.iter('bndbox'):
                    _top = int(bounding_box.find('ymin').text)
                    _left = int(bounding_box.find('xmin').text)
                    _width = int(bounding_box.find('xmax').text) - _left
                    _height = int(bounding_box.find('ymax').text) - _top


                class_name = object_tree.find('name').text

                class_id = self._label_list.index(class_name)
                if class_id < 0:
                    print('Annotations 中的label 和配置文件中 不一致 unknown label: %s' % class_name)
                annotation['class_id'] = class_id
                annotation['top'] = _top
                annotation['left'] = _left
                annotation['width'] = _width
                annotation['height'] = _height
                category['class_id'] = class_id
                category['name'] = class_name
                train_val = dict()
                train_val['name'] = image_name.split('.')[0]
                train_val['label'] = class_id + 1
                train_val_list.append(train_val)


                annotations.append(annotation)
                categories.append(category)


            image_size = dict()
            image_size['width'] = width
            image_size['height'] = height
            image_size['depth'] = 3

            json_object['image_size']= image_size
            json_object['annotations'] = annotations
            json_object['categories'] = categories

            path = self._json_save_path + image_name.split('.')[0] +'.json'
            print(path)
            print(json.dumps(json_object))
            self._save_file(json_object, path)

        return train_val_list




label_lists = ['youth', 'old']

json_save_path = './dataset/'
xml = XML_preprocessor('/Users/mac/tmp/ssd_data/Annotations/', label_lists, json_save_path)

print(xml.data)

print(xml.to_json())