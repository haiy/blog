---
title: 构建一个企业级深度学习平台
layout: post
---

## {{page.title}}

<p class="meta">3 Jun 2018</p>


通常一个公司内的算法工程师达到一定规模后，就需要一个统一的环境来提供一系列的模型训练及上线。
整体来说一个完整的深度学习平台包含两大块，一个就是训练，另一个是上线。那么有么有一套环境能够
较好的支持模型训练和上线呢？在目前探索下，jupyterhub+k8s是一个比较理想的方案。

统一环境其实核心问题主要涉及两个方面，一个是单用户的环境的自定义和隔离，另一是用户资源的隔离。
jupyterhub已经较好的支撑了多用户统一调用的功能，再结合jupyter的notebook这个本来就很好的
支撑深度学习算法开发环境的工具，所以支持单用户开发环境是没有问题的。那么对于计算资源来说，因为
企业内往往都是集群使用，那么对集群资源的抽象最好的就是分布式系统了。可是传统的资源抽象基本都是
基于java进程的container的，比如说yarn。所以容器化平台kubernetes最合适不过了。

那么接下来就简单熟悉下这样的一个平台和架构吧。本文会从以下三个方面来说:

- [基本概念](#基本概念)
  - [jupyter,notebook,jupyterhub](#jupyter,notebook,jupyterhub)
  - [kubernetes](#kubernetes)
- [深度学习平台](#深度学习平台)
- [如何构建平台](#如何构建平台)
  - [基础镜像](#基础镜像)  
  - [训练环境](#训练环境)   
  - [模型服务上线](#模型服务上线)  
- [小结](#小结)

                               
## 基本概念


为了更好的构建整个平台，首先需要的就是弄清楚这些框架工具是什么，有哪些核心组件，需要时怎么定制，以及有哪些局限等。

### jupyter,notebook,jupyterhub

[jupyter](http://jupyter.org/documentation)对于构建深度学习和python开发来说算是比较方便的交互开发环境。
这三者到底是什么关系，各自的定位是什么呢？在一开始接触的时候，真的是一头雾水，因为它不像spark，sklearn这些框架，一个名字对应的就是整个系统本身。一图胜千言，先来一张架构图，

<img src="https://zero-to-jupyterhub.readthedocs.io/en/latest/_images/architecture.png">

上图可以看出整个jupyter体系架构主要分了四层：kernel,api,application,server。其中需要弄清的关键点是：

- jupyter是个上层通用的应用入口
- notebook是一个基于torado构建的web IDE应用
- juypterhub一个多用户管理的应用
- jupyterlab是对notebook的前段界面的重构和优化

所以简单来说一个多用户开发环境是以上几个的结合。

### kubernetes
  
[kubernetes](https://kubernetes.io/docs/home/)是google开源的一个容器化平台。主要的概念来说有这么几个：

- node 对物理机或者虚拟机资源的抽象
- pod 最小的资源调度单位和应用抽象,其实体一般是运行的docker实例
- deployment 包含期望状态和当前状态等信息的pod运行配置抽象,可以更新修改来调整应用状态
- service k8s默认启动的应用是集群内可见，service是将deployment暴露给外部服务的配置抽象

其架构整体如下：

![](https://d33wubrfki0l68.cloudfront.net/518e18713c865fe67a5f23fc64260806d72b38f5/61d75/images/docs/post-ccm-arch.png)


简单来说k8s集群的节点有2个角色，一个是master，其他是资源节点。master节点上主要是apiserver和scheduler还有些controller。

- apiserver是集群的所有交互接口
- scheudler负责资源的调度，pod到哪个node，path到哪个服务
- etcd是所有资源的存储

资源节点上都是apiserver和kubelet交互，服务访问则是kube-proxy进行处理的。具体来说，要部署一个应用到k8s上一般要经过以下几个步骤:

- 1 镜像构建,编写Dockerfile.[Dockerfile best practice](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- 2 镜像测试. [build,run](https://docs.docker.com/get-started/#containers-and-virtual-machines).最好[用镜像](https://docs.docker.com/registry/recipes/mirror/#use-case-the-china-registry-        mirror)，比较好的镜像有: [163](http://hub-mirror.c.163.com), [ustc](https://docker.mirrors.ustc.edu.cn).阿里云注册后也可以有私有的mirror。
- 3 编写k8s配置[yaml文件](https://kubernetes.io/docs/concepts/overview/object-management-kubectl/declarative-config/)。
- 4 创建应用 [应用最佳实践](https://kubernetes.io/docs/concepts/configuration/overview/)
- 5 服务暴露. [实操相关](https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/).注意默认的`nodePort`的暴露和实用的`LoadBalancer`。

    ```
    kubectl expose app_pod_name –type=“LoadBalancer” –name=“example-service”
    ```

- 6 服务调试. 其实服务出问题调试和docker调试的方法类似，最好莫过于进入容器内调试。比较好的路子如下:

  - a 确认pod详情. `kubectl describe pod-name --namespace=pod-ns`
  - b 查看日志. `kubectl logs -f --namespace=pod-ns pod-name `
  - b 进入pod内. `kubectl exec -it pod-name --namepace=pod-ns /bin/bash`
  

熟悉的最好方法是自己跟着教程走一遍.这个[nodejs服务的教程](https://github.com/haiy/jupyterhub-on-k8s/tree/master/hello-k8s/hello-k8s-node)还算是比较全，值得一看。

## 深度学习平台  

前面说完了jupyter和k8s，接下来需要进入正题，一个平台到底要有些什么？

一个深度学习平台主要目标是给建模人员提供一个比较完善高效的开发和上线环境。结合当前主流的平台，一个较好的平台的话主要是自由度和标准化的协调。标准化越高，整个建模流程和上线就自动化程度越高，但自由度的丧失其实一定程度上是限制了建模人员对算法的掌控和自定义。所以一个比较好的平台应该根据当前产品的主要用户群体进行相应的调整侧重点。

总体来说一个应该包含以下几个方面：

- 模型训练环境
- 高效训练支持(GPU，Spark. etc)
- 模型上线流程
- 模型服务


## 如何构建平台

 - [基础镜像](#基础镜像)  
 - [训练环境](#训练环境)   
 - [模型服务上线](#模型服务上线)  


所有镜像已经在[github](https://github.com/haiy/jupyterhub-on-k8s/tree/master/docker)准备好了。可以直接使用。

### 基础镜像

- [ubuntu](https://github.com/haiy/jupyterhub-on-k8s/tree/master/docker/ubuntu)
- [conda](https://github.com/haiy/jupyterhub-on-k8s/tree/master/docker/conda)


### 训练环境

训练环境的构建目标是提供标准的基础环境以及可以自由配置的辅助环境。

- [jupyterhub](https://github.com/haiy/jupyterhub-on-k8s/tree/master/docker/jupyterhub)
- [ai-cpu-gpu](https://github.com/haiy/jupyterhub-on-k8s/tree/master/docker/ai-notebook)



### 模型服务上线

模型上线的话主要解决的问题是不同训练框架产出的模型怎么在线上服务的问题。那这个之所以成为问题的原因是：

- 建模框架多样性,模型导出格式不一致,sklearn,tensorflow,spark
- 线上服务的实时性和稳定性要求

第二点是所有线上服务都有的。但是第一点却是模型服务特有的。模型服务自身的特点具体来说有这几个方面：

- 无状态
- 往往有预处理，模型预测以及结果调整这三步
- 服务链路中往往是模型文件本身变更频繁
- 模型大小不一，Kb ~ Gb

所以模型服务需要解决的问题的可行方案也就瞄准上面的问题来说：

- 构建[服务框架](https://github.com/haiy/ai-serving),抽象服务流程.[以irisi为例的模型服务](https://github.com/haiy/ai-serving/tree/master/aiserving/iris-model).
- [serving镜像](https://github.com/haiy/ai-serving/tree/master/docker)分离模型服务环境和服务相关资源
- 充分利用k8s的特性,auto-scale

## 小结

总算写完了。其实很多点还没有写到。后面再补充吧。

