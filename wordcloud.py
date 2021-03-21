#-*- coding = utf-8 -*-
# @Time    : 2021/3/21 12:42
# @Author  : circle
# @File    : wordcloud.py
# @Software: PyCharm
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3


conn = sqlite3.connect('../movie.db')
cur = conn.cursor()
sql = 'select instroduction from movie250'
content = cur.execute(sql)
print('打开数据库')
text = ''
for item in content:
    text = text + item[0]
cur.close()
conn.close()
#分词
cut = jieba.cut(text)
temp = ' '.join(cut)
print('cut value', temp)
img = Image.open('tree.jpg')
#将图片转化为数组
img_array = np.array(img)
#设置
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path='msyh.ttc',
).generate_from_text(temp)
#绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
# plt.show() 显示图片
plt.savefig('wordcloud.jpg')