#-*-coding:utf8-*-
"""
author:david
date:2018****
produce item sim file
"""

import os
import numpy as np
import operator


class Synonym:
    def __init__(self, word_vec_file_path, threshold_rate=0.6):
        self.threshold_rate = threshold_rate
        self.word_vec_file_path = word_vec_file_path
        self.item_vec = self._load_item_vec(self.word_vec_file_path)

    @staticmethod
    def _load_item_vec(input_file):
        """
        Args:
            input_file: item vec file
        Return:
            dict key:itemid value:np.array([num1, num2....])
        """
        if not os.path.exists(input_file):
            return {}
        linenum = 0
        item_vec = {}
        fp = open(input_file)
        for line in fp:
            if linenum == 0:
                linenum += 1
                continue
            item = line.strip().split()
            if len(item) < 129:
                continue
            itemid = item[0]
            if itemid == "</s>":
                continue
            item_vec[itemid] = np.array([float(ele) for ele in item[1:]])
        fp.close()
        return item_vec

    def cal_item_sim(self, itemid):
        """
        Args
            item_vec:item embedding vector
            itemid:fixed itemid to clac item sim
            output_file: the file to store result
        """
        if itemid not in self.item_vec:
            return
        score = {}
        topk = 10
        fix_item_vec = self.item_vec[itemid]
        for tmp_itemid in self.item_vec:
            if tmp_itemid == itemid:
                continue
            tmp_itemvec = self.item_vec[tmp_itemid]
            fenmu = np.linalg.norm(fix_item_vec) * np.linalg.norm(tmp_itemvec)
            if fenmu == 0:
                score[tmp_itemid] = 0
            else:
                score[tmp_itemid] =  round(np.dot(fix_item_vec, tmp_itemvec)/fenmu, 3)
        out_str = itemid + "\t"
        # print(out_str)
        synonym_list = []
        for zuhe in sorted(score.items(), key=operator.itemgetter(1), reverse=True)[:topk]:
            if zuhe[1] > self.threshold_rate:
                synonym_list.append(zuhe)
                # print('{} :  {}'.format(zuhe[0], zuhe[1]))

        return synonym_list


if __name__ == "__main__":

    synonym = Synonym("./target/vec.txt", 0.45)
    synonym.cal_item_sim('get')
