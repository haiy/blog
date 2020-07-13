---
title: 常用损失函数和激活函数及导数
layout: post
---

{{page.title}}
=============

<p class="meta">14 Mar 2018</p>

Table of Contents
========
* [1 LogisticRegression](#1-logisticregression)   
* [2 softmax](#2-softmax)
* [3 cross entroy with softmax](#3-cross-entroy-with-softmax)
* [4 sigmoid,tanh,...](#4-sigmoid-tanh)
* [Ref](#ref)
   
   
# 最常用的：

## 1. LogisticRegression

- LogisticRegression:     

$$  p(x) = \frac{1}{(1+e^{-wx})}$$

- Odds :      

$$\frac{p(x)}{1-p(x))} = e^{wx}$$

- Log Odds:      

$$ ln(\frac{p(x)}{1-p(x)}) = wx $$

- Loss $$y\in\{0,+1\}$$:

    $$J(\theta)=-\frac{1}{m}\sum_{i=1}^{m}y^{i}\log(h_\theta(x^{i}))+(1-y^{i})\log(1-h_\theta(x^{i}))$$

    其导数：

$$
\begin{align} 
\frac{\partial J(\theta)}{\partial \theta_j}  &= 
\frac{\partial}{\partial \theta_j} \,\frac{-1}{m}\sum_{i=1}^m 
\left[ y^{(i)}\left(\log(h_\theta \left(x^{(i)}\right)\right) +
(1 -y^{(i)})\left(\log(1-h_\theta \left(x^{(i)}\right)\right)\right]\\[2ex]
&\underset{\text{linearity}}= \,\frac{-1}{m}\,\sum_{i=1}^m 
\left[ 
y^{(i)}\frac{\partial}{\partial \theta_j}\log\left(h_\theta \left(x^{(i)}\right)\right) +
(1 -y^{(i)})\frac{\partial}{\partial \theta_j}\left(\log(1-h_\theta \left(x^{(i)}\right)\right)
\right]\\[2ex]
&\underset{\text{chain rule}}= \,\frac{-1}{m}\,\sum_{i=1}^m 
\left[ 
y^{(i)}\frac{\frac{\partial}{\partial \theta_j}(h_\theta \left(x^{(i)}\right)}{h_\theta\left(x^{(i)}\right)} +
(1 -y^{(i)})\frac{\frac{\partial}{\partial \theta_j}\left(1-h_\theta \left(x^{(i)}\right)\right)}{1-h_\theta\left(x^{(i)}\right)}
\right]\\[2ex]
&\underset{h_\theta(x)=\sigma\left(\theta^\top x\right)}=\,\frac{-1}{m}\,\sum_{i=1}^m 
\left[ 
y^{(i)}\frac{\frac{\partial}{\partial \theta_j}\sigma\left(\theta^\top x^{(i)}\right)}{h_\theta\left(x^{(i)}\right)} +
(1 -y^{(i)})\frac{\frac{\partial}{\partial \theta_j}\left(1-\sigma\left(\theta^\top x^{(i)}\right)\right)}{1-h_\theta\left(x^{(i)}\right)}
\right]\\[2ex]
&\underset{\sigma'}=\frac{-1}{m}\,\sum_{i=1}^m 
\left[ y^{(i)}\,
\frac{\sigma\left(\theta^\top x^{(i)}\right)\left(1-\sigma\left(\theta^\top x^{(i)}\right)\right)\frac{\partial}{\partial \theta_j}\left(\theta^\top x^{(i)}\right)}{h_\theta\left(x^{(i)}\right)}\\ -
(1 -y^{(i)})\,\frac{\sigma\left(\theta^\top x^{(i)}\right)\left(1-\sigma\left(\theta^\top x^{(i)}\right)\right)\frac{\partial}{\partial \theta_j}\left(\theta^\top x^{(i)}\right)}{1-h_\theta\left(x^{(i)}\right)}
\right]\\[2ex]
&\underset{\sigma\left(\theta^\top x\right)=h_\theta(x)}= \,\frac{-1}{m}\,\sum_{i=1}^m 
\left[ 
y^{(i)}\frac{h_\theta\left( x^{(i)}\right)\left(1-h_\theta\left( x^{(i)}\right)\right)\frac{\partial}{\partial \theta_j}\left(\theta^\top x^{(i)}\right)}{h_\theta\left(x^{(i)}\right)} \\-
(1 -y^{(i)})\frac{h_\theta\left( x^{(i)}\right)\left(1-h_\theta\left(x^{(i)}\right)\right)\frac{\partial}{\partial \theta_j}\left( \theta^\top x^{(i)}\right)}{1-h_\theta\left(x^{(i)}\right)}
\right]\\[2ex]
&\underset{\frac{\partial}{\partial \theta_j}\left(\theta^\top x^{(i)}\right)=x_j^{(i)}}=\,\frac{-1}{m}\,\sum_{i=1}^m \left[y^{(i)}\left(1-h_\theta\left(x^{(i)}\right)\right)x_j^{(i)}-
\left(1-y^{i}\right)\,h_\theta\left(x^{(i)}\right)x_j^{(i)}
\right]\\[2ex]
&\underset{\text{distribute}}=\,\frac{-1}{m}\,\sum_{i=1}^m \left[y^{i}-y^{i}h_\theta\left(x^{(i)}\right)-
h_\theta\left(x^{(i)}\right)+y^{(i)}h_\theta\left(x^{(i)}\right)
\right]\,x_j^{(i)}\\[2ex]
&\underset{\text{cancel}}=\,\frac{-1}{m}\,\sum_{i=1}^m \left[y^{(i)}-h_\theta\left(x^{(i)}\right)\right]\,x_j^{(i)}\\[2ex]
&=\frac{1}{m}\sum_{i=1}^m\left[h_\theta\left(x^{(i)}\right)-y^{(i)}\right]\,x_j^{(i)}
\end{align}
$$



 

- Loss $$y\in\{-1,+1\}$$:

$$     L_{log}(w,b,X,y) = \sum_{i=0}^{N}log(1+e^{-y_i(W^Tx_i+b)})$$

- 链式法则求导:

$$
l(a) = \ln(a) = z
$$

$$             
l^{\prime}(a) = \frac{\partial z}{\partial a} = \frac{1}{\ln(e)(a)} = \frac{1}{a}
$$


$$
f(b) = 1 + e^b = v
$$

$$
f^{\prime}(b) = \frac{\partial v}{\partial b} = e^b
$$



$$
g(c) = -yc = u
$$

$$
g^{\prime}(c) = \frac{\partial u}{\partial c} = -y
$$



$$
h(w) = wx = t
$$

$$
h^{\prime}(w) = \frac{\partial t}{\partial w} = x
$$


将上面的函数拼一起:

$$
l(f(g(h(w)))) = \ln(1 + e^{-y(wx)})
$$

$$
l^{\prime}(f(g(h(w))))
= \frac{\partial z}{\partial v} \frac{\partial v}{\partial u} \frac{\partial u}{\partial t} \frac{\partial t}{\partial w}
=
\frac{1}{1+e^{-y(wx)}} { e^{-y(wx)} }{( -y)}{ x}
=
\frac{-yxe^{-y(wx)}}{1+e^{-y(wx)}}
$$


## 2 softmax 

- Softmax

$$ p_j = \frac{e^{a_i}}{\sum_{k=1}^N e^a_k} $$

- Stable Softmax, 为了避免 分子和分母因为$$e^a_i$$过大，造成数值计算不准，所以实际计算的时候分子分母同时倍乘一个常数(通常 $$log{C}=-max_jf_j$$)，
推导如下：


$$p_j = \frac{e^{a_i}}{\sum_{k=1}^N e^{a_k}} = \frac{Ce^{a_i}}{C\sum_{k=1}^N e^{a_k}} = \frac{e^{a_i + \log(C)}}{\sum_{k=1}^N e^{a_k + \log(C)}}$$

- 偏导数
    
    $$\frac{\partial p_j}{\partial a_j} = \frac{\partial  \frac{e^{a_i}}{\sum_{k=1}^N e^{a_k}}}{\partial a_j}$$
    
    根据求导除法规则,对于$$f(x) = \frac{g(x)}{h(x)}$$，那么其导数为：$$f^\prime(x) = \frac{ g\prime(x)h(x) - h\prime(x)g(x)}{h(x)^2}$$ .
    在这儿, $$g(x) = e^{a_i}$$, $$h(x) = \sum_{k=1}^ N e^{a_k}$$。这里对于指数求和的$$h(x)$$来说$$h'(e^{a_j})= e^{a_j}$$，因为其中肯定含有
    要求的偏导的那一项。而对与$$g(x)$$来说，当i=j时，也就是当前要求导的项和计算的项一致时，
    $$g'(e^{a_i}) = e^{a_j}$$,否则的话$$g'(e^{a_i}) = 0$$.
    
    因此，当i=j时，
    
    $$\begin{align}
\frac{\partial  \frac{e^{a_i}}{\sum_{k=1}^N e^{a_k}}}{\partial a_j}&= \frac{e^{a_i} \sum_{k=1}^N e^{a_k} - e^{a_j}e^{a_i}}{\left( \sum_{k=1}^N e^{a_k}\right)^2} \\
&= \frac{e^{a_i} \left( \sum_{k=1}^N e^{a_k} - e^{a_j}\right )}{\left( \sum_{k=1}^N e^{a_k}\right)^2} \\
&= \frac{ e^{a_j} }{\sum_{k=1}^N e^{a_k} } \times \frac{\left( \sum_{k=1}^N e^{a_k} - e^{a_j}\right ) }{\sum_{k=1}^N e^{a_k} } \\
&= p_i(1-p_j)
\end{align}
    $$
    
    当 $$i\neq{j}$$,
    
    $$
    \begin{align}
    \frac{\partial  \frac{e^{a_i}}{\sum_{k=1}^N e^{a_k}}}{\partial a_j}&= \frac{0 - e^{a_j}e^{a_i}}{\left( \sum_{k=1}^N e^{a_k}\right)^2} \\
    &= \frac{- e^{a_j} }{\sum_{k=1}^N e^{a_k} } \times \frac{e^{a_i} }{\sum_{k=1}^N e^{a_k} } \\
    &= - p_j.p_i
    \end{align}
     $$
     
     综上，softmax的偏导为：
     
     $$
    \frac{\partial p_j}{\partial a_j} = 
\begin{cases}p_i(1-p_j) &  if & i=j \\
-p_j.p_i & if & i \neq j
\end{cases} 
    $$
    
## 3 cross entroy with softmax   
softmax作为输出层，在计算loss的时候通常和交叉熵连用。交叉熵主要是用来衡量两个概率分布之间概率差异大小的。是除了均方差外另一个
用的比较多的loss评价。

- cross entropy
  
    $$ H(y,p) = - \sum_i y_i log(p_i)$$
  
- 交叉熵的导数
 
 $$
 \begin{align}
L &= - \sum_i y_i log(p_i) \\
\frac{\partial L}{\partial a_i} &= - \sum_k y_k \frac{\partial log(p_k)}{\partial a_i } \\
&= - \sum_k y_k \frac{\partial log(p_k)}{\partial p_k} \times \frac{\partial p_k}{ \partial a_i} \\
&= - \sum y_k \frac{1}{p_k} \times \frac{\partial p_k}{\partial a_i} \\
\end{align} 
$$  

- 带softmax的cross entropy的导数
  
  $$
  \begin{align}
\frac{\partial L}{\partial a_i}  &= -y_i(1-p_i) - \sum_{k\neq i} y_k \frac{1}{p_k}(-p_k.p_i) \\
&= -y_i(1-p_i) + \sum_{k \neq 1} y_k.p_i \\
&= - y_i + y_ip_i + \sum_{k \neq i} y_k.p_i \\
&= p_i\left( y_i +  \sum_{k \neq i} y_k\right) - y_i \\
&= p_i\left( y_i +  \sum_{k \neq i} y_k\right)  - y_i
\end{align}
$$

    因为y是标签的one-hot编码的矩阵，所以$$\sum_k y_k = 1$$，并且$$y_i +  \sum_{k \neq i} y_k = 1$$,
    综上：
    
    $$\frac{\partial L}{\partial a_i} = p_i - y_i$$


## 4 sigmoid, tanh

- sigmoid
    
    $$ \sigma(x) = \frac{1}{1+e^{-x}} $$
    
    导数：
    
    $$ \sigma'(x) = s(x)(1-s(x))$$

- tanh

   $$ tanh(x) =   \frac{e^x-e^{-x}}{e^x-e^{-x}}  = 2\sigma(2x)-1 $$
   
   导数:
   
   $$tanh'(x) = 1 - tanh^2(x) $$


- ReLU, PReLU,ELU, SoftPlus

   激活函数和其导数表：
   
   <img src="/images/activation_fns/part-1.png" height="315px">
   <img src="/images/activation_fns/part-2.png" height="400px">
          


  



# Ref:
LR     
   - <http://cs231n.github.io/optimization-2/>    
   - <https://en.wikipedia.org/wiki/Linearity_of_differentiation>   
   - <https://en.wikipedia.org/wiki/Chain_rule>      
   - <https://en.wikipedia.org/wiki/Differentiation_rules#Derivatives_of_exponential_and_logarithmic_functions>     
   - <https://en.wikipedia.org/wiki/Logistic_regression>
   - <https://stats.stackexchange.com/questions/219241/gradient-for-logistic-loss-function>
   - <https://math.stackexchange.com/questions/874481/derivative-of-logistic-loss-function> 
   - <https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/pdfs/40%20LogisticRegression.pdf>
   - <https://math.stackexchange.com/questions/477207/derivative-of-cost-function-for-logistic-regression>   

softmax            
   - <https://stats.stackexchange.com/questions/235528/backpropagation-with-softmax-cross-entropy>          
   - <https://deepnotes.io/softmax-crossentropy>       
   - <http://cs231n.github.io/linear-classify/#softmax>          
    
softmax cross entropy loss         
   - <https://deepnotes.io/softmax-crossentropy>      
   - <https://www.ics.uci.edu/~pjsadows/notes.pdf>     
   - <http://cs231n.github.io/neural-networks-case-study/#together>
   - <http://www.wildml.com/2015/09/implementing-a-neural-network-from-scratch/>      
   - <https://stats.stackexchange.com/questions/235528/backpropagation-with-softmax-cross-entropy>
   - <https://eli.thegreenplace.net/2016/the-softmax-function-and-its-derivative/>
   - <http://neuralnetworksanddeeplearning.com/> 

ReLU, PReLU,ELU, SoftPlus          
   - <https://en.wikipedia.org/wiki/Activation_function>           