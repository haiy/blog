---
title: tensorflow note
date: 2017-06-19 00:00:00 Z
layout: post
---

{{page.title}}
=============

<p class="meta">19 June 2017</p>

### 基本概念

operation: 计算逻辑

Kernels：operation在特定设备类型上的具体实现

node:instantiation of an operation

tensor: operation的输入和输出数据形式

client: 用户编写的计算图

master:       
-1. 根据session run对图进行裁剪得到子图        
-2. 将子图分割成小片到不同的进程和设备上       
-3. 分发计算图块到worker service
-4. 初始化worker service图的执行

worker:    
-1. 根据实际的设备用对应的kernel实现来调度执行图的operation
-2. 发送和接收其他worker的数据

master session: 

客户端程序和Tensorflow的交互接口。主要方法是extend和run。

1. node和device的分配对应关系处理

2. 为了支持跨设备和跨进程的数据流增加中间节点和边，send和receive，feed和fetch

3. 发送执行命令到关联的workers

variables:

variable是特殊的一种在整个图计算结束后返回的一个可修改的持久化数据。而大部分tensor在只存在计算过程中，计算完就没有了。

### 实现

client通过session和master及workers通信.每个worker用本地对应的设备来执行master分配的图节点。

### 单设备

client master worker都在同一个进程中，根据拓扑排序构建依赖关系，按照依赖顺序执行。

### 多设备

和单设备的区别点:
- a. 需要确定node分配策略
- b. node之间的通信策略

### 跨设备通信

1. 每个设备一个子图            
2. 跨设备的边被替换成Send和Recv节点         

### 分布式和多设备的区别

不同worker service之间的数据交换是TCP或者RDMA


### 分布式的容错机制

错误类型

1. node的数据发送和接收出错
2. master或者worker的心跳失联

容错机制:出错后中止计算从最新的checkpoint开始重新算

### 梯度计算

1. 内置operation。在使用了求梯度的operation后，会自动根据loss用链式法则算出其对应依赖的输入的偏导数。   
2. 内存使用较大，因为反向的时候需要所有数据。

### 控制流

Switch,Merge根据boolean跳过特定子图.用Enter, Leave, and NextIteration来表示循环

### 输入operation

feed dict,从存储到客户端，然后到worker。

input node,从存储到worker。

### 队列

入无位或余不足出，皆阻。

prefetch data. accumulating gradients.

### Ref:          
  - <https://www.tensorflow.org/versions/r1.0/extend/architecture>               
  - <https://github.com/tensorflow/tensorflow/blob/r1.1/tensorflow/core/protobuf/master_service.proto>        
  - <https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/45166.pdf>
  - <https://github.com/samjabrahams/tensorflow-white-paper-notes> 
  - <http://cs231n.github.io/optimization-2/>  
	
