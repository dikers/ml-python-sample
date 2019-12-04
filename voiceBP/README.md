# voiceBP
语音分类， 可以识别某一个人的声音， 或者不同语种的声音， 声音用mp3文件， 每个文件30秒左右， 可以制作100-200个声音文件， 进行训练。 

[声音文件特征生成](https://github.com/dikers/ml-python-sample/blob/master/voiceBP/splite_sound.py)
在python框架下，搭建简单三层(20,3,3)BP神经网络,通过对音频的MFCC系数的特征最大值进行学习，在较少训练次数下，实现对音频信号的识别。
特征提取以后， 可以用常用的分类算法进行分类。
[进行分类](https://github.com/dikers/ml-python-sample/blob/master/voiceBP/main.py)
