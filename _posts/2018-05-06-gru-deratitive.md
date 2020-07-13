---
title: GRU的推导和实现
layout: post
---

{{page.title}}
=============
<p class="meta">6 May 2018</p>

Table of Content
=================
   * [前向计算](#前向计算)
   * [反向推导](#反向推导)           
   * [小结](#小结)                  
   * [实现](https://github.com/haiy/rush_in_dl/blob/master/gru.py)                         
                            
                      
===========
               
### 前向计算

$$\begin{align}
\text{forward : }\\
z_t &= \sigma(W_z \cdot [h_{t-1},x_t]) \\
r_t &= \sigma(W_r \cdot [h_{t-1},x_t]) \\
h'_t &= tanh(W_{h'} \cdot [r_t * h_{t-1}, x_t]) \\
h_t &= (1 - z_t) * h_{t-1} + z_t * h'_t\\
y_t &= softmax(W_y \cdot h_t) \\\\
\text{Loss: }\\
L &= \sum^{t}_{i=0}{L_t} = -\sum^{t}_{i=0}y_ilog\hat{y_i}\\\\
\end{align}
$$

### 反向推导

### 计算图

这个图是从参考的文章里直接拿来的，需要自己画个更好。
<div align="center">
<img src="{{site.url}}/images/GRUComputeGraph.jpg" width="300px">
</div>

因为GRU中核心的要求的参数除$$\frac{\partial L_t}{\partial W_y}$$外,就是$$\frac{\partial L_t}{\partial W_z}$$,
$$\frac{\partial L_t}{\partial W_r}$$,$$\frac{\partial L_t}{\partial W_{h'}}$$这三个。

$$
\begin{align}
\frac{\partial L_t}{\partial W_z} &= \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial W_z}\\
&=\frac{\partial L_t}{\partial h_t}\sum_{i=1}^t\frac{\partial h_i}{\partial W_z}\frac{\partial h_i}{\partial W_z}\\

&=\frac{\partial L_t}{\partial h_t}\sum_{i=1}^t((\prod _{j=i}^{t-1}\frac{\partial h_{j+1}}{\partial h_{j}})
\overline{\frac{\partial h_i}{\partial W_z}})\\\\
\frac{\partial L_t}{\partial W_r} 
&= \frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial W_r}\\

&=\frac{\partial L_t}{\partial h_t}\sum_{i=1}^t((\prod _{j=i}^{t-1}\frac{\partial h_{j+1}}{\partial h_{j}})
\overline{\frac{\partial h_i}{\partial W_r}})\\\\
\frac{\partial L_t}{\partial W_{h'}} &= \frac{\partial L_t}{\partial {h'_t}} \frac{\partial h'_t}{\partial W_{h'}}\\

&=\frac{\partial L_t}{\partial h'_t}\sum_{i=1}^t((\prod _{j=i}^{t-1}\frac{\partial h_{j+1}}{\partial h_{j}})
\overline{\frac{\partial h'_i}{\partial W_{h'}}})
\end{align}
$$

此处$$\overline{\frac{\partial h'_i}{\partial W_{h'}}}$$ 的意思是将其他项都看作常数项时的求导。
上面的求导公式中都添加了乘积的计算。这个乘积的具体推导过程和RNN是基本一致的。
从上面三个式子可以看出接下来需要具体展开的求导过程由两种，
一种是$$\frac{\partial h_{j+1}}{\partial h_{j}}$$,另一种就是类似$$\overline{\frac{\partial h'_i}{\partial W_{h'}}}$$的2个。

$$
\begin{align}
\frac{\partial h_t}{\partial h_{t-1}} 
&= \frac{\partial h_t}{\partial {z_t}} \frac{\partial z_t}{\partial h_{t-1}} 
    + \frac{\partial h_t}{\partial h'_t}\frac{\partial h'_t}{\partial h_{t-1}} 
    + \overline{\frac{\partial h_t}{\partial h_{t-1}} }\\
&= \frac{\partial h_t}{\partial {z_t}} \frac{\partial z_t}{\partial h_{t-1}} 
    + \frac{\partial h_t}{\partial h'_t}(\frac{\partial h'_t}{\partial r_t}\frac{\partial r_t}{\partial h_{t-1}} 
    + \overline{\frac{\partial h'_t}{\partial h_{t-1}}}) + \overline{\frac{\partial h_t}{\partial h_{t-1}} } \\
&= (-h_{t-1}+h'_t)\cdot z_t\cdot(1-z_t)W_z + z_t\cdot(1-tanh^2h'_t)((W_{h'}h_{t-1}\cdot(r_t(1-r_t))W_r+W_{h'}*r_t) + (1-z_t)
\end{align}
$$

在上述的推导过程中可以看到要对三个偏导计算的复杂度都是$$O(n^2)$$.那么有木有更高效的算法呢？通过对公式的进一步推导之和是有的。

$$
\begin{align}
\frac{\partial L}{\partial W_z} 
&= \sum_{t=1}^n(\frac{\partial L_t}{\partial h_t} \frac{\partial h_t}{\partial W_z})\\
&=\sum_{t=1}^n(\frac{\partial L_t}{\partial h_t}\sum_{i=1}^t\frac{\partial h_t}{\partial h_i}\frac{\partial h_i}{\partial W_z})\\
&=\sum_{t=1}^n\sum_{i=1}^t\frac{\partial L_t}{\partial h_i}\frac{\partial h_i}{\partial W_z}\\
\end{align}
$$

对$$\frac{\partial L_t}{\partial h_i}$$的计算进行前后调整，这个调整实际上是将从t往前计算梯度的过程，转变成从后往前求。总量不变。

$$
\begin{align}
\frac{\partial L}{\partial W_z} 
&=\sum_{t=1}^n(\sum_{i=t}^t\frac{\partial L_i}{\partial h_t})\overline{\frac{\partial h_t}{\partial W_z}}\\
&=\sum_{t=1}^n((\sum_{i=t+1}^n\frac{\partial L_i}{\partial h_{t+1}})
\frac{\partial h_{t+1}}{\partial h_t} + \frac{\partial L_t}{\partial h_t})\overline{\frac{\partial h_t}{\partial W_z}}
\end{align}
$$

其实上式的核心点在于以累加的方式更新:

$$
\begin{align}
\sum_{i=t}^t\frac{\partial L_i}{\partial h_t}
&=(\sum_{i=t+1}^n\frac{\partial L_i}{\partial h_{t+1}})
\frac{\partial h_{t+1}}{\partial h_t} + \frac{\partial L_t}{\partial h_t}
\end{align}
$$


## 小结

GRU和LSTM的核心区别在于将三个门转成2个。减少了一定量的参数，但是二者的核心思想都是通过门路来调整
信息的传递。孰优孰劣并无定论。一图胜千言，有了计算图对反向传播的求导理解事半功倍。

### Refs: 

- [Understanding-LSTMs](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- [gru-scratch](http://gluon.mxnet.io/chapter05_recurrent-neural-networks/gru-scratch.html)
- [GRUBPTTTutorial](https://book.haihome.top/deeplearning/GRU-BPTTTutorial.pdf)
- [erikvdplas-GRU](https://github.com/erikvdplas/gru-rnn/blob/master/main.py)ß