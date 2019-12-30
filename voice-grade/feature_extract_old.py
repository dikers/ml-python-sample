from __future__ import print_function
import time
import boto3
import datetime
import urllib
import json
import os

def read_all_file(file):
    comprehend_client = boto3.client('comprehend')

    right_content = """It was a sunny day during last summer vacation. Ming practiced speaking English the whole morning. After that, he went to take piano lessons. Then his father took him to the art school to learn painting. Ming didn't have a rest until the evening. Unfortunately, he was so stressed out that he felt terrible. His parents sent him to hospital. And the doctor said Ming had a bad fever and should lie down and rest."""
    print(right_content)
    word_dict = create_word_dict(right_content, comprehend_client)
    word_dict_list = list()

    word_dict_list.append(word_dict)
    score_list = list()

    for root, dirs, files in os.walk(file):
        for f in files:
            print('\n', os.path.join(root, f))
            content = read_json_file(os.path.join(root, f))
            print(len(content), '   ',  content)
            word_dict = create_word_dict(content, comprehend_client)
            word_dict_list.append(word_dict)
            score_list.append(f.split('.')[0])
    return word_dict_list, score_list




def read_json_file(file_path):

    with open(file_path, "r") as f:
        new_dict = json.load(f)

    return new_dict['results']['transcripts'][0]['transcript']


def create_word_dict(content, comprehend_client):

    result = comprehend_client.detect_syntax(Text= content, LanguageCode='en')
    result = result['SyntaxTokens']
    word_dict = dict()

    for item in result:
        tag_name = item['PartOfSpeech']['Tag']
        if tag_name == 'PUNCT':
            continue
        # print(item)
        item_set = word_dict.get(tag_name)

        if item_set is None:
            item_set = set()

        item_set.add(item['Text'].lower())
        word_dict[tag_name] = item_set


    for item in word_dict.items():
        print(item)
    return word_dict


def compare_list(base_list, new_list):

    total_count = len(base_list)

    tmp_count = 0
    for j in new_list:
        if j in base_list:
            tmp_count += 1

    return float('%.2f' % (tmp_count/total_count))



def run(word_type_name_list):

    word_dict_list, score_list = read_all_file('./dataset')
    print('--------------  word_dict_list: ', len(word_dict_list))
    count_index = 0
    base_item = word_dict_list[0]
    word_dict_list = word_dict_list[1:]
    for word_type_name in word_type_name_list:
        print('-------------- {}---------------- '.format(word_type_name))
        tmp_item = sorted(list(base_item[word_type_name]))
        score_dict = get_score_dict()

        for item, student_id in zip(word_dict_list, score_list):
            words = sorted(list(item[word_type_name]))
            print('相似度: {}\t 得分{}\t 学号： {} 单词个数： {} \t{}'.format(compare_list(tmp_item, words), score_dict[student_id], student_id, len(words), words))
            count_index += 1


def get_score_dict():
    score_dict = dict()
    score_dict['184190001'] = 4
    score_dict['184190003'] = 3
    score_dict['184190010'] = 4
    score_dict['184190020'] = 4
    score_dict['184190045'] = 4

    score_dict['184190058'] = 3
    score_dict['184190071'] = 3.5
    score_dict['184190081'] = 4
    score_dict['184190109'] = 4
    score_dict['184190151'] = 3.5

    score_dict['184190170'] = 4
    score_dict['184190177'] = 4
    score_dict['184190189'] = 4
    score_dict['184190199'] = 3.5
    score_dict['184430141'] = 3.5
    return score_dict



if __name__=='__main__':
    word_type_name_list = ['NOUN', 'VERB']
    run(word_type_name_list)













