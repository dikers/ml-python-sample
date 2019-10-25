from PIL import Image
from multiprocessing import Process
import histogram as htg
import aHash as ah
import pHash as ph
import dHash as dh
import os
import time


"""
ffmpeg -ss 00:00 -i test.ts -f image2  -s 300x200 -r 0.5 -t 02:00 1%3d.jpg
ffmpeg -ss 00:01 -i test.ts -f image2  -s 300x200 -r 0.5 -t 00:30 2%3d.jpg

视频截图 
"""

# 相似度的最低值  max 64
SIMILARITY_BAR_PH = 57
#max 64
SIMILARITY_BAR_DH = 44

SIMILARITY_BAR_AH = 44
BASE_DIR = '/Users/mac/tmp/test_split_image/demo2/'
# 广告的帧数窗口值
AVERT_IMAGE_COUNT = 3

# 下一个广告位置， 默认10秒后
NEXT_AVERT_WINDOW = 7


def get_file_list(file_dir):
    """
    获取文件列表
    :param file_dir:
    :return:
    """
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(root, file))
    return L


def get_image_dict(image_file):
    """
    通过文件生成 对象 hash 值只计算一次， 加快处理速度。
    :param image_file:
    :return:
    """

    image_dict = dict()
    image_dict['path'] = image_file
    img = Image.open(image_file)
    image_dict['p_hash'] = ph.get_p_hash(img)
    image_dict['d_hash'] = dh.get_d_hash(img)
    image_dict['a_hash'] = ah.get_a_hash(img)
    return image_dict


def cala_image_similarity(image_dict_1, image_dict_2):
    """
    计算图片相似度
    :param image_dict_1:
    :param image_dict_2:
    :return:
    """

    if image_dict_1['path'] == image_dict_2['path']:
        return True

    result_ph = ph.compHashCode(image_dict_1['p_hash'], image_dict_2['p_hash'])
    result_dh = dh.compHashCode(image_dict_1['d_hash'], image_dict_2['d_hash'])
    result_ah = dh.compHashCode(image_dict_1['a_hash'], image_dict_2['a_hash'])
    # print('依据感知哈希算法计算相似度：{}/{}'.format(result_ph, 64))
    # print('依据差异哈希算法计算相似度：{}/{}'.format(result_dh, 64))
    # print('依据平均哈希算法计算相似度：{}/{}'.format(result_ah, 64))

    return result_ph > SIMILARITY_BAR_PH and result_dh > SIMILARITY_BAR_DH and result_ah > SIMILARITY_BAR_AH


def add_image_to_set(parent_queue, exist_image_set, pos_list):
    """
    将发现有问题的图片保存到 set 中， 以后就不需要重复读取这个图片了
    :param parent_queue:
    :param exist_image_set:
    :param pos_list:
    :return:
    """
    for j in pos_list:
        for i in range(AVERT_IMAGE_COUNT):
            exist_image_set.add(parent_queue[j + i]['path'])


def print_report(total_count, pos_all_list, parent_queue):
    """
    打印报告内容
    :param total_count:
    :param pos_all_list:
    :param parent_queue:
    :return:
    """

    print('\n\n--------------[报告开始]--------------------\n')
    print('共比较图片{}次'.format(total_count))

    print('共发现{}个相同的片段广告'.format(len(pos_all_list)))
    print('')
    count = 0
    for index in pos_all_list:
        pos_list = index
        count += 1
        print('第{}个相同片段起始位置是: {}'.format(count, pos_list))
        for j in pos_list:
            print('\t start[{}] --> end [{}] :'.format(j, j + AVERT_IMAGE_COUNT))

            for i in range(AVERT_IMAGE_COUNT):
                print('\t\t', parent_queue[j+i]['path'])
    print('\n\n--------------[报告结束]--------------------\n')


def queue_image_compare(image_item_list):
    """
    比较队列， 找出重复序列
    :param image_item_list:
    :return:
    """

    parent_queue = image_item_list

    parent_len = len(parent_queue)
    if parent_len <= AVERT_IMAGE_COUNT + NEXT_AVERT_WINDOW:
        print('Error: 输入队列的长度[{}]小于广告队列, 请检查。'.format(parent_len))
        return
    # 记录总比较次数
    total_count = 0

    # 记录所有重复片段的起始位置
    pos_all_list = []

    # 保存发现有问题的序列， 后续不对这些图片进行比较
    exist_image_set = set()

    # i 广告窗口队列的起始位置
    i = 0
    while i < parent_len - AVERT_IMAGE_COUNT:

        child_queue = parent_queue[i:i+AVERT_IMAGE_COUNT]
        current_index = i
        i += 1
        print('当前进度{}, {}/{}\t 窗口坐标 : [ {} ... {}]'.format(float(i) / (parent_len - AVERT_IMAGE_COUNT), i,
                                     (parent_len - AVERT_IMAGE_COUNT), current_index, current_index+AVERT_IMAGE_COUNT))
        # 如果该图片已经发现问题， 直接跳过
        if child_queue[0]['path'] in exist_image_set:
            print('\t该图片已经发现问题， 直接跳过 ', child_queue[0]['path'])
            continue

        # print('\t当前窗口坐标 : [ {} ... {}]'.format(current_index, current_index+AVERT_IMAGE_COUNT))
        start_pos_list = list()
        start_pos_list.append(current_index)

        # item 父队列进行比较的位置坐标
        item = current_index + AVERT_IMAGE_COUNT

        while item < parent_len - AVERT_IMAGE_COUNT:
            found_flag = True
            current_item = item
            item += 1

            if item - i < AVERT_IMAGE_COUNT + NEXT_AVERT_WINDOW :
                continue

            for j in range(AVERT_IMAGE_COUNT):
                # print('\t\t  ', child_queue[j], parent_queue[item])

                if child_queue[j]['path'] in exist_image_set or parent_queue[current_item+j]['path'] in exist_image_set:
                    print('\t该图片已经发现问题， 直接跳过 ', child_queue[j]['path'])
                    found_flag = False
                    continue
                total_count += 1
                if not cala_image_similarity(child_queue[j], parent_queue[current_item+j]):
                    found_flag = False
                    break
                else:
                    print('\t {}  {} 相同'.format( child_queue[j]['path'], parent_queue[current_item+j]['path']))

            if found_flag:
                start_pos_list.append(current_item)
                item += (AVERT_IMAGE_COUNT - 1)

        # 如果发现两个或者 两个以上的相同序列
        if len(start_pos_list) > 1:

            pos_all_list.append(start_pos_list)
            print('\t发现相同片段  ', 'start pos: ', start_pos_list)
            add_image_to_set(parent_queue, exist_image_set, start_pos_list)
            i += AVERT_IMAGE_COUNT - 1

    print_report(total_count, pos_all_list, parent_queue)


if __name__ == '__main__':

    # result = cala_image_similarity(get_image_dict('/Users/mac/tmp/test_split_image/demo2/140.jpg'),
    #                          get_image_dict('/Users/mac/tmp/test_split_image/demo2/148.jpg'))
    # print(result)
    #
    # result = cala_image_similarity(get_image_dict('/Users/mac/tmp/test_split_image/demo2/141.jpg'),
    #                          get_image_dict('/Users/mac/tmp/test_split_image/demo2/149.jpg'))
    # print(result)
    # result = cala_image_similarity(get_image_dict('/Users/mac/tmp/test_split_image/demo2/142.jpg'),
    #                          get_image_dict('/Users/mac/tmp/test_split_image/demo2/150.jpg'))
    # print(result)

    start = time.time()

    file_list = get_file_list(BASE_DIR)
    file_list.sort(reverse=False)
    image_item_list = list()
    for file_name in file_list:
        print(get_image_dict(file_name)['path'])
        image_item_list.append(get_image_dict(file_name))


    queue_image_compare(image_item_list)

    end = time.time()
    print('耗时{}秒'.format(end - start))




