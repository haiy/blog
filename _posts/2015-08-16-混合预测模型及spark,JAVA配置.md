---
title: 混合预测模型以及Spark，JDK1.8配置
date: 2015-08-16 00:00:00 Z
layout: post
commentIssueId: 1
---

{{page.title}}
---
<p class='meta'>17 Aug 2015</p>


#### 1.混合迭代模型

混合迭代模型的主要思路是混合多模型，多规则的结果，计算一个用户的复合得分，而后按得分排序，取topN 作为最终投放人群。通过每隔3天的投放效果对混合模型的各项进行权重调整，以其达到最好的效果。

```
用户得分函数：
userscore = wLR*SLR + wGBDT*SGBDT + wRF*SRF + wR1*SR1 + … + wRn*SRn
     注：w表示某个模型或者规则的权重
S表示某个模型或者规则的得分
所有模型初始权重为1
所有得分S取值范围（0，1)
LR表示逻辑回归模型
GBDT表示梯度渐进决策树
RF表示随机森林
R表示规则

采用特征:
is_member, 
view_pages,
view_items,
view_days,
view_pages/d.view_days as avg_pages_per_day,
view_items/d.view_days as avg_items_per_day,
view_pages/d.view_items as avg_pages_per_item,
datediff(to_date('${bizdate}','yyyymmdd'),
	to_date(d.latest_view_time,'yyyymmdd'), 'dd')  as last_view_interval,
order_count,
order_count/d.view_days as order_per_day,
datediff(to_date('${bizdate}','yyyymmdd'),
	to_date(e.latest_order_time,'yyyymmdd'), 'dd')  as last_buy_interval,
f.collect_count,
f.collect_days
注：斜体部分为比较有效的特征
迭代过程：
	根据模型投放人群每隔3天，计算一次各个模型及规则人群的命中效果，
	根据命中人群比例确定模型权重，调整目标可以根据需求侧重，从而产生如高点击模型，高转化模型。
```

#### 2.Spark以及JDK1.8快速配置
	
Spark 部署方式：
1.部署脚本

```bash
#!/bin/bash
cd /software/servers/
wget http://mirrors.aliyun.com/apache/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz
tar -xvzf  spark-1.4.1-bin-hadoop2.6.tgz
echo “SPARK_HOME=/software/servers/spark-1.4.1-bin-hadoop2.6” >> ~/.bashrc
echo “export PATH=$SPARK_HOME/bin:$PATH” >> ~/.bashrc
source ~/.bashrc
```

2.测试命令
cd $SPARK_HOME
./bin/spark-submit --class org.apache.spark.examples.SparkPi \
--master yarn-cluster \
--num-executors 3 \
--driver-memory 4g \
--executor-memory 2g \
--executor-cores 1 \
lib/spark-examples*.jar \
10


Java8 部署步骤:

```
1.打开网页：http://www.oracle.com/technetwork/java/javase/
	downloads/jdk8-downloads-2133151.html
2. 选中Accept License Agreement 
3.下载 Linux x64 165.24 MB    jdk-8u45-linux-x64.tar.gz版本
4.cd /software/servers/
5.tar -xvzf jdk-8u45-linux-x64.tar.gz
6.打开/etc/profile,添加以下内容,注意将下面的jdk1.8.0_xx替换成具体的jdk版本号！
JAVA_HOME=/software/servers/jdk1.8.0_xx
JRE_HOME=/software/servers/jdk1.8.0_xx/jre
PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH
CLASSPATH=$CLASSPATH:.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
7.更新系统java版本
update-alternatives --install /usr/bin/java java \ 
	/software/servers/jdk1.8.0_xx/bin/java 300
update-alternatives --install /usr/bin/javac javac \ 
	/software/servers/jdk1.8.0_xx/bin/javac 300
update-alternatives --config java
update-alternatives --config javac
```
测试JDK是否安装配置成功：
 java -version
 
#### 小结
 
 最近两周都没有好好看书，一方面是因为工作的原因，一方面是自己有些懒散了。因为发现实际工作中用到的东西，
 书上给不了，有点无力感。有时候睡觉醒了也在想工作的事情。要努力啊！！
 



