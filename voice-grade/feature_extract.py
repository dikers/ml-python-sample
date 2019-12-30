from __future__ import print_function
import time
import boto3
import json
import os
from synonym import Synonym

# 大于threshold_rate 算相似
threshold_rate = 0.45

class FeatureExtract:


    def __init__(self, word_vec_file_path, right_content):
        self.comprehend_client = boto3.client('comprehend')
        self.word_type_name_list = ['NOUN']
        self.score_dict = self.get_score_dict()
        self.right_content = right_content
        self.synonym = Synonym("./target/vec.txt", threshold_rate)

    @staticmethod
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

    def read_json_file(self, file_path):
        """

        :param file_path:
        :return:
        """
        with open(file_path, "r") as f:
            new_dict = json.load(f)

        return new_dict['results']['transcripts'][0]['transcript']

    def create_word_dict(self, content):

        result = self.comprehend_client.detect_syntax(Text= content, LanguageCode='en')
        result = result['SyntaxTokens']
        word_type_dict = dict()

        for item in result:
            tag_name = item['PartOfSpeech']['Tag']
            if tag_name not in self.word_type_name_list:
                continue

            item_set = word_type_dict.get(tag_name)
            if item_set is None:
                item_set = set()

            item_set.add(item['Text'].lower())
            word_type_dict[tag_name] = item_set

        for item in word_type_dict.items():
            print('\t', item)
        return word_type_dict

    def read_all_file(self, file):
        """
        item（content, word_count ,word_dis_count,  word_type_dict ）
        :param file:
        :return:
        """

        print(self.right_content)
        word_dict = self.create_word_dict(self.right_content)
        _word_dict_list = list()

        count = 0
        for root, dirs, files in os.walk(file):
            for f in files:
                print('\n', os.path.join(root, f))
                content = self.read_json_file(os.path.join(root, f))
                if count >10:
                    continue
                count +=1
                word_count = len(content.split(' '))
                word_dis_count = len(set(content.split(' ')))
                print('word_count{}  word_dis_count {}'.format( word_count, word_dis_count))
                word_type_dict = (f.split('.')[0], word_count, word_dis_count,  self.create_word_dict(content), content)
                _word_dict_list.append(word_type_dict)
        return _word_dict_list


    def get_sim_score(self, base_list, new_list):
        """
        获取相似度得分
        :param base_list:
        :param new_list:
        :return:
        """

        total_score = 0
        for j in new_list:
            if j in base_list:
                total_score += 1.0
            else:
                synonym_list = self.synonym.cal_item_sim(j)
                if synonym_list is None:
                    continue
                for syn_word in synonym_list:
                    if syn_word[0] in base_list:
                        total_score += float(syn_word[1])
                        print('word {} - > syn_word{}  score: {}'.format(j,  syn_word, total_score))
                        break
        return float('%.2f' % total_score)

    def run(self):

        word_dict_list = self.read_all_file('./dataset')
        count_index = 0
        base_item = self.create_word_dict(self.right_content)
        for word_type_name in self.word_type_name_list:
            print('-------------- {}---------------- '.format(word_type_name))
            tmp_item = sorted(list(base_item[word_type_name]))
            score_dict = self.get_score_dict()

            for item in word_dict_list:
                words = sorted(list(item[3][word_type_name]))
                sim_score = self.get_sim_score(tmp_item, words)

                print('学生编号: {}\t 得分: {}\t 单词个数：{} 不重复单词个数：{} \t相似度{}'.format(item[0], score_dict[item[0]],  item[1], item[2], sim_score))
                count_index += 1


if __name__=='__main__':

    _right_content = """It was a sunny day during last summer vacation. Ming practiced speaking English the whole morning. After that, he went to take piano lessons. Then his father took him to the art school to learn painting. Ming didn't have a rest until the evening. Unfortunately, he was so stressed out that he felt terrible. His parents sent him to hospital. And the doctor said Ming had a bad fever and should lie down and rest."""
    featureExtract = FeatureExtract("./target/vec.txt", _right_content)
    featureExtract.run()

    print('------------------------------ end')













