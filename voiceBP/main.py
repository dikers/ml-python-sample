# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:20:40 2019

@author: lei
"""
import BP
import datahelper as dh

if __name__ == '__main__':
    print('start --------------------------- ')
    bp = BP.BPNeuralNetwork()
    bp.setup(20, 200, 2)
    x = dh.load('./dataset/x.txt')
    y = dh.load('./dataset/y.txt')
    x, y = dh.shuffer(x, y)
    x = dh.normalization(x)
    train_list, test_list = dh.data_split(x, y, 0.7)
    bp.train(train_list, test_list, 500, 0.05, 0.1)
    bp.save('%f.h7' % (bp.test_acc))
