import sqlite3
from pathlib import Path


class DBUtils:
    def __init__(self):
        self.connect = None
        self.db_path = Path(__file__).parent / 'douban_plat.db'

    def open_connect(self):
        try:
            self.connect = sqlite3.connect(self.db_path)
            self.connect.row_factory = sqlite3.Row  # 使查询结果可以按列名访问
        except Exception as ex:
            print('数据库连接异常', ex)

    def close_connect(self):
        if self.connect is not None:
            self.connect.close()

    def get_movie_sum(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT COUNT(*) FROM `movies`'
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_max_rating(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT MAX(`rating`) AS `max_rating` FROM `movies`'
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_type_count(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `movie_type` FROM `movies`'
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_max_year(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `release_year`, COUNT(*) AS `year_count` FROM `movies` GROUP BY `release_year` ORDER BY `year_count` DESC LIMIT 1'
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_max_timing(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT MAX(`timing`) FROM `movies`'
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_max_director(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `director`, COUNT(*) AS `director_count` FROM `movies` GROUP BY `director` ORDER BY `director_count` DESC LIMIT 1'
                cursor.execute(sql)
                return cursor.fetchone()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_movies(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT * FROM movies'
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_count_by_year(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `release_year`, COUNT(*) AS `year_count` FROM `movies` GROUP BY `release_year` ORDER BY `release_year` ASC'
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_name_and_rating(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `movie_name`, `rating` FROM `movies` ORDER BY RANDOM() LIMIT 20'
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_movie_top10(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `movie_name`, `id` FROM `movies` LIMIT 10'
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_rater_top20(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `movie_name`, `rater_count` FROM `movies` ORDER BY `rater_count` DESC LIMIT 20'
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def get_movie_name(self):
        self.open_connect()
        try:
            with self.connect:
                cursor = self.connect.cursor()
                sql = 'SELECT `movie_name`, 1 FROM `movies`'
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as ex:
            print('数据库操作异常', ex)
        finally:
            self.close_connect()

    def search_movies(self, query):
        from models import Movie  # 假设 Movie 是电影模型
        # 使用 SQLAlchemy 进行模糊查询
        return Movie.query.filter(Movie.name.like(f'%{query}%')).all()