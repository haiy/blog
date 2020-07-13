---
title: 简单NN的反向传播推导
layout: post
---

{{page.title}}
=============

<p class="meta">19 Mar 2018</p>

Table of Content
=================
   * [前向计算](#前向计算)
   * [反向推导](#反向推导)                             
   * [实现](https://github.com/haiy/rush_in_dl/blob/master/nn.py)                         
                            
                      
===========
               

实际上这两个一个3层神经网络模型的前向和反向计算过程，另一个RNN的前向和反向传播过程。其中RNN的需要注意的是其
反向主要区别在于其累积了多个时间步骤上的梯度。

# 多层神经网络(Neural Network)的前向和反向推导     

## 前向计算

$$
h_1 = xW_1 + b_1\\
o_1 = sigmoid(h_1) \\
h_2 = o_1*W_2 + b_2 \\
o_2 = tanh(h_2) \\
h_3 = o_2*W_3+b_3\\
o_3 = y'=softmax(h_3)
$$

在这选用交叉熵(cross entropy)作为损失函数.

$$
L(y,o) = - \sum_i y_i log(o_i)
$$


## 反向推导

在NN中反向求偏导数的变量是针对L求各个神经元的权重。因此目标偏导数主要是:

$$
\frac{\partial L}{\partial W_3},
\frac{\partial L}{\partial b_3},
 \frac{\partial L}{\partial W_2},
 \frac{\partial L}{\partial b_2},
  \frac{\partial L}{\partial W_1},
 \frac{\partial L}{\partial b_1}
$$

具体求导过程如下:

$$
\frac{\partial L}{\partial W_3} = (y'-y)o_2\\
\frac{\partial L}{\partial b_3} = (y'-y)\\
\frac{\partial L}{\partial h_2} = \sigma = (y'-y)W_3(1-tanh^2(h_2))\\

\frac{\partial L}{\partial W_2} = \frac{\partial L}{\partial h_2}\frac{\partial h_2}{\partial W_2}=\sigma{o_1}\\
\frac{\partial L}{\partial b_2} = \frac{\partial L}{\partial h_2}\frac{\partial h_2}{\partial b_2}=\sigma\\
\frac{\partial L}{\partial o_1} = \frac{\partial L}{\partial h_2}\frac{\partial h_2}{\partial o_1}=\sigma{W_2}\\
\frac{\partial L}{\partial h_1} = \beta = \frac{\partial L}{\partial o_1}\frac{\partial o_1}{\partial h_1} = \sigma{W_2}sigmoid(h_1)( 1-sigmoid(h_1))\\
\frac{\partial L}{\partial W_1} = \beta x \\
\frac{\partial L}{\partial b_1} = 1 

$$


# Refs
    
   - [cs231n](http://cs231n.github.io/optimization-2/)  