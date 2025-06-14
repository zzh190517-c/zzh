import re
from collections import Counter

import jieba
import stylecloud
from wordcloud import WordCloud
from db_utils import DBUtils

utils = DBUtils()


def loading_data():
    data = {}
    movies = utils.get_movies()
    movie_names = []
    director_names = []
    dates = []
    types = []
    for movie in movies:
        movie_names.append(movie[1])
        director_names.append(movie[5])
        dates.append(movie[2])
        types.append(movie[6])
    data['movie_names'] = movie_names
    data['director_names'] = director_names
    data['dates'] = dates
    data['types'] = types
    return data


def to_word_cloud(source_words, target_path, is_chinese=False, is_jieba=False, max_font_size=120, min_font_size=30):
    words = []
    if is_chinese:
        chinese_words = []
        for item in source_words:
            chinese_chars = re.findall('[\u4e00-\u9fff]+', str(item))
            new_item = "".join(chinese_chars)
            chinese_words.append(new_item)
        for item in chinese_words:
            parts = item.split(" ")
            words.extend(parts)
    else:
        for item in source_words:
            parts = str(item).split(" ")
            words.extend(parts)
    if is_jieba:
        new_str = "".join([element.upper() for element in words])
        words = jieba.lcut(new_str, cut_all=False)

    word_counts = Counter(words)
    word_freq_dict = dict(word_counts)
    wc = WordCloud(
        font_path='static/fonts/main.ttf',
        background_color='white',  # 设置背景颜色为白色
        width=800,  # 设置词云图宽度
        height=600,  # 设置词云图高度
        max_words=200,  # 最多显示的词语数量
        min_font_size=min_font_size,  # 最小字体大小
        max_font_size=max_font_size  # 最大字体大小
    ).generate_from_frequencies(word_freq_dict)
    wc.to_file(target_path)


def main():
    data = loading_data()
    to_word_cloud(data['movie_names'], 'static/images/movie_names.png', is_chinese=True)
    to_word_cloud(data['director_names'], 'static/images/director_names.png', is_chinese=True)
    to_word_cloud(data['dates'], 'static/images/dates.png')
    to_word_cloud(data['types'], 'static/images/types.png', is_chinese=True, is_jieba=True, max_font_size=180, min_font_size=60)


if __name__ == '__main__':
    main()
