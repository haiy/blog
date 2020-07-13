---
title: parameter server架构分析  
layout: post
---

## {{page.title}}

<p class="meta">08 Aug 2018</p>

* [简介](#简介)
* [架构](#架构)
     * [集群角色和分组](#集群角色和分组)
     * [数据结构](#数据结构)
     * [数据传输,range pull and push](#数据传输range-pull-and-push)
     * [server端自定义参数的处理函数](#server端自定义参数的处理函数)
     * [任务的异步执行和依赖](#任务的异步执行和依赖)
     * [灵活的一致性](#灵活的一致性)
* [实现细节](#实现细节)
* [论文](#论文)
* [ali impl](#ali-impl)
* [其他相关]()
    * [autoML](#automl)
    * [ZMQ](#zmq)
    * [hyperparameter optimize](#hyperparameter-optimize)
    * [dist ml](#dist-ml)
    * [doc related](#doc-related)
    * [impl](#impl)
    * [zero MQ](#zero-mq)
    * [chain replication](#chain-replication)
    * [Consistency hash](#consistency-hash)
    * [spark internals](#spark-internals)
    * [how to read  code](#how-to-read--code)    
    * [learn IoC with basic spring](#learn-ioc-with-basic-spring)
    * [d3.js](#d3js)


## 简介 
* 源码git: <https://github.com/dmlc/ps-lite>
* 论文：<https://book.haihome.top/distribute/parameter_server_osdi14.pdf>
* 简介: 参数服务器是一个分布式的模型训练框架，其设计目标是为了满足超大规模参数模型高效训练。所谓的超大规模指的是参数信息单机已经无法存储。其核心的设计点是将参数按序切片分布式存储，模型参数更新方式支持同步，异步以及混合方式，可以通过控制参数来实习。
* 贡献点：基于机器学习系统架构抽象，支持应用级别的精确自定义。同时其定位系统层优化的共享平台，其提供对多种算法的实现能力和分布式框架。
* 核心优点： 异步的参数高效通信，灵活的一致性模型，弹性的伸缩能力，容错和持久，易用性
* 参数通信的核心是将参数视作有序数据对，然后进行切片。容错则是采用了链式备份。
* 应用场景: 模型参数巨大


## 架构

### 集群角色和分组

- ps集群是由一个server组和不同的worker组组成。因此可以支持同时运行超过一个算法。一个server节点维护了全局参数的一个partition。一个server管理节点负责server的状态维护和参数数据分发。
- 每个worker组运行一个应用。每个worker组都有一个scheduler节点来管理任务进度以及机器状态。
- ps支持独立的参数命名空间，也就是server端支持参数空间的隔离。
- 可以实现离线训练和在线更新的数据共享。可是问题是在真实线上环境中允许离线和线上环境有交叉么？
- 什么是parameter namespace？worker group可以共享namespace。其本质是server端的空间隔离。
- 任务分配，server组存储参数，worker组执行训练任务，更新参数，相互独立只和server有交互。

### 数据结构

基于有序kv的vectors

### 数据传输,range pull and push

基于kv对中的key的range进行数据交换

### server端自定义参数的处理函数

### 任务的异步执行和依赖

### 灵活的一致性

在系统高效和不一致性敏感之间让算法设计者能够灵活自定义自己一致性模型。目前可支持三种模式: 顺序，最终，有限延迟(有个比较典型的KKT算法)。

## 实现细节

- server端采用一致性哈希算法来存储kv值。用chain rule算法来容错。为基于range的通信方式进行优化进行的数据压缩和range based 向量时钟。
- vector clock： 每个节点都有自己的一个vc，是全局的贯穿不同的namespace的。
- messages： [vc(R),(k1, v1), . . . ,(kp, vp)] kj ∈ R and j ∈ {1, . . . p}
- consistient hashing:a directed DHT design. server manger管理着hash ring。所有其他节点都本地缓存。
- Replication and Consistency： 为降低网络流量，在参数合并后进行复制。
- Server Management：分新key range，fetch更新自己的master key range值，提供k个slave range。server manager广播节点更新。
- worker management： 分发数据，加载训练数据，拉取参数，task scheduler广播更新

## 论文

<iframe width="800" height="450" src="https://book.haihome.top/distribute/parameter_server_osdi14.pdf" frameborder="0">
</iframe>


## ZMQ

install pyzmp
- [doc](http://zeromq.org/bindings:python)
- [zmq pattern,这个很好](http://learning-0mq-with-pyzmq.readthedocs.io/)
- [Great ppt](https://www.slideshare.net/fcrippa/europycon2011-implementing-distributed-application-using-zeromq)
- [pyzmq](https://pyzmq.readthedocs.io/en/latest/)
- [python-multiprocessing-with-zeromq](https://taotetek.net/2011/02/02/python-multiprocessing-with-zeromq/)
- [python-multiprocessing-zeromq-vs-queue/](https://taotetek.net/2011/02/03/python-multiprocessing-zeromq-vs-queue/)
- [zguid](https://github.com/booksbyus/zguide)
- [deeper large size hang](https://stackoverflow.com/questions/8905147/why-does-this-python-0mq-script-for-distributed-computing-hang-at-a-fixed-input)
- [from-kafka-to-zeromq-for-log-aggregation](https://tomasz.janczuk.org/2015/09/from-kafka-to-zeromq-for-log-aggregation.html)
- [Why should I have written ZeroMQ in C, not C++ (part I)
](http://250bpm.com/blog:4)
- [what-are-zeromq-use-cases](https://stackoverflow.com/questions/4499510/what-are-zeromq-use-cases)

## autoML

- [github](https://github.com/automl)
- [auto sklearn](http://automl.github.io/auto-sklearn/stable/)
- [tpot](https://github.com/EpistasisLab/tpot)

### hyperparameter optimize

- [HPOlib](https://github.com/automl/HPOlib)
- [fastml compare](http://fastml.com/optimizing-hyperparams-with-hyperopt/)
- [Towards an Empirical Foundation for
Assessing Bayesian Optimization of Hyperparameters](http://www.cs.ubc.ca/~hutter/papers/13-BayesOpt_EmpiricalFoundation.pdf)
- [hyperopt](https://github.com/hyperopt/hyperopt)
- [Spearmint](https://github.com/HIPS/Spearmint)

## dist ml
- [Strategies and Principles of Distributed Machine Learning on Big Data](https://www.petuum.com/pdf/Xing_Engineering16.pdf)
- [zhihu](https://www.zhihu.com/people/niu-chong/activities)
- [intro dml](https://medium.com/@Petuum/intro-to-distributed-deep-learning-systems-a2e45c6b8e7)
- [petuum blog](http://www.petuum.com/blog.html)
- [h2o.ai](https://www.slideshare.net/0xdata/h2o-world-2017-keynote-sri-ambati-ceo-cofounder-h2oai)
- [PMLS doc](http://pmls.readthedocs.io/en/latest/)
- [petuum vs spark](https://www.quora.com/What-is-the-difference-between-Spark-and-Petuum)
- [poseidon](http://poseidon-release.readthedocs.io/)
- [xunzhang douban](http://xunzhangthu.org/)
- [paracel quick_tutorial](http://paracel.io/docs/quick_tutorial.html)
- [Paracel十问](https://www.douban.com/note/491307203/)
- [Petuum note](https://github.com/JerryLead/blogs/tree/master/BigDataSystems/Petuum)
- [jerrylead](http://www.cnblogs.com/jerrylead)
- [zhihu dml zhuanlan](https://zhuanlan.zhihu.com/p/29032307)
- [Tencent angel](https://github.com/Tencent/angel)

## doc related

- [ps paper](https://book.haihome.top/distribute/parameter_server_osdi14.pdf)
- [ps-lite github](https://github.com/dmlc/ps-lite)
- [ray ps](http://ray.readthedocs.io/en/latest/example-parameter-server.html)
- [spark ps](https://databricks.com/session/glint-an-asynchronous-parameter-server-for-spark)
- [ps lite doc](http://ps-lite.readthedocs.io/en/latest/overview.html)
- [paper中文note](https://www.zybuluo.com/Dounm/note/517675)
- [源码解析](https://www.zybuluo.com/Dounm/note/517675)
- [li-mu ppt](http://www.mlss2014.com/files/Li/introduction.pdf)
- [li-mu optimization](http://www.mlss2014.com/files/Li/optimization.pdf)
- [parameter_server](http://www.mlss2014.com/files/Li/parameter_server.pdf)

## impl

- [ps 1](https://github.com/ArtHackDay-Plus1/ParameterServer)
- [ps 2](https://github.com/wenjunpku/ParameterServer)

## zero MQ
- [Great PPT](https://www.slideshare.net/fcrippa/europycon2011-implementing-distributed-application-using-zeromq)
- [office site](http://zeromq.org/)
- [github](https://github.com/zeromq/libzmq)

## chain replication

- [paper](http://www.cs.cornell.edu/home/rvr/papers/OSDI04.pdf)
- [brief history](https://book.haihome.top/distribute/QConSF2015-ChristopherMeiklejohn-ABriefHistoryofChainReplication.pdf)
- [intro blog](http://dsrg.pdos.csail.mit.edu/2013/08/08/chain-replication/)

## Consistency hash

- [blog](http://yikun.github.io/2016/06/09/%E4%B8%80%E8%87%B4%E6%80%A7%E5%93%88%E5%B8%8C%E7%AE%97%E6%B3%95%E7%9A%84%E7%90%86%E8%A7%A3%E4%B8%8E%E5%AE%9E%E8%B7%B5/)

## spark internals

- [SparkInternals](https://github.com/JerryLead/SparkInternals)

## how to read  code
- [如何阅读一份代码](https://zhuanlan.zhihu.com/p/26222486)

## ali impl

- [如何搭建大规模机器学习平台？以阿里和蚂蚁的多个实际场景为例](https://yq.aliyun.com/articles/59941)
- [ali dml ppt](https://book.haihome.top/distribute/ali-dml-ppt.pdf)

<iframe src="https://book.haihome.top/distribute/ali-dml-ppt.pdf" width="800" height="500"> </iframe>

### learn IoC with basic spring 

[simple-spring](https://github.com/Yikun/simple-spring)

## d3.js

[big one d3](https://bost.ocks.org/mike/)


```python

```
