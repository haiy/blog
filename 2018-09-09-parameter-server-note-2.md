---
title: parameter server核心源码解析  
layout: post
---

## {{page.title}}

<p class="meta">09 Sep 2018</p>

* [启动过程](#启动过程)
* [键值传输分配](#键值传输分配)
     
     
###  启动过程

ps的启动过程关键在于理解postoffice，van，customer, app这四个抽象组件之间的关系。

ps中一个节点可选的角色有三种,scheduler,server,worker. scheduler负责所有节点的接入和心跳检测。

启动的时候,所有的节点都会先启动开始提到组件。其中postoffice负责环境信息和集群信息的维护，van负责
当前节点数据的发送和接受，而customer则是业务消息接受和发送管理的抽象，app则是基于customer对server和
worker具体执行函数的自定义入口。

van是基于zmq实现的pub-sub消息传递模式，主要作用是消息路由，对于集群控制类消息和数据类消息传递
给不同的对象，也就是scheduler或者customer。

整个启动过程，首先会执行app所在main函数作为入口，app启动的时候会直接创建一个customer实例，
并将具体的req和resp处理函数绑定到customer上。然后会进行postoffice初始化。

postoffice在类初始化的时候会直接初始化一个van实例。在启动的时候，主要步骤如下:

- 读取系统变量中集群配置情况
- 根据配置生成节点顺序和ID的对应关系

van则在启动中主要做的事情如下:

- 找到合适的端口启动，绑定
- 连接scheduler
- 发送添加自己节点到集群的请求

当所有节点都添加到scheduler端的时候，sceduler端根据节点的ip+port排序rank分别给每个节点
分配ID，每个节点收到ID分配消息后，更新自己的信息。

当所有节点信息更新完成，集群启动开始根据barrier参数进行固化。
    

### 键值传输分配

#### **节点的key range是如何划分的？计算过程中一个key应该会分到哪个主机上？**

先说key range划分问题。当配置了server和worker的数量后，server端的key range已经直接按照每个区间范围都是Max/numb_server的大小。具体可以看[这部分源码](https://gitee.com/arthurhu/ps-lite/blob/master/src/postoffice.cc#L168),线上是server rank转成node id,然后直接将key range分给该node
来划分来。

那么一个key到底会分到哪个机器上呢？

一个具体的物理机信息要经过两步才能和真正的key range对应起来。

- 1 基于所有物理机ip+port排序分配`node id的。涉及到RankToId[ServerRankToID](https://gitee.com/arthurhu/ps-lite/blob/master/include/ps/internal/postoffice.h#L99)和[WorkerRankToId](https://gitee.com/arthurhu/ps-lite/blob/master/include/ps/internal/postoffice.h#L106),具体的连接分配逻辑要看[van是如何对接入节点信息处理的](https://gitee.com/arthurhu/ps-lite/blob/master/src/van.cc#L42).

- 2 ps中默认实现了一个key分割器[DefaultSlicer](https://gitee.com/arthurhu/ps-lite/blob/master/include/ps/kv_app.h#L411),

    具体实现逻辑步骤：首先计算基于ServerRanges对key的分割点，然后在value数据分割成对应的份

- 3 根据ServerRankToID顺序将sliced的kv pair发送到对应的server，具体可以参照[kv_app.h#L493](https://gitee.com/arthurhu/ps-lite/blob/master/include/ps/kv_app.h#L493)


 其中另外一个比较需要注意的点是[test_kv_app.cc](https://gitee.com/arthurhu/ps-lite/blob/master/tests/test_kv_app.cc#L25)中key的生成方式其实也是比较有意思的。

其实以上过程就包含了一个worker对数据进行PUSH的过程:
- slice kv
- send to server
    