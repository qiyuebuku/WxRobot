#coding=utf-8
from wxpy import *
import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL.Image as Image

bot = Bot(cache_path = True)
friends = bot.friends(update=False)
male = female = other = 0

#提取好友签名，并去掉span，class，emoji，emoji1f3c3等的字段
signatures = []
for i in friends:
    signature = i.signature.strip().replace("span", "").replace("class", "").replace("emoji", "")
# 正则匹配过滤掉emoji表情，例如emoji1f3c3等
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    signatures.append(signature)
# 拼接字符串
text = "".join(signatures)
# jieba分词
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)

# wordcloud词云
my_wordcloud = WordCloud(background_color="white",
                         max_words=2000,
                         max_font_size=1000,
                         random_state=42,
                         font_path='./hanyi.ttf').generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()