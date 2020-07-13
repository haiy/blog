---
title: 如何解决90%的NLP问题
layout: post
---

{{page.title}}
=============

<p class="meta">14 Mar 2018</p>

Table of Contents
=================
   * [NLP问题实际应用](#nlp问题实际应用)
   * [本文期望目标](#本文期望目标学会如何做下面的事情)
   * [具体步骤](#具体步骤)
      * [1 GatherData](#1-gatherdata)
      * [2 Clean data](#2-clean-data)
      * [3 Find a good data representation](#3-find-a-good-data-representation)  
        * [a One-hot encoding (Bag of Words)](#a-one-hot-encoding-bag-ofwords)   
        * [b Visualizing the embeddings](#b-visualizing-the-embeddings)
      * [4 Classification](#4-classification)
      * [5 Inspection](#5-inspection)
      * [6 Accounting for vocabulary structure](#6-accounting-for-vocabulary-structure)
      * [7 Leveraging semantics](#7-leveraging-semantics)
      * [8: Leveraging syntax using end-to-end approaches](#8-leveraging-syntax-using-end-to-end-approaches)
   * [Final Notes](#final-notes)
   * [Refs](#refs)

 简单来说，主要是对词的表示形式的变化，从基本的词频->词嵌套->TF-IDF->词向量->整句。也就是将词和词，词和句的关系一步一步
 从单个数字表示扩展为1维向量然后再进一步延伸成2维向量来建模。本文比较有意思的地方是为了提高模型的可解释性，采用了一个新的
 工具Lime。它不需要知道是什么模型，其简单的原理是直接去掉部分特征然后看对模型效果的影响，其实质上是一个wrapper的特征选择
 过程可视化。还是比较值得尝试。

# NLP问题实际应用
    情绪正负识别，用户识别，意图识别分类

# 本文期望目标，学会如何做下面的事情
    收集,准备,探查数据
    构建简单的模型来开始，并且如果有必要的话迁移到深度学习
    翻译和理解你的模型，确保真正获得的是有效信息而不是噪音

# 具体步骤
## 1 GatherData
对于数据的label: 不要尝试用无监督来构建标签，直接花一星期时间来标注

## 2 Clean data
* 		Remove all irrelevant characters such as any non alphanumeric characters
* 		Tokenize your text by separating it into individual words
* 		Remove words that are not relevant, such as “@” twitter mentions or urls
* 		Convert all characters to lowercase, in order to treat words such as “hello”, “Hello”, and “HELLO” the same
* 		Consider combining misspelled or alternately spelled words to a single representation (e.g. “cool”/”kewl”/”cooool”)
* 		Consider lemmatization (reduce words such as “am”, “are”, and “is” to a common form such as “be”)

## 3 Find a good data representation
#### a One-hot encoding (Bag of Words)
先构建词典，然后直接统计词频，构建一句的词向量。

￼<img src="/images/general_nlp/embedding.png"  height="135px">

#### b Visualizing the embeddings
目标：确认embedding有没有捕获到和我们问题相关的信息
采用PCA 投影到2维空间可视化

## 4 Classification
先用logisticRegression尝试下分类，尝试去分析这个模型效果代表的意义

## 5 Inspection
Confusion Matrix:
   
    － false postive-> 把负样本错误的分到正类了
    － false negative -> 把正样本错误的分到负样本
    
确认是对哪个错误更敏感

根据LR分别确定对正负类来说最重要的词。建模参数：

```python
clf_w2v = LogisticRegression(C=30.0, class_weight='balanced', solver='newton-cg', 
                         multi_class='multinomial', random_state=40)
clf_w2v.fit(X_train_word2vec, y_train_word2vec)
y_predicted_word2vec = clf_w2v.predict(X_test_word2vec)
```

## 6 Accounting for vocabulary structure
进一步采用TF-IDF对文本进行处理，根据得到的向量再做一次关键字分析，查看模型的效果。这次同样可以
看到每个词的重要性情况。判定其是否符合认知。

## 7 Leveraging semantics
采用word2vec将词和词之间的语义关系表示成一个300维的向量，
对一段文本来说，将其中包含的词的词向量做均值得到该段文本的表示。

￼<img src="{{site.url}}/images/general_nlp/lookup_table.png"  height="200px" >


The Complexity/Explainability trade-off
但是采用word2vec之后模型的可解释性就直接降低了，为了确定模型的关键影响因素，采用LIME对黑盒模型进行进一步的尝试解释。

## 8: Leveraging syntax using end-to-end approaches

先将词转为词向量然后每个短文本作为一个完整的二维数据来进行处理。然后在此基础上用CNN来进行建模。

￼￼<img src="{{site.url}}/images/general_nlp/arch.jpg"  height="230px">

# Final Notes

* 		Start with a quick and simple model
* 		Explain its predictions
* 		Understand the kind of mistakes it is making
* 		Use that knowledge to inform your next step, whether that is working on your data, or a more complex model.


# Refs:           
   blog:<https://blog.insightdatascience.com/how-to-solve-90-of-nlp-problems-a-step-by-step-guide-fda605278e4e>         
   code: <https://github.com/hundredblocks/concrete_NLP_tutorial/blob/master/NLP_notebook.ipynb>  
   Convolutional Neural Networks for Sentence Classification: <https://arxiv.org/abs/1408.5882>                 
   模型的可解释性问题: <http://www.csdn.net/article/2015-08-17/2825471>                   
   Lime: <https://github.com/marcotcr/lime>, <http://geek.csdn.net/news/detail/66259>                  
   ExplainingThePredictionsOfAnyClassifier: <https://arxiv.org/abs/1602.04938>                  
   word2vec: <https://arxiv.org/pdf/1301.3781.pdf>                  
   tf-idf : <https://en.wikipedia.org/wiki/Tf–idf>                    
   sklearn tf-idf: <http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction>                                                         
   data: <https://www.crowdflower.com/data-for-everyone/>                                        
   PCA: <https://en.wikipedia.org/wiki/Principal_component_analysis>                

