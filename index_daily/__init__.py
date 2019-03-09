from pyecharts import Style, Geo, Pie

# style,init_style 会返回类初始化的风格

pie = Pie('各类电影中"好片"所占的比例', "数据来着豆瓣", title_pos='center',width=1600, height=600)
pie.add("", ["剧情", ""], [25, 75], center=[10, 30])
pie.add("", ["奇幻", ""], [24, 76], center=[30, 30])
pie.add("", ["爱情", ""], [14, 86], center=[50, 30])
pie.add("", ["惊悚", ""], [11, 89], center=[70, 30])

pie.render("test.html")