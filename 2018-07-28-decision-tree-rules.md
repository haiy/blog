---
title: 基于随机森林的规则生成算法 
layout: post
---

## {{page.title}}

<p class="meta">28 July 2018</p>


在金融风控领域里面由于需要对所有上线的模型和规则都有明确的可解释性。但是因为人工去直接基于特征构建规则训练的成本较高，所以需要有工具能提供规则的生成。而树类模型训练后的可解释性比较好，因此在此情况下比较适合用来作为规则的生成算法。具体的做法就是先训练一颗颗的树，然后将这棵树的上所有的节点都抽出来作为规则条件。最后再对这些抽取出来的规则进行重要性评估。


在规则生成之后，如何运用这些规则重新生成特征和对其评价其实也是另外真正需要花费精力的。

Table of Contents
=================

* [单颗树算法流程](#单颗树算法流程)
* [规则导出算法实现](#规则导出算法实现)
* [规则评估算法](#规则评估算法)
* [核心点回顾](#核心点回顾)
* [Refs](#refs)



#### 单颗树算法流程

- 1 用sklearn的DecisionTree对输入数据`train_data`进行训练得到模型`dt_model`
- 2 根据`dt_model`中保存的模型树信息`dt_model._tree` 信息，进行节点遍历生成规则
- 3 将`train_data`转换成用规则生成新的数据集，每列即为一个规则，然后用LogisticRegresssion模型L2来训练该数据
- 4 导出LR的权重作为规则的评估权重

#### 规则导出算法实现


```python
from pprint import pprint
from collections import deque
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
import logging
import time, uuid, os

import numpy as np

LOGGER = logging.getLogger("export decision tree rules")

timestamp = lambda: int(round(time.time() * 1000))
get_id = lambda: str(uuid.uuid4())
os.environ["JOBLIB_TEMP_FOLDER"] = "/tmp"


def load_bin_data():
    from sklearn.datasets import make_classification
    X, y = make_classification(n_samples=1000, n_features=4,
                               n_informative=2, n_redundant=0,
                               random_state=0, shuffle=False)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    return X_train, X_test, y_train, y_test

def train_dt(X_train, y_train):
    estimator = DecisionTreeClassifier(max_leaf_nodes=9, random_state=0)
    estimator.fit(X_train, y_train)
    tree.export_graphviz(estimator, out_file='tree.dot')
    return estimator

def export_rules(dt_estimator):
    """
    extract rules from trained sklearn DecisionTreeClassifier model by traverse the
    tree.
    :param dt_estimator: fitted model
    :return: path rules to the leaf node
    """
    n_nodes = dt_estimator.tree_.node_count
    children_left = dt_estimator.tree_.children_left
    children_right = dt_estimator.tree_.children_right
    feature = dt_estimator.tree_.feature
    threshold = dt_estimator.tree_.threshold

    node_depth = np.zeros(shape=n_nodes, dtype=np.int64)
    is_leaves = np.zeros(shape=n_nodes, dtype=bool)

    # collect leaf nodes
    stack = [(0, -1)]  # seed is the root node id and its parent depth
    while len(stack) > 0:
        node_id, parent_depth = stack.pop()
        node_depth[node_id] = parent_depth + 1
        # If we have a test node
        if (children_left[node_id] != children_right[node_id]):
            stack.append((children_left[node_id], parent_depth + 1))
            stack.append((children_right[node_id], parent_depth + 1))
        else:
            is_leaves[node_id] = True
    LOGGER.info("The binary tree structure has %s nodes" % n_nodes)

    # traverse the tree by layer in increment order
    dep_map = {}
    path_info = {}
    path_info[0] = []
    for i in range(n_nodes):
        if i not in dep_map:
            dep_map[i] = []
        if is_leaves[i]:
            pass
        else:
            dep_map[i] += [children_left[i], children_right[i]]
            path_info[children_left[i]] = path_info[i] + [("%s <= %s") % ("f_idx_" + str(feature[i]), threshold[i])]
            path_info[children_right[i]] = path_info[i] + [("%s > %s") % ("f_idx_" + str(feature[i]), threshold[i])]
            LOGGER.info("%snode=%s test node: go to node %s if X[:, %s] <= %s else to "
                        "node %s."
                        % (node_depth[i] * "\t",
                           i,
                           children_left[i],
                           feature[i],
                           threshold[i],
                           children_right[i],
                           ))
    return dict([(k, " && ".join(v)) for k, v in path_info.items()]), dep_map


X_train, X_test, y_train, y_test = load_bin_data()
dt_model = train_dt(X_train, y_train)
rules, dependency_info = export_rules(dt_model)
pprint(rules, width=300)

from graphviz import Source
Source.from_file("tree.dot").view()
```

下图是一个导出的树:

![tree](/images/dt_tree.jpg)

导出的规则：

```python
{0: '',
 1: 'f_idx_1 <= -0.180589914322',
 2: 'f_idx_1 > -0.180589914322',
 3: 'f_idx_1 > -0.180589914322 && f_idx_0 <= 2.17871904373',
 4: 'f_idx_1 > -0.180589914322 && f_idx_0 > 2.17871904373',
 5: 'f_idx_1 > -0.180589914322 && f_idx_0 > 2.17871904373 && f_idx_1 <= 0.835420966148',
 6: 'f_idx_1 > -0.180589914322 && f_idx_0 > 2.17871904373 && f_idx_1 > 0.835420966148',
 7: 'f_idx_1 <= -0.180589914322 && f_idx_1 <= -0.462307840586',
 8: 'f_idx_1 <= -0.180589914322 && f_idx_1 > -0.462307840586',
 9: 'f_idx_1 <= -0.180589914322 && f_idx_1 > -0.462307840586 && f_idx_0 <= 1.17936778069',
 10: 'f_idx_1 <= -0.180589914322 && f_idx_1 > -0.462307840586 && f_idx_0 > 1.17936778069',
 11: 'f_idx_1 > -0.180589914322 && f_idx_0 > 2.17871904373 && f_idx_1 > 0.835420966148 && f_idx_0 <= 2.65450286865',
 12: 'f_idx_1 > -0.180589914322 && f_idx_0 > 2.17871904373 && f_idx_1 > 0.835420966148 && f_idx_0 > 2.65450286865',
 13: 'f_idx_1 > -0.180589914322 && f_idx_0 <= 2.17871904373 && f_idx_3 <= 2.88247418404',
 14: 'f_idx_1 > -0.180589914322 && f_idx_0 <= 2.17871904373 && f_idx_3 > 2.88247418404',
 15: 'f_idx_1 > -0.180589914322 && f_idx_0 > 2.17871904373 && f_idx_1 > 0.835420966148 && f_idx_0 > 2.65450286865 && f_idx_0 <= 2.97060251236',
 16: 'f_idx_1 > -0.180589914322 && f_idx_0 > 2.17871904373 && f_idx_1 > 0.835420966148 && f_idx_0 > 2.65450286865 && f_idx_0 > 2.97060251236'}

```

#### 规则评估算法

在前面完成了规则导出，其实只是完成了一半，如何对这些导出的规则进行高效的评估呢？

具体的评估算法其实有两个，
- 1 计算每个规则的覆盖率以及lift
- 2 生成基于这些规则的数据集然后训练LR，根据权重评估

那么，其实DecisonTree模型本身在进行预测的时候，输出的是叶子节点，而叶子节点的label是根据其训练的时候
样本的分布来确定的。而每个规则的路径其实都是叶子节点的一部分。因此在进行规则评估的时候，只要得到了叶子节点规则的
评估结果，在根据规则路径的依赖关系就可以算出所有规则的评估结果。

所以规则评估算法的核心其实是算出规则之间的依赖关系，也就是将树倒过来算。

具体算法流程:

- 1 计算所有规则的依赖关系字典`dep_info`,key为节点Id，value为其下游两个节点
- 2 对节点依赖关系进行分层拓扑排序，得到按层存储的依赖关系表
- 3 计算测试样本集`test_data.csv`中每条样本对应的叶子节点
- 4 对所有样本按照叶子节点进行合并统计
- 5 根据节点分层依赖关系以及叶子节点样本分布统计值，计算所有节点的统计分布



```python
# 基于叶子节点规则评估
def topological(graph):
    GRAY, BLACK = 0, 1
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = GRAY
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == GRAY: raise ValueError("cycle")
            if sk == BLACK: continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = BLACK

    while enter: dfs(enter.pop())
    return order

def predict_leaf_rules(dt_estimator, eval_data):
    leaves_ids = dt_estimator.apply(eval_data)
    return leaves_ids


def extract_predict_sample_count(dt_estimator, leave_ids, y_test, dep_map):
    sort_dep = topological(dep_map)
    eval_table = []
    new_shape_dist = np.reshape(dt_estimator.tree_.value, (dt_estimator.tree_.node_count, dt_estimator.n_classes_))
    node_class_dict = np.argmax(new_shape_dist, axis=1)
    for leaf_id, real_class_label in zip(leave_ids, y_test):
        eval_table.append([leaf_id, node_class_dict[leaf_id], real_class_label])

    def reduce_sum_fn(r1, r2):
        return [r1[0] + r2[0], r1[1] + r2[1], list(np.sum([r1[2], r2[2]], axis=0)),
                list(np.sum([r1[3], r2[3]], axis=0))]

    n_classes = 2

    def reduceByKey(func, iterable):
        get_first = lambda p: p[0]
        get_second = lambda p: p[1]
        return map(
            lambda l: (l[0], reduce(func, map(get_second, l[1]))),
            groupby(sorted(iterable, key=get_first), get_first)
        )

    def map_fn(r):
        predict_onehot = [0] * n_classes
        predict_onehot[r[1]] = 1
        real_onehot = [0] * n_classes
        real_onehot[r[2]] = 1
        return (r[0], [1, int(r[1] == r[2]), predict_onehot, real_onehot])

    leaf_sample_count = dict(reduceByKey(reduce_sum_fn, map(map_fn, eval_table)))

    all_node_count = {}
    for i in reversed(sort_dep):
        if len(dep_map[i]) == 0:
            if i in leaf_sample_count:
                all_node_count[i] = leaf_sample_count[i]
            else:
                all_node_count[i] = [0, 0, [0, 0], [0, 0]]
        else:
            left_dep, right_dep = dep_map[i]
            totoal_count = reduce_sum_fn(all_node_count[left_dep], all_node_count[right_dep])
            all_node_count[i] = totoal_count

    return [all_node_count[i][-1] for i in range(len(all_node_count))]


test_sample_leaf_ids = predict_leaf_rules(dt_model, X_test)
res = extract_predict_sample_count(dt_model, test_sample_leaf_ids, y_test, dependency_info)
# 每个节点的样本分布情况
pprint(res)
```

#### 核心点回顾

至此，从随机森林导出规则算法评估的核心功能已经实现了2/3.还剩下的关键点是将所有的单颗树的规则拼成训练样本，用LR来训练。
这个直接看实现的代码就好了。
这个事情其实比较有意思的地方在于规则的导出，以及规则的合并评估，需要稍微思考下。

#### Refs

- [sklearn rules from decision tree](https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree)
- [RandomForestClassifier](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
- [eval rule string](http://hplgit.github.io/primer.html/doc/pub/input/._input-readable003.html)
- [string to fun](https://stackoverflow.com/questions/22443939/python-built-in-function-compile-what-is-it-used-for)
- [python-builtin-functions-compile](http://joequery.me/code/python-builtin-functions/#compile)
- [hyperparameter tuning](http://sujitpal.blogspot.com/2016/04/hyperparameter-optimization-on-spark-ml.html)