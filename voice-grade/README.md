#  判断语音得分

### 步骤
1.  Transcribe. 语音转文本
2.  英语语法分析 找出有语法错误的句子
3.  用Amazon Comprehend 按照词性进行分类
4.  提取特征  名词形似度  动词相似度  单词个数 语法错误数等， 然后根据得分， 进行机器学习训练


### 编译word2vec distance

word2vec 用来讲单词转换成词向量， 用来计算单词间的距离， 距离近的相似度高。 

```shell script
# 源码下载地址
#wget https://code.google.com/archive/p/word2vec/source/default/source

cd word2vec

make word2vec distance
mv word2vec ../target/
mv distance ../target/

```


###  训练单词相似度矩阵

'../target/english_train.txt'   训练的数据集
'../target/vec.txt' 是生成好的相似度矩阵

```shell script

cd shell
./train.sh '../target/english_train.txt'   '../target/vec.txt'
```



###  特征提取

```
python feature_extract.py

```
