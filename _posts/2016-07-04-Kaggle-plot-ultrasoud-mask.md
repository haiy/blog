---
title: Kaggle Plot Ultrasoud Mask
date: 2016-07-04 00:00:00 Z
layout: post
---

{{ page.title }}
================
<p class="meta">04 July 2015 </p>
将kaggle上的[超声波识别比赛](https://www.kaggle.com/c/ultrasound-nerve-segmentation)的神经组织mask
合并到原始的超声波图片上。
原始的图片如下：

<img src="images/1_1.png"  height="200px" width="200px">

轮廓mask:

<img src="images/1_1_mask.png"  height="200px" width="200px">



将上面两个图合并到一张图上去的代码如下：

```python
import matplotlib.pyplot as plt
import cv2
import numpy as np  
img = plt.imread("1_1.tif")
mask = plt.imread("1_1_mask.tif")
img_color = np.dstack([img, img, img])
mask_pix = cv2.Canny(mask,200,100) > 0
img_color[mask_pix, 0] = 255
img_color[mask_pix, 1] = 255
img_color[mask_pix, 2] = 255
plt.imshow(img_color)
plt.show()
```
合并后的结果如下：

<img src="images/1_1_mask_combined.png"  height="300px" width="300px">


tips: tif文件灰度存为png灰度 

```python
import Image
Image.open('1_1.tif').convert('LA').save('1_1.png')
```

参考：[kaggle script](https://www.kaggle.com/chefele/ultrasound-nerve-segmentation/plot-images-overlaid-with-mask/comments)




