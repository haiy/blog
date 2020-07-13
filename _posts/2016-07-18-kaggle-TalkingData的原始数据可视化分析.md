---
title: Kaggle Talkingdata的原始数据可视化分析
date: 2016-07-18 00:00:00 Z
layout: post
---

{{page.title}}
========

<p class="meta">July 18 2016</p>

kaggle上的talking data数据分析要想好好玩呢，开发环境越舒服越好啦。我这采用的环境是
mysql+sublimt+tmux+sql_terminal+ipython+matplotlib。简单说下这么选型的原因:

 - 1 mysql存储，数据量不是很大查询高效，数据初步探索分析很方便
 - 2 sublime + tmux, sublime的多点选择非常有用，这点比vim好用；tmux界面切换方便 
 - 3 ipython + matplotlib, 直接读入mysql数据，和matplotlib无缝衔接
 

**1 基本安装**

```bash
sudo apt-get install ipython python-mysqldb tmux python-matplotlib
```

**2 数据分析**

 - 2.1 训练集样本中男女分布

```python
import MySQLdb
import matplotlib.pyplot as plt
import numpy as np
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

db = MySQLdb.connect(user='root', passwd='root')
cur = db.cursor()
cur.execute("select use_group, count(*) from kaggle.gender_age_train group by gender")
res = cur.fetchall()
labels = res[0][0], res[2][0]
size = res[0][1], res[2][1]
explode = (0.1,0)
plt.pie(size,labels)
plt.pie(size, explode=explode, labels=labels,autopct='%1.1f%%')
plt.axis('equal')
plt.show()
```
<img src="{{site.url}}/images/kaggle/talking_data/figure_1.png"  height="300px" width="400px">

- 2.1 男女年龄分级分布对比

```python
cur.execute("select use_group as user_group,count(*) from kaggle.gender_age_train group by use_group")
age_dist = cur.fetchall()
N = 6
ind = np.arange(N)
men = [f[1] for f in age_dist if str(f).startswith('F')]
women = [f[1] for f in age_dist if f[0].startswith('M')]
fig, ax = plt.subplots()
rects1 = ax.bar(ind, men, width, color = 'r')
rects2 = ax.bar(ind+width, women, width, color = 'y')
ax.set_ylabel('count')
ax.set_title('Men and women age level count')
ax.set_xticks(ind+width)
ax.set_xticklabels(('L1', 'L2', 'L3', 'L4', 'L5', 'L6'))
ax.legend((rects1[0], rects2[0]), ('Men', 'Women'))
plt.show()
```

<img src="{{site.url}}/images/kaggle/talking_data/figure_2.png"  height="300px" width="400px">

- 2.2 数据长什么样子

```sql
mysql> select * from events limit 10;
+----------+----------------------+---------------------+-----------+----------+
| event_id | device_id            | timestamp           | longitude | latitude |
+----------+----------------------+---------------------+-----------+----------+
|        0 | device_id            | timestamp           | longitude | latitude |
|        1 | 29182687948017175    | 2016-05-01 00:55:25 | 121.38    | 31.24    |
|        2 | -6401643145415154744 | 2016-05-01 00:54:12 | 103.65    | 30.97    |
|        3 | -4833982096941402721 | 2016-05-01 00:08:05 | 106.60    | 29.70    |
|        4 | -6815121365017318426 | 2016-05-01 00:06:40 | 104.27    | 23.28    |
|        5 | -5373797595892518570 | 2016-05-01 00:07:18 | 115.88    | 28.66    |
|        6 | 1476664663289716375  | 2016-05-01 00:27:21 | 0.00      | 0.00     |
|        7 | 5990807147117726237  | 2016-05-01 00:15:13 | 113.73    | 23.00    |
|        8 | 1782450055857303792  | 2016-05-01 00:15:35 | 113.94    | 34.70    |
|        9 | -2073340001552902943 | 2016-05-01 00:15:33 | 0.00      | 0.00     |
+----------+----------------------+---------------------+-----------+----------+

mysql> select count(*) from events;
+----------+
| count(*) |
+----------+
|  3252951 |
+----------+

mysql> select count(distinct event_id) from events;
+--------------------------+
| count(distinct event_id) |
+--------------------------+
|                  3252951 |
+--------------------------+

mysql> select * from app_events limit 10;                                          
+----------+----------------------+--------------+-----------+
| event_id | app_id               | is_installed | is_active |
+----------+----------------------+--------------+-----------+
|        0 | app_id               |            0 |         0 |
|        2 | 5927333115845830913  |            1 |         1 |
|        2 | -5720078949152207372 |            1 |         0 |
|        2 | -1633887856876571208 |            1 |         0 |
|        2 | -653184325010919369  |            1 |         1 |
|        2 | 8693964245073640147  |            1 |         1 |
|        2 | 4775896950989639373  |            1 |         1 |
|        2 | -8022267440849930066 |            1 |         0 |
|        2 | 9112463267739110219  |            1 |         0 |
|        2 | -3725672010020973973 |            1 |         0 |
+----------+----------------------+--------------+-----------+

mysql> select count(*) from app_events;                                                   
| count(*) |
+----------+
| 32473068 |
+----------+

mysql> select count(distinct event_id) from app_events;
+--------------------------+
| count(distinct event_id) |
+--------------------------+
|                  1488097 |
+--------------------------+
```
 



### 参考:

- [MySQLdb doc](http://mysql-python.sourceforge.net/MySQLdb.html)     
- [Simple python mysql example](http://stackoverflow.com/questions/372885/how-do-i-connect-to-a-mysql-database-in-python)      
- [matplotlib](http://matplotlib.org/)   
- [pie_demo_features](http://matplotlib.org/examples/pie_and_polar_charts/pie_demo_features.html)   
- [barchart_demo](http://matplotlib.org/examples/api/barchart_demo.html)    
