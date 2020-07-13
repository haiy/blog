---
title: 对话系统的调研：最近的进展和前沿
layout: post
---

## {{page.title}}

<p class="meta">11 Jun 2019</p>

## 对话系统的调研：最近的进展和前沿

### 摘要

对话系统已经引起了越来越多的注意。最近对话系统的进展很大程度是由深度学习技术带来的，很多大数据领域也通过采用深度学习来得到了强化，比如计算机视觉，自然语言处理，以及推荐系统。对于对话系统来说，深度学习可以从巨大的数据中学习有意义的特征表示以及回复生成策略，只需要很少量的手工操作。在这片文章中，我们从各个角度来对对话系统最近的进展进行了回顾，并且讨论了一些可能的研究方向。需要注意的是，我们把现有的对话系统整体上分成了任务型和非任务型模型，然后详细的深度学习是如何基于表示算法来帮助它们的。最后讨论了一些有可能把对话系统带入新世纪的一些吸引人的研究方向。

### 1 介绍

想要一个有足够智力的虚拟助手或者一个聊天陪伴系统看起来有些像白日梦，并且可能会长时间只存在于科幻电影中。最近，人机对话系统已经因为其潜在的大好前景和诱人的商业价值，引起了日益增长的关注。随着大数据和深度学习技术的发展，创造一个自动的人机对话系统，作为我们的个人助理或者聊天伙伴，已经不再是幻想。一方面，现在我们能够很方便的接触网上的聊天大数据，并且我们有可能学会如何回复和在基本任何输入的情况下该回复什么。正是这些给了我们构建人类和机器之间的数据驱动，开放领域的对话系统提供了可能。另一方面，深度学习已经在大数据上被证明能够很有效的习得复杂模式并且推动了非常多的研究领域，例如计算机视觉，自然语言处理和推荐系统。因此，出现了一大批文献从很多的角度通过深度学习利用大量数据来推进对话系统。

根据应用类型，对话系统可以大体分为两类-(1)任务驱动型(2)非任务驱动型(也即是大家熟知的聊天机器人)。任务驱动系统目标是帮助用户来完成特定的任务(举例来说，产品查找，食宿预定等）。任务型对话系统广泛使用的方法如图1所示，将整个对话回复过程看成是一个管道流水线。
整个系统首先理解人类给出的信息，把它用内部状态来表示，然后基于对话状态根据对话策略来进行一些动作，最终这个动作被转换成自然语言作为其展现形式。
尽管语言理解是基于统计模型的，但是大部分部署的对话系统还是用手动的特征或者手工的规则来进行状态描述和行为空间的表示,意图识别和槽位填充。这就不仅使得部署一个真实的对话系统不仅代价高昂并且耗时长久，并且限制了其在其他领域的使用。最近，开发出来了很多基于深度学习的算法通过学习特征在高维空间的分布来减轻这些问题，并在这些方面取得了显著的提升。此外，还有一些构建端到端的任务型对话系统的尝试，这些尝试拓宽了传统管道式流程中状态空间的表示并且对于标注预料以外的回复的泛化生成。非任务型对话系统的目标主要是是和人类互动提供合理的回复和娱乐活动。比较显著的特点是它们主要是关注于在开放领域和人类的对话。尽管非任务型对话系统看起来是都是在闲聊，但是在很多现实应用中都是占主导地位的。就像在文献[111](Z. Yan, N. Duan, P. Chen, M. Zhou, J. Zhou, and Z. Li. Building task-oriented dialogue systems for online shopping. In AAAI Conference on Artificial Intelligence, 2017)中所显示的，在线上购物场景下几乎80%的聊天都是闲聊，并且对这些的处理和用户体验有着密切关系。整体来说，对于非任务型对话系统主要发展了两种主要的方案-(1)生成式方法如在对话过程中给你生成合适回复的seq2seq模型，以及(2)检索式方法，也就是从现有的语料库中来选择出回复。

近来大数据和深度学习技术的发展已经极大地促进了任务型和非任务型对话系统，并在对话系统方面激发出了非常多的基于深度学习的研究。在本文中，我们的目标是1)对对话系统进行一个整体的回复尤其是近期由深度学习带来的，2）讨论一些可能的研究方向。文章主要结构如下。首先在第二部分回顾了包含流水线和端到端的任务型对话系统。在第三部分，我们首先介绍了神经生成方法，包括流行的模型和热点研究问题；然后详细介绍了基于检索的方法。在第四部分，我们基于一些研究方向做了下总结。

### 2. 任务型对话系统

任务型对话系统是对话系统里一个重要的分支。在这部分，我们将回顾下流水线和端到端的任务型对话系统。

### 2.1 管道式方法

典型的管道式任务型对话系统结构可以看图1.其主要有四个组成部分：

- 语言理解。通常大家称作NLU(自然语言理解)模块，负责将用户的话语解析成预定义的语义槽位。
- 对话状态跟踪。其管理着每轮的输入和对话历史，输出当前的对话状态。
- 对话系统策略学习。主要学习基于当前策略的下个行为。
- 自然语言生成(NLG)。主要负责把选择的行为和表现方式对应起来并生成回复。

在接下来的几个子部分，我们将对每个模块的最新的方法深入了解。

### 2.1.1 语言理解

给定一个用户语句，自然语言理解将其映射到对应语义槽位里。槽位是基于不同的场景预先定义的。表1给出了一个自然语言表示的样例，

![](/images/dialogue_system.png)



其中“New York”是方位的具体槽位值，领域和意图也分别有具体的对应。通常有两种类型的表示。一个是语句级别的类别，如用户的意图和语句的分类。另一个是单词级别的抽取信息，如命名实体识别和槽位填充。

意图识别是用来识别一个用户的意图的。其将用户的语句分类为很多预先定义好的意图里面的一个。深度学习已经成功的应用在意图识别的问题上。(Use of kernel deep convex networks and end-to-end learning for spoken language understanding. Towards deeper understanding: Deep convex networks for semantic utterance classification. Zeroshot learning and clustering for semantic utterance classification using deep learning)
特别的是,文献(Query intent detection using convolutional neural networks)中用CNN来抽取查询的向量表示作为特征来进行查询分类。此外基于CNN的文本分类方法也有类似于以下2文的方法：(Learning deep structured semantic models for web search using clickthrough data. Learning semantic representations using convolutional neural networks for web search.)。类似的方法也用在了类别和领域分类上。

槽位填充是对话语言理解中另一个比较挑战的问题。和意图识别不同，槽位填充通常定义为一个序列标注的问题，也就是句子中的每个单词都被分配了一个语义标签。输入是由一组有序单词组成句子，输出是槽位(概念ID)的序列，每个词一个对应的输出。这两篇文章(Deep belief network based semantic taggers for spoken language understanding.Use of kernel deep convex networks and end-to-end learning for spoken language understanding.)用了深度信念网络来解决这个问题，取得了比基准CRF模型好很多的效果。用RNN的方法主要有(Investigation of recurrent-neural-network architectures and learning methods for spoken language understanding.Recurrent neural networks for language understanding. Deep belief nets for natural language call-routing. Spoken language understanding using long short-term memory neural networks.)。由NLU生成的语义表示接下来会由对话管理模块进一步处理。一个典型的对话管理模块包含两个步骤-对话状态根据和策略学习。

### 2.1.2 对话状态跟踪

跟进对话状态是对话系统中用来保障系统健壮性的核心组件。它预估了对话中每轮的用户目标。一个对话状态Ht是t时刻会话过程的表示。这个经典的状态结构通常称作是填槽或者语义帧。用人工制定的规则来选择最有可能的结果是一种比较传统的做法，并且在大多数商业实现中都广泛采用(A form-based dialogue manager for spoken language applications)。然而，这些基于规则的系统都倾向于经常出错，通常最有可能的结果并不一定是是想要的(Web-style ranking and slu combination for dialog state tracking.)。

一个统计对话系统维护了一个关于真实对话状态的多重假设，以此来应对噪声条件和歧义。(The hidden information state model: A practical framework for pomdpbased spoken dialogue management.)在对话状态跟踪挑战赛(DSTC)里，结果的形式是给出每轮对话中每个槽位的概率分布。在DSTC比赛里出现了各种各样的统计方法，包含健壮的人工规则集(A simple and generic belief tracking mechanism for the dialog state tracking challenge:),条件随机场(Recipe for building robust spoken dialog state trackers: Dialog state tracking challenge system description. Structured discriminative model for dialog state tracking.),最大熵模型(Multi-domain learning and generalization in dialog state tracking),网络风格的排序(Web-style ranking and slu combination for dialog state tracking)

最近，(Deep neural network approach for the dialog state tracking challenge)将深度学习引入了置信跟踪。它用一个滑动窗口来输出任意个数可能值的概率序列。尽管其只是在一个领域上训练额度，但是可以很容易的迁移到新的领域。(Multidomain dialog state tracking using recurrent neural
networks)开发了一个多领域RNN状态路径模型。它首先用了可以获得的所有数据来训练了一个非常通用的路径模型，然后又对通用模型针对每个领域进行调整以学习领域特有的行为。（ Neural belief tracker: Data-driven dialogue state tracking.）提出了一个神经置信路径方法来检测槽值对。其将系统的对话行为放在用户输入前，用户的语句本身还有一个备选的槽值对也就是需要基于此作出决定的作为输入，然后遍历所拥有的备选槽值对来确定到底哪个是用户刚表达的。

### 2.1.3 策略学习

在状态跟踪器的状态表示的条件下，策略学习的目标是生成下一个系统内可用的动作。监督学习或者强化学习都可以用来优化策略学习的(Strategic dialogue management via deep reinforcement learning.)。比较典型的做法是用一个基于规则的客体来启动系统(Building task-oriented dialogue systems for online shopping)。然后用基于规则生成的行为数据来进行监督学习。在在线购物场景，如果对话状态是“推荐”，那么然后“推荐”的动作就会触发，并且这时候系统就会从产品库中检索商品。如果状态是“对比”，那么系统就会对比目标的商品或品牌。对话策略可以进一步用强化学习来训练端到端的策略，来引导系统朝着最终效果的方向优化策略。(Strategic dialogue management via deep reinforcement learning)把强化学习应用在对话策略上并同时学习到了特征表示和对话策略，这个系统比几个基准的方法,基于随机，规则和监督学习的都要好。

### 2.1.4 自然语言生成

自然语言生成组件将一个抽象的对话行为转换成一个自然语言的语句表述。在文章(Evaluating evaluation methods for generation in the presence of variation.)中有注意到，一个好的生成方法依赖有几个因素：流畅度，可读性和变化。传统的自然语言生成方法典型的方案是进行句子的规划。其在语义符号和语言中间层表示之间建立映射关系，语言的中间层类似有树状结构或者模版结构，然后将中间层表示结构转换成最终的语言表示( Training a sentence planner for spoken dialogue using boosting. Trainable sentence planning for complex information presentation in spoken dialog systems)。
在这两个文章中( Stochastic language generation in dialogue using recurrent neural networks with
convolutional sentence reranking. Semantically conditioned lstm-based natural language generation for spoken dialogue systems)介绍了一个类似RNNLM的基于LSTM的NLG神经网络方法。对话行为类型和其槽位值对都转换成one-hot的控制向量并作为最终生成语句的额外输入以此来保证生成的是真实的意思。前者用一个前向RNN生成器和CNN排序器，以及一个后向RNN的重排器。所有的子模块都是基于需要的对话行为来联合优化生成语句的。为了解决在实现语句的时候槽位信息的忽略和重复问题，文章中用了一个额外的控制cell来门控对话行为.(Semantic refinement
gru-based neural language generation for spoken dialogue systems. )通过将LSTM的输入向量带着对话行为进行门控扩展了这种方法。其他人又通过多种修改将该方法应用到了多领域里面。 在这个文章中(Context-aware natural language generation for spoken dialogue systems.)采用了LSTM结构的编码和解码来将问题信息，语义槽值，对话行为类型信息结合在一起来生成正确的回答。其用注意力机制来关注基于当前解码器解码状态下的关键信息。将对话行为类型编码成向量，基于神经网络的模型能够对不同的行为类型输出不同的回答。(Sequence-to-sequence generation for spoken dialogue via deep syntax trees and strings)也提出了一种基于seq2seq的方法可以选了来产生自然语言字符串基于从输入对话行为尝试深度语法依赖树。其随后就被扩展成利用前置的用户语句和回复模型。其能够让模型根据用户的说话进行再训练，提供了有上下文信息的合适回复。

### 2.2 端到端的方法

在传统的任务型对话系统中除了很多难应用到新地方的领域特定的定制部分，有人进一步提出了传统的管道式任务型对话系统还有两个主要的缺陷。一个是结果分配问题，也就是说用户的最终反馈很难传播到上游组件。第二个问题是流程之间的依赖性。一个组件的输入依赖于另一个组件的输出。当将一个组件进行新环境适配或者用新数据训练后，都有的组件都需要进行适配以保证全局的最优。槽位和特征也需要相应的进行变动。这个过程需要大量的人力。随着近些年端到端生成式模型的进展，已经有很多尝试用端到端的方法来训练任务型对话系统。不同于传统管道，端到端的模型用一个组件和结构化的外部数据库进行交互。




## 实际应用-智能外呼系统

### 系统简介

智能外呼系统是借力于在近年迅猛发展深度学习技术结合具体的行业领域而构建的一套旨在提高人工电话效益的智能辅助系统。
目前的智能外呼系统行业又通称为智能外呼机器人，通常应用的领域有房地产，保险，贷款，
信用卡等之前都需要大量人工座席对客户进行回访，营销，催收等以实现对目标客户的转化引导。

### 传统电销

传统的人工座席因为外呼主体是人，因此其外呼效果主要有以下成本：

- 1 新人培训成本,时间和人力
- 2 因人而异的效果差异,经验可复制性不高
- 3 人员管理,工资,工作时间等

### 智能外呼

借力于深度学习技术的系统语音和文本处理能力，以及定制化开发的应答系统的智能外呼系统，主要是通过以下手段提高人工效率的：

- 1 基于话术的智能应答，业务专家经验的直接复用
- 2 基于统一深度学习模型的的应答过程，效果有保证
- 3 实时快速灵活的座席数扩张，按需设置

综上可以
