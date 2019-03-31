#coding=utf-8
from wxpy import *
from pyecharts import Pie

bot = Bot(cache_path = True)   #定义一个微信机器人
friends = bot.friends(update=False)   #获取更新好友列表
male = female = other = 0

for i in friends[1:]:     #[1:]是因为整个好友列表里面自己市在第一个，排除掉
    sex = i.sex
    if sex == 1:
        male += 1
    elif sex == 2:
        female += 1
    else:
        other += 1
total = len(friends[1:])   #计算总数

#下面为分析
attr = ["男性","女性","其他"]
v1 = [float(male),float(female),float(other)]
pie = Pie("饼图-圆环图示例", title_pos='center')
pie.add("", attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True,
        legend_orient='vertical', legend_pos='left')
pie.render("./res/sex.html")