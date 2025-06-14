from collections import Counter

from flask import Flask, render_template, request
from db_utils import DBUtils
import charts

app = Flask(__name__)
utils = DBUtils()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/movie_list')
def movie_list():
    movie_sum = utils.get_movie_sum()[0] if utils.get_movie_sum() else 0
    max_rating = utils.get_max_rating()[0] if utils.get_max_rating() else 0
    # 将内容放入至set集合中，目的是为了去重。
    type_count = len({word for tuple_item in utils.get_type_count() or [] for word in tuple_item[0].split(',')})
    max_year = utils.get_max_year()[0] if utils.get_max_year() else 0
    max_timing = utils.get_max_timing()[0] if utils.get_max_timing() else 0
    max_director = utils.get_max_director()[0] if utils.get_max_director() else ''
    movies = utils.get_movies() or []
    data = {
        'movie_sum': movie_sum,
        'max_rating': max_rating,
        'type_count': type_count,
        'max_year': max_year,
        'max_timing': max_timing,
        'max_director': max_director,
        'movies': movies
    }
    return render_template('movie_list.html', data=data)


@app.route('/movie_by_year')
def movie_by_year():
    return render_template('movie_by_year.html')


@app.route('/movie_by_year_chart')
def movie_by_year_chart():
    args = tuple(zip(*utils.get_count_by_year()))
    max_year_result = utils.get_max_year()
    if max_year_result is None:
        # 提供默认值或返回错误信息
        max_count = 0
    else:
        max_count = max_year_result[1]
    chart = charts.movie_year_chart(args, max_count)
    return chart


@app.route('/movie_type_percent')
def movie_type_percent():
    return render_template('movie_type_percent.html')


@app.route('/movie_type_percent_chart')
def movie_type_percent_chart():
    args = []
    types = utils.get_type_count()
    genre_count = Counter()
    for item in types:
        genre_count.update(item[0].split(','))
    for genre, count in genre_count.items():
        args.append((genre, count))
    
    # 检查 args 是否为空
    if not args:
        return "No data available for the chart", 400
    
    return charts.movie_type_chart(args)


@app.route('/name_and_rating')
def name_and_rating():
    return render_template('name_and_rating.html')


@app.route('/name_and_rating_chart')
def name_and_rating_chart():
    args = utils.get_name_and_rating()
    return charts.movie_rating_chart(args)


@app.route('/movie_top')
def movie_top():
    return render_template('movie_top.html')


@app.route('/movie_top_chart')
def movie_top_chart():
    args = utils.get_movie_top10()
    return charts.movie_top_chart(args)


@app.route('/rater_top')
def rater_top():
    return render_template('rater_top.html')


@app.route('/rater_top_chart')
def rater_top_chart():
    # 获取数据并检查是否为空
    raw_data = utils.get_rater_top20()
    if not raw_data:
        # 如果数据为空，返回一个默认图表或错误信息
        return "No data available for the chart", 400
    
    # 构造 args
    args = tuple(zip(*raw_data))
    if len(args) < 2:
        # 如果数据不足以构造 X 轴和 Y 轴，返回错误信息
        return "Insufficient data to generate the chart", 400
    
    return charts.movie_rater_count_chart(args)


@app.route('/word_cloud')
def word_cloud():
    return render_template('word_cloud.html')


@app.route('/word_cloud_chart')
def word_cloud_chart():
    args = utils.get_movie_name()
    return charts.movie_words_cloud(args)


@app.route('/search_movies', methods=['GET'])
def search_movies():
    # 从请求参数中获取搜索关键词
    query = request.args.get('query', '').strip()
    
    # 如果查询为空，则返回空结果或提示信息
    if not query:
        return render_template('search_results.html', movies=[], query=query)
    
    # 调用 DBUtils 进行搜索
    movies = utils.search_movies(query) or []
    
    # 将结果传递给模板
    return render_template('search_results.html', movies=movies, query=query)


@app.route('/favicon.ico')
def favicon():
    return '', 204  # 返回空响应，状态码为 204


if __name__ == '__main__':
    app.run()