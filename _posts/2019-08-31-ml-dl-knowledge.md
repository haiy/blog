---
title: 机器学习和深度学习常见知识点
layout: post
---

## {{page.title}}

<p class="meta">31 August 2019</p>

ML&DL QA knowledge

Ref: https://nndl.github.io/

* [Q13 如何进行模型调优](#q13-如何进行模型调优)
* [Q14 简述下CNN,TextCNN的原理,1*1的filter有什么用](#q14-简述下cnntextcnn的原理11的filter有什么用)
* [Q8 RNN，LSTM，GRU的联系和区别，能否画出对应结构图](#q8-rnnlstmgru的联系和区别能否画出对应结构图)
* [Q8-1 LSTM的激活函数为什么分别采用了sigmoid和tanh，对mem信息和输入信息采用加法操作有什么好处？](#q8-1-lstm的激活函数为什么分别采用了sigmoid和tanh对mem信息和输入信息采用加法操作有什么好处)
* [Q15 表示学习是指的什么？](#q15-表示学习是指的什么)
* [Q1 什么是机器学习，如何运用机器学习，怎么高效的使用](#q1-什么是机器学习如何运用机器学习怎么高效的使用)
* [Q2 什么是梯度消失，如何解决](#q2-什么是梯度消失如何解决) 
* [Q3 GBDT和XGB的联系和区别有哪些](#q3-gbdt和xgb的联系和区别有哪些)
* [Q3-1 XGB有什么缺点？](#q3-1-xgb有什么缺点)
* [Q4 什么是过拟合，如何解决](#q4-什么是过拟合如何解决)
* [Q5 L1和L2正则化有什么特点，为什么，分别适合什么场景](#q5-l1和l2正则化有什么特点为什么分别适合什么场景)
* [Q6 什么是梯度优化，常见的优化算法有哪些？梯度提升和梯度下降有什么关系](#q6-什么是梯度优化常见的优化算法有哪些梯度提升和梯度下降有什么关系)
* [Q6-1 什么是线性模型，什么是非线性模型](#q6-1-什么是线性模型什么是非线性模型)
* [Q6-2 模型参数和超参数有什么区别](#q6-2-模型参数和超参数有什么区别)
* [Q6-3 miniBatch有什么好处](#q6-3-minibatch有什么好处)
* [Q15 BatchNormalization 和 LayerNormalization分别解决了什么问题？](#q15-batchnormalization-和-layernormalization分别解决了什么问题)
* [Q16 Bagging和Boosting分别适用什么场景？](#q16-bagging和boosting分别适用什么场景)


#### Q13 如何进行模型调优
A13 神经网络表达能力强，但也存在两大问题。非凸优化以及过拟合。
- 网络结构
- 优化算法
- 参数初始化
- 数据预处理
- 逐层归一化
- 超参优化
- 网络正则化

#### Q14 简述下CNN,TextCNN的原理,1*1的filter有什么用
A14 CNN指的是卷积神经网络的。其网络架构主要卷积层，池化层以及全链接层。以手写问题为例其计算过程主要如下：

#### Q8 RNN，LSTM，GRU的联系和区别，能否画出对应结构图
https://arxiv.org/pdf/1506.02078.pdf
https://arxiv.org/pdf/1412.3555.pdf 
先来说说RNN和LSTM以及GRU的区别。
- 1 相较于RNN，LSTM和GRU当前状态信息是在历史信息的基础上加上当前的信息，而RNN则是直接根据上一个信息算出的替换了之前的值。
- 2 累加的特性有多个优点。首先有助于从很长的步骤中学习到输入中存在的特征，因为每个内存单元学习到的知识不是直接被替换掉，而是累积起来。
- 3 加法操作能够让重要信息的梯度在多步传递过程中不会轻易消失，因为即使是sigmoid的函数使得某个输入门进入饱和区，但是因为内存单元是加法的，所以梯度的传递还是不会很快消失的。
再来看看LSTM和GRU的区别。其实二者的根本区别在于对输入信息和内存信息的处理方式上。
- 1 LSTM和GRU也是有区别的。 GRU相对于LSTM缺少的一点是对内存信息的使用程度的控制，也就是输出门。也就是说GRU完全将其内存信息完全传递给隐藏输出。
- 2 另一个区别就是输入门或者叫做重置门的位置。GRU单元对于从上一时间步骤传递到新的内存信息没有单独的控制。但是LSTM用了一个单独的遗忘门来独立控制添加到新的内存内容的信息。换种说法就是GRU只是在计算新的内存内容的时候来控制对上一步激活信息的使用，而没有单独控制上一步的激活信息要用多少。

#### Q8-1 LSTM的激活函数为什么分别采用了sigmoid和tanh，对mem信息和输入信息采用加法操作有什么好处？

A8-1 sigmoid主要是用在i,f,o三个门控单元上，之所以用sigmoid是因为其在值在0，1区间上并且可微，更符合门控单元的物理意义。而tanh其值区间在-1，1是用来对内存单元信息进行调整。加法操作能够在反向传播的过程中基本不会分散梯度，能让内存单元c的梯度反向传播很长区间而不打断。

#### Q15 表示学习是指的什么？
https://arxiv.org/abs/1206.5538

#### Q1 什么是机器学习，如何运用机器学习，怎么高效的使用
A1 机器学习是一种运用基于统计算法的从数据中挖掘业务价值的方法。其目前主要应用领域有计算广告，金融风控，智能交互等，目前定位宽泛点说可以是一种提高生产效率的工具。那么如何高效使用其实是和各个领域的业务问题有着密不可分的关系。根据具体的业务问题特点去选择合适的算法模型进行建模，然后得到比较有价值的模型。

#### Q2 什么是梯度消失，如何解决
A2 梯度消失这种现象主要出现在深度神经网络DNN和循环神经网络中。
- 1.1 在DNN全联接的网络结构中出现这种情况的根本原因是采用了Sigmoid和tanh
这类激活函数。这类激活函数具有数据压缩的特性，如sigmoid其取值范围在（0，1）间，其导函数f'在取值特别大或者特别小的时候梯度值很小几乎为0。因为DNN网络在优化过程中采用的是梯度下降优化算法，每一层的梯度计算输入都是前一层的梯度输出，因此在经过n层的传播压缩后，误差梯度几乎衰减为0，无法对参数进行有效学习。
- 1.2 针对DNN的这种情况，主要是对激活函数进行调整。引入了ReLU这样的激活算子，
具有更大的至于空间。
- 2.1 对于循环神经网络来说，出现这种情况的根本原因是其在多层之间的权重共享导致的。因为循环神经网络的设计目标是用一个权重矩阵来捕捉一定长度的序列之间的依赖关系，因此在进行梯度计算的反向求导过程中梯度变化和权重成指数关系。所以如果取了比较小的权重值后，会造成梯度消失，取了大于1的权重会造成梯度爆炸。这也是RNN无法捕捉较长序列间依赖关系的根源。
- 2.2 为了解决RNN的这种问题，对于梯度爆炸，引入了BPTT算法，对大值进行截断按比例规约。对于梯度消失，则是有多种方案。首先有类似LSTM，GRU等基于内存记忆的网络就随之产生了。其解决这个问题的思路是通过引入门控单元，来将信息存储在引入的内存单元变量上，以此弥补梯度消失带来的信息量的损失。另外一种是对前馈网络结构进行改变，通过残差学习的方式来缓解。

#### Q3 GBDT和XGB的联系和区别有哪些
A3 GBDT是梯度提升决策树的简称，属于集成学习里面boosting算法的一种。boosting的算法通常是由n个基准模型对数据进行连续学习，并通过重点关注前面模型分错的数据进行模型调整，从而达到学习目标的。GBDT也是类似流程，不过其主要是通过学习模型预测结果和实际值之间的残差来进行模型训练。CART回归树来作为基础模型。XGB也是GBDT模型的一种。其相对于典型的GBDT主要有以下几点：
- 1 XGB模型的损失函数中加入了正则项来对模型进行过拟的调整，而GBDT则是通过后剪枝的方式的进行模型泛化能力的调整
- 3 XGB的损失函数中用到了二阶导数信息，而GBDT则是只用了一阶导数。
- 2 GBDT中节点的分裂条件通常是和基本的树类算法一致的，比如Gini系数，信息增益比等。而XGB中节点的分裂方式则是通过判定按照特定位置进行分裂能否带来最大的损失函数提升来的。
- 4 XGB的基础函数支持了更为丰富
- 5 对样本的使用上，XGB支持了数据的采样，而GBDT则是全样本
- 6 XGB支持了对缺失样本，而GBDT不支持。

#### Q3-1 XGB有什么缺点？
A3-1 XGB的不足之处主要表现在三个方面：
- 1 不同颗树的生成必须是顺序的，会有一定性能瓶颈
- 2 对稠密的结构化数据处理效果较好，对于高维稀疏数据的表现不如支持向量机
- 3 对于文本类数据则效果不佳

#### Q4 什么是过拟合，如何解决
过拟合是指模型学到了训练数据中比较特异性的特征，在训练数据表现很好，在测试数据和其他数据表现很差。
对于传统模型比较通用的解决方法有
- 1 添加数据，通过丰富数据
- 2 采用更简单些的模型，降低模型容量，如对树类模型，降低树的深度
- 3 进行正则化，对模型进行优化
- 4 采用集成学习的模型，如bagging类模型，降低模型方差，提高泛化能力
对于深度学习模型来说，其可以采用的方法有
- 1 调整网络结构，采用较少的网络节点
- 2 对损失函数加入正则项
- 3 训练过程引入dropout策略，在训练时随机丢弃部分节点，以达到类似bagging的效果
- 4 加入验证集提前停止策略，如果在验证集上的效果提升达到预期就停止

#### Q5 L1和L2正则化有什么特点，为什么，分别适合什么场景
L1和L2正则化都是对通过添加在目标函数后对模型参数空间进行调整的方法。L1倾向于将模型参数稀疏化，有特征选择的作用。L2则倾向于对不重要的特征赋予较低的权重值，对模型参数进行平滑。之所以能产生如此的效果和L1，L2的计算方式以及和目标函数的结合方式有关。函数加和的效果等效于对目标函数的求解加上了对应的限制条件。因此权重的分布空间就是在L1，L2的限定空间内。

Q6 有哪些正则化方法？(针对过拟合有什么解决办法？)
https://arxiv.org/pdf/1611.03530.pdf
https://arxiv.org/pdf/1710.05468.pdf
- L1L2
- weight decay, 引入权重衰减系数，对学习速率进行衰减
- early stop, 用单独验证集上数据的表现来确定模型训练效果
- dropout, 训练过程随机丢弃一些神经元。设定一个概率p，对每个神经元都判定是否丢弃.具体做法是引入一个mask丢弃函数。训练时根据概率p生成的由伯努利分布产生的丢弃掩码来判定是否要丢弃当前神经元。在测试时，因为训练时的平均神经单元数是原先的平均p倍，而测试如果用全量的神经元的话就会造成输入分布不一致，为了缓解这个问题，测试时需要将神经元的输入乘以P。
对循环神经网络来说，dropout的话不能在循环层进行，这样会破坏记忆。因此是在输入和
和输出阶段进行随机丢弃。
- data augmentation
- label smoothing. 标签中有错误数据，对此进行加入噪声的方式来避免过拟合。0，1整形的数据标签可以看作是硬目标，若是softmax分类器交叉熵作为损失函数
- batch normlization 

#### Q6 什么是梯度优化，常见的优化算法有哪些？梯度提升和梯度下降有什么关系
梯度优化是指用梯度变化信息求解目标函数在特定约束下最优解的过程。在函数的最优解求解一般有凸函数和非凸函数两种。对于凸函数来说，其有全局唯一最优解，而对于非凸函数则是有多个局部最优解。梯度优化就是求解函数最优解的一种方法。

#### Q6-1 什么是线性模型，什么是非线性模型
线性分类器是指对于由模型函数为0解的特征空间组成的一个线性分类超平面。简单来说，分类边界是线性超平面的就是线性模型，反之为非线性模型。

#### Q6-2 模型参数和超参数有什么区别
模型本身的参数，可以通过学习得到的。超参数是定义模型结构或者优化过程的，这类是超参数。超参数的最优解是一个组合优化过程，学习不到。

#### Q6-3 miniBatch有什么好处
A6-3 miniBatch的好处主要是相对单个样本和全部样来说的
- 1 miniBatch的梯度相比单个样本来说，其更接近于整体样本的梯度期望，batchSize越大越接近。
- 2 小批量相比全部的计算效率要高

#### Q15 BatchNormalization 和 LayerNormalization分别解决了什么问题？
A15 
- 1 BN出现提高了学习速率，减轻了初始化权重对模型参数梯度变化的影响，同时bn也有正则化的效果可以降低对dropout的需求。之所以有这样的效果，是因为我们在DNN随机梯度优化的过程中，存在着内部协方差偏移的问题。具体来说就是模型的前一层的输出是后一层的输入，那么在训练过程中，输入数据分布的轻微变化会造成后一层模型参数的变化，随着层数的增加，这个变化会不断放大，会造成激活函数的饱和。https://arxiv.org/pdf/1502.03167.pdf
不足之处在于，BN求的是移动均值，面向的数据是固定维度，所以不适用于BatchSize特别小，以及RNN一类的模型。

- 2 LN是针对BN的不足设计的。其和BN的核心区别点在于计算方式的不同。其主要解决的是在面对RNN一类模型时的效果。


二者的计算方式的区别是一个是针对Batch内的每个特征维度，LN则是针对Batch内的每个样本维度。

#### Q16 Bagging和Boosting分别适用什么场景？
A16 bagging主要目标是降低目标函数的方差，并行化好，训练速度快。boosting
则是针对学错的数据不断进行修正，模型的偏差小。因此在过拟合不严重的情况下可以用boosting类算法提高效果，数据不足的情况下可以bagging的方式防止过拟合。