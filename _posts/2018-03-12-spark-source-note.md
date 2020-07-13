---
title: spark note
layout: post
---

{{page.title}}
=============

<p class="meta">12 Mar 2018</p>
     
* [spark alpha-0.1版本](#spark-alpha-01版本)
* [RDD的生成：](#rdd的生成)
    * [a paralleArray](#a-parallearray)
    * [b hdfsTextFile也是RDD的一个具体实现](#b-hdfstextfile也是rdd的一个具体实现)
* [对于中间计算](#对于中间计算)
* [spark alpha-0.2版本](#spark-alpha-02版本)

spark作为大数据计算的基础框架，熟悉其使用的重要性不需多言，接下来以spark基础最开始的版本来说明下其核心模块。

# spark alpha-0.1版本

# RDD的生成
RDD的构建过程主要包含三个方面：
1 split信息的构建和读取
2 iterator单split的数据读取执行函数

## a paralleArray  
根据其具体实现可以看出其是一个RDD的具体实现

```java
class ParallelArray[T: ClassManifest](
  sc: SparkContext, @transient data: Seq[T], numSlices: Int)
extends RDD[T](sc) {
  // TODO: Right now, each split sends along its full data, even if later down
  // the RDD chain it gets cached. It might be worthwhile to write the data to
  // a file in the DFS and read it in the split instead.

  val id = ParallelArray.newId()

  @transient val splits_ = {
    val slices = ParallelArray.slice(data, numSlices).toArray
    slices.indices.map(i => new ParallelArraySplit(id, i, slices(i))).toArray
  }

  override def splits = splits_.asInstanceOf[Array[Split]]
  override def iterator(s: Split) = s.asInstanceOf[ParallelArraySplit[T]].iterator
  override def preferredLocations(s: Split): Seq[String] = Nil
}

```

## b hdfsTextFile也是RDD的一个具体实现

src/scala/spark/RDD.scala
核心抽象RDD

# 对于中间计算

以RDD的map操作为例，可以看出其实质是直接生成了一个新的MappedRDD类型的对象，并将处理函数
去闭包后传入作为参数。

def map[U: ClassManifest](f: T => U) = new MappedRDD(this, sc.clean(f))

深入MappedRDD，可以看到，其实质上是将该函数应用到了分区的迭代器函数上
 override def iterator(split: Split) = prev.iterator(split).map(f)

对RDD的union计算实际上是将数据的split信息合并，并不对数据的处理函数做任何处理。

对于实际action计算：
以collect操作为例，其是直接每个split对应生成了一个CollectTask，然后直接执行这些任务。
def collect(): Array[T] = {
  val tasks = splits.map(s => new CollectTask(this, s))
  val results = sc.runTaskObjects(tasks)
  Array.concat(results: _*)
}

最后将结果返回driver端。

从上面可以明显看出spark的RDD的基本抽象概念。

# spark alpha-0.2版本

core/src/main/scala/spark/RDD.scala
RDD抽象更加完善

1 每个RDD新增dependencies信息
2 明确唯一标示，cache不再返回CacheRDD，只是将shouldCache置为true
3 添加了针对key的合并计算,添加真正的reduce步骤，也就是PairRDD


PairRDDExtras抽象最核心的方法是：


```java
def combineByKey[C](createCombiner: V => C,
                    mergeValue: (C, V) => C,
                    mergeCombiners: (C, C) => C,
                    numSplits: Int)
: RDD[(K, C)] =
{
  val aggregator = new Aggregator[K, V, C](createCombiner, mergeValue, mergeCombiners)
  val partitioner = new HashPartitioner(numSplits)
  new ShuffledRDD(self, aggregator, partitioner)
}
```

其主要定义了真正的reduce操作步骤,并最终输出一个ShuffledRDD。

### Ref:
   - [spark alpha 0.1](https://github.com/apache/spark/tree/alpha-0.1)
   - [spark alpha 0.2](https://github.com/apache/spark/tree/alpha-0.2)
