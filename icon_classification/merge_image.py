import os
import cv2



def get_stop_list(num):
    stop_list = []

    for i in range(2):
        stop_list.append('/Users/mac/tmp/test_split_image/merge/029.jpg')
        stop_list.append('/Users/mac/tmp/test_split_image/merge/030.jpg')
        stop_list.append('/Users/mac/tmp/test_split_image/merge/031.jpg')
        stop_list.append('/Users/mac/tmp/test_split_image/merge/030.jpg')
        stop_list.append('/Users/mac/tmp/test_split_image/merge/029.jpg')

    return stop_list


def get_image_list(L, num):
    image_list = []
    temp_list = L.copy()
    list_length = len(temp_list)
    print('list size:  {} , num:  {}'.format(list_length, num))
    if num>len(L):
        print('数量太大')

    for item in range(num):
        # print('1--', temp_list[item])
        image_list.append(temp_list[item])

    # print('-----------------------\n')
    temp_list = temp_list[0:num-1]
    temp_list.reverse()
    for item in range(len(temp_list)):
        # print('2--', temp_list[item])
        image_list.append(temp_list[item])


    return image_list






def get_file_list(file_dir):
    """
    :param file_dir:
    :return:
    """
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                input_file_name = os.path.join(root, file)
                L.append(input_file_name)
    return L



def wirte_image_list(file_list , cv2, video):
    print('write {} pictures success. '.format(len(file_list)))
    for item in file_list:
        img = cv2.imread(item)
        video.write(img)



file_list = get_file_list('/Users/mac/tmp/test_split_image/merge/')


file_list.sort()


video = cv2.VideoWriter("/Users/mac/tmp/test_split_image/merge/video.avi", cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'), 24, (1277, 718))   #视频保存在当前目录下, 格式为 motion-jpeg codec，图片颜色失真比较小


for index in range(3):
    wirte_image_list(get_image_list(file_list, 120), cv2, video)
    wirte_image_list(get_image_list(file_list, 110), cv2, video)
    wirte_image_list(get_image_list(file_list, 130), cv2, video)


video.release()
cv2.destroyAllWindows()