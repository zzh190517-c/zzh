from pyecharts.charts import Bar, Pie, Scatter, Funnel, WordCloud
from pyecharts import options as opts


def movie_year_chart(args, max_count):
    chart = Bar()
    chart.add_xaxis(args[0])
    chart.add_yaxis('电影数目', args[1])
    chart.set_global_opts(
        legend_opts=opts.LegendOpts(
            is_show=False
        ),
        visualmap_opts=opts.VisualMapOpts(
            is_show=True,
            max_=max_count
        )
    )
    return chart.dump_options_with_quotes()


def movie_type_chart(args):
    # 检查 args 是否为空
    if not args:
        # 返回一个默认的空饼图
        chart = Pie()
        chart.add(
            series_name="电影类型",
            data_pair=[("无数据", 1)],
            radius=["40%", "75%"],  # 饼图的内外半径
        )
        chart.set_global_opts(
            legend_opts=opts.LegendOpts(
                pos_right='5%',
                pos_top='middle',
                orient='vertical'
            )
        )
        chart.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        return chart.dump_options_with_quotes()
    
    # 正常处理非空数据
    chart = Pie()
    chart.add(
        series_name="电影类型",
        data_pair=args,
        radius=["40%", "75%"],  # 饼图的内外半径
    )
    chart.set_global_opts(
        legend_opts=opts.LegendOpts(
            pos_right='5%',
            pos_top='middle',
            orient='vertical'
        )
    )
    chart.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    return chart.dump_options_with_quotes()


def movie_rating_chart(args):
    chart = Scatter()
    x_data = [item[0] for item in args]  # 电影名称
    y_data = [item[1] for item in args]  # 评分
    chart.add_xaxis(x_data)
    chart.add_yaxis(
        series_name="电影评分",
        y_axis=y_data,
        symbol_size=20  # 设置散点的大小
    )

    chart.set_global_opts(
        legend_opts=opts.LegendOpts(
            is_show=False
        ),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),  # 旋转x轴标签，避免重叠
        yaxis_opts=opts.AxisOpts(min_=8, max_=10),  # 设置y轴范围
    )
    return chart.dump_options_with_quotes()


def movie_top_chart(args):
    chart = Funnel()
    chart.add(
        series_name="电影TOP10",
        data_pair=args,
        gap=2,
        label_opts=opts.LabelOpts(is_show=True, position="inside"),
        min_=10,
        max_=1,
        min_size='40%',
        max_size='80%',
        tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
    )
    chart.set_global_opts(
        legend_opts=opts.LegendOpts(
            is_show=False
        )
    )
    return chart.dump_options_with_quotes()


def movie_rater_count_chart(args):
    chart = Bar()
    chart.add_xaxis(args[0])
    chart.add_yaxis('评分人数', args[1])
    chart.set_global_opts(
        legend_opts=opts.LegendOpts(
            is_show=False
        )
    )
    # 翻转x轴的方法
    chart.reversal_axis()
    return chart.dump_options_with_quotes()


def movie_words_cloud(args):
    chart = WordCloud()
    chart.add(series_name="电影名称", data_pair=args)
    chart.set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True)
    )
    return chart.dump_options_with_quotes()