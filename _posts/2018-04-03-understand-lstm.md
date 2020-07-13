---
title: 理解并推导LSTM
layout: post
---

{{page.title}}
=============

<p class="meta">03 April 2018</p>

Table of Content
=================
   * [前向计算](#前向计算)
       * [门函数](#门函数)
       * [状态更新及计算输出](#状态更新及计算输出)
       * [损失函数](#损失函数)
   * [反向推导](#反向推导)
   * [小结](#小结)                             
   * [手写实现](https://github.com/haiy/rush_in_dl/blob/master/lstm.py)                         
                            
                      
===========


LSTM, Long Short Memory Networks.其实质是RNN的变种.其关键点是对隐含层之间状态迁移计算的精细化.

要理解LSTM首先必须得非常清楚的理解了RNN才能更好的继续，因为LSTM的诞生正是为了解决
RNN的局限性,梯度消失(或者爆炸).那么LSTM对这个问题是怎么解决的？

首先,RNN的局限的根源是对任何历史信息和当前数据信息都不加区分的直接传递到后面的序列节点中。所以LSTM
的解决方式是对历史信息和输入信息的的传递加上一个权重开关，来控制信息的传递过程。

其次,RNN的计算过程中其实是没有用到上次计算的输出的。而LSTM则综合考虑历史的输出和当前的输入作为状态
迁移的一部分信息进行处理。

最后,LSTM创造性的将模型结构概念和人的直觉认知更进一步的深化结合。人会遗忘也会长期
的实践过程反复强化一些有用的信息。刚发生的事情肯定印象比较深。那么这两个方面作用的过程
最终形成了人的经验。类比于LSTM结构，加上遗忘门(forget gate)给历史信息和当前信息一个
衰减的过程。在根据上一步状态和输入计算当前状态时，再综合考虑进上一步的输出。最终当前状态的信息来源
包含三个方面:       
   - a 经过遗忘后的遗留,forget gate       
   - b 当前输入信息的"精馏", input gate   
   - c 粗糙的状态信息  

# 前向计算

## 门函数

$$
\begin{align}
f_t &= sigmoid(W_{xf}x_t + W_{hf}h_{t-1} + b_f) \\
i_t &= sigmoid(W_{xi}x_t + W_{hi}h_{t-1} + b_i) \\
o_t &= sigmoid(W_{xo}x_t + W_{ho}h_{t-1} + b_o) \\
c\_c_{t} &= tanh(W_{xc}x_{t} + W_{hc}h_{t-1} + b_{c\_in})
\end{align}
$$

* 将参数成一个变量

这个合并计算的地方其实并不是啥新东西，在RNN计算的时候也可以，不过因为
RNN就一个类似公式，而这实际上有4个。这样写好处就是方便。

$$
\begin{align}
W &= sigmoid(W_x * x + W_h * h) \\
W_x.shape &= hiddenSize * Xsz \\
x.shape &= Xsz*1 \\
W_h.shape &= hiddenSize * hiddenSize \\ 
h shape &= hiddenSize * 1 \\\\
\text{合并计算: }\\
W.shape &= hiddenSize*(Xsz + hiddenSize), colmerge \\
X.shape &= Xsz + hiddenSize, rowmerge \\\\
\text{合并后新公式: }\\
f_t &= sigmoid(W_f[x_t,h_{t-1}]) \\
i_t &= sigmoid(W_i[x_t,h_{t-1}]) \\
o_t &= sigmoid(W_o[x_t,h_{t-1}]) \\
Cc_t &= tanh(W_cc[x_t,h_{t-1}]) \\
\end{align}
$$

## 状态更新及计算输出

$$
\begin{align}
c_{t} =& f_{t} \cdot c_{t-1} + i_{t} \cdot c\_c_{t} \\
h_{t} =& o_{t} \cdot tanh(c_{t}) \\
y_t =& softmax(W_hy*h_t + b_y) \\
\end{align}
$$

## 损失函数

$$
L = -\sum_{t=0}^{t} p_tlog{(y_t)} \\\\
$$

## 反向求导

$$
\begin{align}
\frac{\partial L_t}{\partial h_t} &= (h_t - y_t) = \delta_{ht}\\
\frac{\partial L_t}{\partial o_t} &= \frac{\partial L_t}{\partial h_t}\frac{\partial h_t}{\partial o_t}=\delta_{ht} \cdot tanh(C_t) = \delta_{ot}\\
\frac{\partial L_t}{\partial C_t} &= \frac{\partial L_t}{\partial h_t}\frac{\partial h_t}{\partial c_t}=\delta_{ht} \cdot o_t \cdot (1-tanh^2{C_t}) = \delta_{C_t}\\\\
\text{对三个门以及一个输入转换求导: } \\
\frac{\partial L_t}{\partial f_t} &= \frac{\partial dL}{\partial c_t}\frac{\partial c_t}{\partial f_t} = \delta_{C_t} \cdot C_{t-1}\\
\frac{\partial L_t}{\partial C_{t-1}} &= \frac{\partial L}{\partial c_t}\frac{\partial c_t}{\partial C_{t-1}} = \delta_{C_t} \cdot f_t\\
\frac{\partial L_t}{\partial i_t} &= \frac{\partial L}{\partial C_t}\frac{\partial C_t}{\partial i_t} = \delta_{C_t} \cdot C'_t\\
\frac{\partial L_t}{\partial Cc_t} &= \frac{\partial L}{\partial C_t}\frac{\partial C_t}{\partial Cc_t} = \delta_{C_t} \cdot i_t\\\\
\text{对所有参数求导: }\\
\frac{\partial L_t}{\partial W_{i}} &= \delta_{i_t} \cdot i_t(1-i_t)\\
\frac{\partial L_t}{\partial W_{f}} &= \delta_{f_t} \cdot f_t(1-f_t)\\
\frac{\partial L_t}{\partial W_{o}} &= \delta_{o_t} \cdot o_t(1-o_t)\\
\frac{\partial L_t}{\partial W_{cc}} &= \delta_{cc_t}\cdot (1-tanh^2{Cc_t})\\

\end{align}
$$


需要特殊注意的是之所以

$$
\begin{align}
\frac{\partial L_t}{\partial C_t} &= \frac{\partial L_t}{\partial h_t}\frac{\partial h_t}{\partial c_t}=\delta_{ht} \cdot o_t \cdot (1-tanh^2{C_t}) = \delta_{C_t}
\end{align}
$$

其原因是用了截断的BPTT，只考虑前一步，所以不会有递归。另外其实际计算时

$$
\begin{align}
\frac{\partial L_t}{\partial C_t}  = \delta_{ht} \cdot o_t \cdot (1-tanh^2{C_t}) + \delta_{C_{t+1}}
\end{align}
$$

则是因为$$C_t$$的梯度贡献不仅来自于当前步骤的计算还有前一步的结果。



## 小结

在lstm的整个推导过程中，耗时最久的是对cell state的求导计算。前向过程在colah的博客中解释的
很清楚。但是关于截断的BPTT和RTRL(real time recurrent learning)这两个在lstm求导中的应用
却不得不翻论文，结果却是翻了好久也没有几个人能真正把这个以比较好理解的方式明确说出来。所以结果就是
我知道这样做，但是却并不知道为什么。留下了疑点。现在虽然有所认识，但依然不是很明确。尽管如此还是
实现了一个100行不到的lstm。还是值得欣慰的。


# Refs   
  - <http://www.cs.utoronto.ca/~ilya/pubs/ilya_sutskever_phd_thesis.pdf>
  - <http://ml.cs.tsinghua.edu.cn/~jun/pub/lstm-parallel.pdf> 
  - <http://arunmallya.github.io/writeups/nn/lstm/#/>
  - <https://wiseodd.github.io/techblog/2016/08/12/lstm-backprop/>
  - <http://colah.github.io/posts/2015-08-Understanding-LSTMs/>     
  - <https://nic.schraudolph.org/teach/NNcourse/project.html>
  - <http://www.wildml.com/2015/10/recurrent-neural-network-tutorial-part-4-implementing-a-grulstm-rnn-with-python-and-theano/>
  - <https://r2rt.com/written-memories-understanding-deriving-and-extending-the-lstm.html#fnref2>      
