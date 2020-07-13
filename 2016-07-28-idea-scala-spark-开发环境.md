---
title: Idea Scala Spark 开发环境
date: 2016-07-28 00:00:00 Z
layout: post
---

{{page.title}}
=======
<p class="meta">July 28 2016</p>

**1. 安装java1.84,scala以及其他基本工具**

[java 8, spark安装](http://haiy.github.io/2015/08/16/%E6%B7%B7%E5%90%88%E9%A2%84%E6%B5%8B%E6%A8%A1%E5%9E%8B%E5%8F%8Aspark,JAVA%E9%85%8D%E7%BD%AE.html)

```bash
sudo apt-get install git maven scala
```

- [java8 下载地址](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
- [scala11 下载地址](http://scala-lang.org/download/)
- [spark2.0 下载地址](http://spark.apache.org/downloads.html)
- [hadoop2.7 下载地址](http://hadoop.apache.org/releases.html)
- [Idea162 下载地址](https://www.jetbrains.com/idea/download/download-thanks.html?code=IIC)


**2. 代码框架**
 
(artifactId就是最后的jar包的名字）

手动生成全新的代码框架或者直接用我的[带有spark样例测试的代码框架](https://raw.githubusercontent.com/haiy/haiy.github.io/master/old_data/HackData.tar.gz)

[How_do_I_setup_Maven](https://maven.apache.org/guides/getting-started/index.html#How_do_I_setup_Maven)

切换到工程目录，

```
mvn -B archetype:generate \
  -DarchetypeGroupId=org.apache.maven.archetypes \
  -DgroupId=com.mycompany.app \
  -DartifactId=my-app

#pom.xml中spark core依赖
<!-- https://mvnrepository.com/artifact/org.apache.spark/spark-core_2.11 -->
<dependency>
    <groupId>org.apache.spark</groupId>
    <artifactId>spark-core_2.11</artifactId>
    <version>2.0.0</version>
</dependency>
```

**3. 打开Idea，导入maven项目，安装插件，设置sdk**

安装插件,ctrl+shift+a, plugins,install jetbrain plugins, 搜索scala,安装


**4. 测试代码**

[sparkl-core pom dependency](https://mvnrepository.com/artifact/org.apache.spark/spark-core_2.11/2.0.0)  
[running on yarn](http://spark.apache.org/docs/latest/running-on-yarn.html)  

```bash
#打包
mvn package -DskipTests=true -T 2C

$ ./bin/spark-submit --class path.to.your.Class --master yarn --deploy-mode cluster [options] <app jar> [app options]

$ ./bin/spark-submit --class org.apache.spark.examples.SparkPi \
    --master yarn \
    --deploy-mode cluster \
    --driver-memory 4g \
    --executor-memory 2g \
    --executor-cores 1 \
    --queue thequeue \
    lib/spark-examples*.jar \
    10

$ ./bin/spark-submit --class my.main.Class \
    --master yarn \
    --deploy-mode cluster \
    --jars my-other-jar.jar,my-other-other-jar.jar \
    my-main-jar.jar \
    app_arg1 app_arg2
```

**5. java scala混合项目**

其实主要是pom的配置

### 参考：
  
- [spark_test project](https://github.com/haiy/test_project/tree/master/spark_test)    
- [running on yarn](http://spark.apache.org/docs/latest/running-on-yarn.html)   
- [Hadoop doc](http://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)  
- [scala download](http://www.scala-lang.org/download/)   
- [spark maven repo](http://search.maven.org/#search%7Cga%7C1%7Cg%3A%22org.apache.spark%22)  
- [scala tech blog](http://hongjiang.info/scala/)   
- [spark-dataframe-transform-multiple-rows-to-column](http://stackoverflow.com/questions/33732346/spark-dataframe-transform-multiple-rows-to-column)  
- [hadoop download](http://hadoop.apache.org/releases.html)  
