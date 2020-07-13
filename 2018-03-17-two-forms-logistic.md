---
title: 逻辑回归两种损失函数
layout: post
---

{{page.title}}
=============

<p class="meta">17 Mar 2018</p>

Table of Contents
=================
  * [1. 哪个对？](#1-哪个对)
  * [2. 有什么区别呢？](#2-有什么区别呢)
  * [3. 都是怎么得来的？](#3-都是怎么得来的)
  * [4. 为什么会有这两种形式？](#4-为什么会有这两种形式)
  * [Ref](#ref)

关于这个sigmoid函数的的样子大家都见过不少了，但是关于逻辑回归的损失函数样式的定义，或多或少我们可能都见过
以下两种：
 
- Loss 1:

$$     \begin{align}
l=&-\sum_i\left[y_i\log p+(1-y_i)\log(1-p)\right]\\
=&\sum_i\left[y_iW^{\mathrm{T}}x_i-\log(1+e^{W^{\mathrm{T}}x_i})\right]
\end{align}
$$

- Loss 2:

$$     l = \sum_{i=0,1}^{N}log(1+e^{-y_i(W^Tx_i+b)})$$


那么这两种到底有什么区别呢？哪个对呢？都是怎么得来的呢？为什么会有这两种形式？

## 1. 哪个对？

两个都对。

## 2. 有什么区别呢？

两个的区别其实是根据$$y$$的取值区间不同得到的。其中：
 - Loss1, $$y \in \{0, 1\}$$
 - Loss2, $$y \in \{-1, +1\}$$
 
## 3. 都是怎么得来的？     
先定义：

$$ \sigma(z) = \frac{e^{z}}{1 + e^{z}} = \frac{1}{1+e^{-z}} $$

 
它有个很漂亮的属性：$$\sigma(-z) = 1-\sigma(z)$$
 
正样本概率公式：

 $$P(y=1|x) = \sigma(z) = \frac{1}{1 + e^{-w^{T}x}}, (tip: z = W^Tx)$$
 

 
 - Loss1，当负样本标签取值为0时， 
 
     $$P(y=0|x) =1-\sigma(z) =1- \frac{1}{1 + e^{-w^{T}x}}$$
    
    此时：
    
    $$\mathbb{P}(y|z)  =\sigma(z)^y(1-\sigma(z))^{1-y}$$
    
    简单解释下，这个形式的y条件概率函数其实也就是伯努利分布的样子。   
    其负对似然函数：
     
    \begin{equation}
    \begin{aligned}
    l(z)=-\log\big(\prod_i^m\mathbb{P}(y_i|z_i)\big)=-\sum_i^m\log\big(\mathbb{P}(y_i|z_i)\big)=\sum_i^m\left[-y_iz_i+\log(1+e^{z_i})\right]
    \end{aligned}
    \end{equation}
     
     至此，Loss1也就得到了
     
 - Loss2, 当负样本取值为1时，   
 
    $$P(y=-1|x) = 1-\sigma(z) =\sigma(-z) = \frac{1}{1 + e^{w^{T}x}}$$
    
    此时：
    
    \begin{equation}
    \mathbb{P}(y|z)=\sigma(yz). 
    \end{equation}

    简单解释下，因为 $$P(y=1|x)$$时和$$P(y=-1|x)$$时概率的计算唯一差别也就时正负号，而y标签值又正好是+1或-1，
    所以y的条件概率公式就写成上面形式了。
    那么至此Loss2也就呼之欲出了：
    
    \begin{equation}
    \begin{aligned}
    L(z)=-\log\big(\prod_j^m\mathbb{P}(y_j|z_j)\big)=-\sum_j^m\log\big(\mathbb{P}(y_j|z_j)\big)=\sum_j^m\log(1+e^{-yz_j})
    \end{aligned}
    \end{equation}

## 4. 为什么会有这两种形式？
好好好，你说的都对。那为什么会有这两种形式？搞数学的炫耀智商么？我觉得应该是。数学的美感不正在其中么~,:joy:
不过认真的说有以下原因：

  * 二者理论基础不一样，Loss1是根据[Bernoulli probability model](https://en.wikipedia.org/wiki/Bernoulli_distribution)来玩的，
        Loss2有点长的和SVM很像。
  
  * 实际计算考虑，$$y\in\{0,1\}$$，据此 
        $$\mathbb{P}(y|z)=\sigma(z)^y(1-\sigma(z))^{1-y}$$ 
  能更好的计算偏导数，
        
       $$\frac{\partial \sigma(z)}{ \partial z}=\sigma(z)(1-\sigma(z))$$
        

至此，基本弄清二者的关系。                


# Ref:

- <https://stats.stackexchange.com/questions/250937/which-loss-function-is-correct-for-logistic-regression>
- <https://stats.stackexchange.com/questions/145147/two-equivalent-forms-of-logistic-regression>
- <https://stats.stackexchange.com/questions/229645/why-there-are-two-different-logistic-loss-formulation-notations>
 
