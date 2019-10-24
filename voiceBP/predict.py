# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 09:20:40 2019

@author: lei
"""
import BP
import datahelper as dh

if __name__ == '__main__':
    print('start ---------------------- ')
    bp = BP.BPNeuralNetwork()

    bp = bp.load('1.000000.h7')
    inputs = [-55.03368,215.3841,97.02559,154.21176,86.06147,66.7886,44.5021,48.164444,31.047588,38.115547,46.489082,16.503178,39.60366,29.442366,37.703796,45.399925,48.772804,49.458755,38.72352,62.047348]

    print(bp.predict(inputs))
