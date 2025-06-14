import sqlite3
import requests
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from pathlib import Path

# 定义多个 User-Agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

# 随机选择一个 User-Agent
headers = {
    'User-Agent': random.choice(user_agents),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive'
}

# 豆瓣电影Top250的URL基础部分
base_url = "https://movie.douban.com/top250"
# 存储电影详情链接
movie_links = []
# 用于存储爬取到的电影信息的列表
movie_list = []

# 创建带重试机制的会话
def create_session():
    session = requests.Session()
    retries = Retry(
        total=5,  # 总重试次数
        backoff_factor=1,  # 重试间隔时间
        status_forcelist=[429, 500, 502, 503, 504]  # 需要重试的状态码
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


# 发送HTTP GET请求，获取网页内容
def get_page(url):
    session = create_session()  # 使用带重试机制的会话
    try:
        response = session.get(url, headers=headers, timeout=10)  # 设置超时时间为10秒
        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败，状态码：{response.status_code}, URL: {url}")
            return None
    except Exception as e:
        print(f"请求异常：{e}, URL: {url}")
        return None


# 解析HTML内容，提取电影信息
def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 查找所有电影条目
    movies = soup.find_all('div', class_='item')
    for movie in movies:
        movie_links.append(movie.select_one('.hd>a').get('href'))


def parse_movie(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # 检查是否存在电影名称
    movie_name_tag = soup.select_one('h1>span')
    if not movie_name_tag:
        print("无法找到电影名称")
        return
    
    movie_name = movie_name_tag.text.strip()
    
    # 提取其他信息
    release_year = soup.select_one('h1>span.year')
    release_year = release_year.text[1:-1] if release_year else "未知"
    
    rating = soup.select_one('.rating_self>strong')
    rating = rating.text.strip() if rating else "未知"
    
    rater_count = soup.select_one('.rating_sum>a>span')
    rater_count = rater_count.text.strip() if rater_count else "未知"
    
    director = soup.select_one('#info>span:nth-of-type(1)>span.attrs>a')
    director = director.text.strip() if director else "未知"
    
    genre_spans = soup.find_all('span', property='v:genre')
    movie_type = ','.join([genre.text.strip() for genre in genre_spans]) if genre_spans else "未知"
    
    timing = soup.find('span', property='v:runtime')
    timing = timing.get('content') if timing else "未知"
    
    # 将电影信息添加到列表
    movie_list.append([movie_name, release_year, rating, rater_count, director, movie_type, timing])


# 主函数，程序入口
def main():
    # 每页25部电影，共10页
    for start in range(0, 250, 25):
        # 构造带有start参数的URL
        url = f"{base_url}?start={start}"
        print(f"正在抓取第 {start // 25 + 1} 页: {url}")  # 打印进度
        # 获取网页内容
        html = get_page(url)
        if not html:
            print(f"跳过 URL: {url}")
            continue
        # 解析网页内容
        parse_page(html)
        time.sleep(random.uniform(1, 3))  # 增加随机延迟，避免触发反爬虫机制
    
    # 通过获取到的链接，完成数据抓取
    for i, link in enumerate(movie_links):
        print(f"正在抓取第 {i + 1} 个电影详情页: {link}")  # 打印进度
        html = get_page(link)
        if not html:
            print(f"跳过详情页: {link}")
            continue
        parse_movie(html)
        time.sleep(random.uniform(1, 3))  # 增加随机延迟，避免触发反爬虫机制


# 主函数，程序入口
def write_to_sqlite():
    db_path = Path(__file__).parent / 'douban_plat.db'
    connect = None
    try:
        connect = sqlite3.connect(db_path)
        cursor = connect.cursor()

        # 创建表
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS movies
                       (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           movie_name TEXT,
                           release_year TEXT,
                           rating REAL,
                           rater_count TEXT,
                           director TEXT,
                           movie_type TEXT,
                           timing TEXT
                       )
                       ''')

        # 批量插入
        sql = ('INSERT INTO movies (movie_name, release_year, rating, rater_count, director, movie_type, timing)'
               ' VALUES (?, ?, ?, ?, ?, ?, ?)')
        cursor.executemany(sql, movie_list)
        connect.commit()
    except Exception as e:
        print(e)
        if connect:
            connect.rollback()
    finally:
        if connect:
            connect.close()


if __name__ == "__main__":
    main()  # 执行爬取操作
    write_to_sqlite()