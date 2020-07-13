---
title: 博客搭建相关
date: 2015-07-06 00:00:00 Z
layout: post
commentIssueId: 6
---

{{ page.title }}
================

<p class="meta">8 July 2015 </p>

#### 1.定制的google 搜索

主要参考了这篇[博客](http://digitaldrummerj.me/blogging-on-github-part-7-adding-a-custom-google-search/), 但是
这篇博客中其实还有几个地方没有写清楚，下面就整理下我的google 定制搜索(Custom Search Engine,cse)的整个流程。

主要流程是先在google的站点管理里面认证自己的网站，证明对网站具有所有权，然后将该站点添加到自己的google的定制
搜索里面，最后在自己的博客里面部署代码。具体的流程如下：

- 打开[Google Search Console](https://www.google.com/webmasters/tools/home?hl=en) , 验证自己的网站。这个是
验证的[官方教程](https://support.google.com/webmasters/answer/34592?hl=en). 当然了，验证前你肯定得把自己的网站
添加到Google Search Console里面，如果不知道怎么弄，看
[这里](https://support.google.com/webmasters/topic/4564315?hl=en&ref_topic=4581229) .
- 验证完后，就可以在先大概看下这个[cse文档](https://support.google.com/customsearch#topic=4513742), 主要是先大概
看下有个整体的概念，然后就可以玩起来咯，来[这里](https://cse.google.com/cse/all) 开动，暂时需要做的有这么几个
方面:
    - a.新建好自己的CSE，
    - b.然后拿到自己CSE的js代码[Edit search engine -> Setup -> Basics -> Get code]，
    - c.建立下主页的索引，待会会用到索引数据来测试CSE

- 在自己的博客新建搜索页面，如我的[搜索页面](https://github.com/haiy/haiy.github.io/blob/master/search.html),
将刚才得到的cse的js代码copy进来，保存。这个时候CSE基本是已经可以用的了。如果不能，请确认索引有没有建好。
- 构建好基本的CSE之后，接下来就是让它更自然点，如你现在看到我的博客上的样子。主要涉及的有这几个方面：
    - 搜索框， 这个是通过在default模版页面添加search form，
        可参考[我的](https://github.com/haiy/haiy.github.io/blob/master/_layouts/default.html#L20-L29) 。
    - 搜索结果页面跳转, 这个主要是想让搜索框的结果直接出现在结果页面，也就是自动提交到CSE,
        关键是[这儿](https://github.com/haiy/haiy.github.io/blob/master/search.html#L19]的queryParameterName)。
    - 搜索结果页面样式, 这个主要涉及两个地方，一个是CSE中的[Edit search engine -> Look and feel],另外一个就是
        结果页的模版样式，以及CSS。

经过上述步骤后自己的CSE应该就可以看起来不错啦，过两天等google的爬虫爬完后，就会用起来不错啦。

#### 2. 基于github issue的评论系统

这个评论参考了多说，disque，但是感觉不够干净，自己尝试过直接用新建issue但效果看起来都不很如意，直到遇见了
[它](http://ivanzuzak.info/2011/02/18/github-hosted-comments-for-github-hosted-blogs.html),顿时感觉遇到了
知音。搭建的过程完全参考该篇博客，么有什么特别需要注意的，按步骤来就可以的了拉。其主要是调用了github的issue
的[API](https://developer.github.com/v3/), 该API中获取issues的接口为
https://api.github.com/repos/izuzak/izuzak.github.com/issues/12/comments, 在实际使用的时候要将里面的repos等信息更换为自己的。注意，一定要把博客中提到的两个js库加到页面中。

#### 3. www.haiyf.space和haiy.space的设置

这个设置主要是域名提供商那儿的设置，我的域名是从Namecheap买的，所以我在namecheap设置的。至于如果给自己的
github主页添加特定的域名，可以参考[这儿](http://davidensinger.com/2013/03/setting-the-dns-for-github-pages-on-namecheap/) 。
关于www的支持问题则是在namecheap的Customize Parked Page中添加重定向，实质上是将www.haiyf.space重定向到haiyf.space.

#### 4. Math Functions

关于Latex语法主要参考[这儿](http://mirrors.ustc.edu.cn/CTAN/info/lshort/english/lshort.pdf). 
而关于这个数学公式显示的js插件，则可参考[这个](http://docs.mathjax.org/en/latest/start.html)。

x^2_1
When a ne 0 , there are two solutions to \(ax^2 + bx + c = 0\) and they are

$$x = {-b \pm \sqrt{b^2-4ac} \over 2a }.$$

我在测试这个玩意\( 1/x^{2} \)看看到底怎么用


