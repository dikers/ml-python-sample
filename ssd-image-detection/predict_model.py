from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
import pickle
from SSD300.ssd_v2 import SSD300v2
from SSD300.ssd_training import MultiboxLoss
from SSD300.ssd_utils import BBoxUtility



IMAGE_WIDTH  = 300
IMAGE_HEIGHT = 300

def init_model():
    voc_classes = ['little', 'big']
    NUM_CLASSES = len(voc_classes) + 1
    input_shape = (IMAGE_WIDTH, IMAGE_HEIGHT, 3)

    model = SSD300v2(input_shape, num_classes=NUM_CLASSES)

    priors = pickle.load(open('./SSD300/prior_boxes_ssd300.pkl', 'rb'))
    bbox_util = BBoxUtility(NUM_CLASSES, priors)

    model.load_weights('./dataset/checkpoint-13-0.4195.hdf5', by_name=True)

    return model, bbox_util


def predict_image(model, bbox_util, file_path):
    inputs = []

    img = image.load_img(file_path, target_size=(IMAGE_WIDTH, IMAGE_HEIGHT))
    img = image.img_to_array(img)

    inputs.append(img.copy())

    inputs = preprocess_input(np.array(inputs))

    preds = model.predict(inputs, batch_size=1, verbose=1)

    return bbox_util.detection_out(preds)


file_path = "./test.jpg"
model, bbox_util = init_model()
results = predict_image(model, bbox_util, file_path)


print(len(results))


print(results)