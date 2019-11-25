import cv2
import time
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
import numpy as np
import pickle
from SSD300.ssd_v2 import SSD300v2
from SSD300.ssd_training import MultiboxLoss
from SSD300.ssd_utils import BBoxUtility



IMAGE_WIDTH  = 300
IMAGE_HEIGHT = 300
SLEEP_TIME = 1
MAX_TARGET_COUNT = 2
confidence = 0.4
voc_classes = ['little', 'big']
NUM_CLASSES = len(voc_classes) + 1

def init_model():

    input_shape = (IMAGE_WIDTH, IMAGE_HEIGHT, 3)

    model = SSD300v2(input_shape, num_classes=NUM_CLASSES)

    priors = pickle.load(open('./SSD300/prior_boxes_ssd300.pkl', 'rb'))
    bbox_util = BBoxUtility(NUM_CLASSES, priors)
    model.load_weights('./dataset/checkpoint-20-0.7403.hdf5', by_name=True)

    return model, bbox_util

def takeSecond(elem):
    return elem[1]


def predict_image(model, bbox_util, image_path):
    inputs = []

    img = image.load_img(image_path, target_size=(IMAGE_WIDTH, IMAGE_HEIGHT))
    img = image.img_to_array(img)
    inputs.append(img.copy())
    inputs = preprocess_input(np.array(inputs))



    preds = model.predict(inputs, batch_size=1, verbose=1)
    results = bbox_util.detection_out(preds)

    print(results[0])
    if results is None or len(results) ==0:
        return None
    if len(results) == 0 or len(results[0]) <= 1:
        return None
    results.sort(key=takeSecond, reverse=True)
    results = results[0][0:MAX_TARGET_COUNT]

    return results



def draw_image(cv2, image , image_path , model, bbox_util):


    """
    预测图片， 根据返回结果重新绘制图片
    :param cv:
    :param img:
    :return:
    """
    results = predict_image(model, bbox_util, image_path)
    if results is None:
        return
    font = cv2.FONT_HERSHEY_SIMPLEX
    print(image.shape)
    for item in results:
        if item[1] < confidence:
            continue
        xmin = int(round(image.shape[1] * item[2]))
        ymin = int(round(image.shape[0] * item[3]))
        xmax = int(round(image.shape[1] * item[4]))
        ymax = int(round(image.shape[0] * item[5]))
        color = (0, 255, 0)
        if int(item[0]) == 1:
            name = 'Card : {}% '.format(int(item[1]*100))
            cv2.putText(img, name, (xmin, ymin), font, 1.2, (255, 255, 255), 2)
            color = (0, 0, 255)
        else:
            name = 'Phone : {}% '.format(int(item[1] * 100))
            cv2.putText(img, name, (xmin, ymin), font, 1.2, (255, 255, 255), 2)
            color = (0, 255, 0)

        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)

    cv2.imshow('SSD-DEMO', image)





model, bbox_util = init_model()
cap = cv2.VideoCapture(0)
cv2.namedWindow("SSD - Demo")

show_count = 0
while(cap.isOpened()):  #isOpened()  检测摄像头是否处于打开状态
    ret,img = cap.read()  #把摄像头获取的图像信息保存之img变量
    print('============ ', show_count)
    show_count += 1
    if show_count > SLEEP_TIME:
        show_count = 0
    else:
        continue
    if ret == True:       #如果摄像头读取图像成功
        image_path = './test.jpg'
        cv2.imwrite(image_path, img)
        draw_image(cv2, img, image_path, model, bbox_util)
        k = cv2.waitKey(100)
        if k == ord('a') or k == ord('A'):
            print('A key down')
            # draw_image(cv2, img, model, bbox_util)

        if cv2.waitKey(100) & 0xff == ord('q'):
            break

cap.release()  #关闭摄像头
cv2.waitKey(0)
cv2.destroyAllWindow()


