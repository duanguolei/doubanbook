"""
code speace
@Time    : 2024/4/10 10:33
@Author  : 泪懿:dgl
@File    : read_db_book.py
"""
import init
from book import models
import pymysql
from douban_spider import BookContent_spider
import pandas as pd
from book.uitls import encrypt
from book.uitls import utils
import os

import re
def main():
    connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='123456',
                             database='library_manage',
                             cursorclass=pymysql.cursors.DictCursor)

    try:

        with connection.cursor() as cursor:
            sql = "SELECT * FROM douban_books "
            cursor.execute(sql)

            result = cursor.fetchall()
    except Exception as e:
        print(e)

    # ['id', 'ISBN', 'book_name', 'book_author', 'tag_name', 'book_press',
    #  'book_year', 'book_pice', 'book_rating_num', 'book_url', 'is_review'],

    df = pd.DataFrame(result)

    try:

        with connection.cursor() as cursor:
            sql = "SELECT * FROM douban_books_content "
            cursor.execute(sql)

            result = cursor.fetchall()
    finally:

        connection.close()

    df2 = pd.DataFrame(result)

    spider=BookContent_spider()
    for index,row in df.iterrows():
        if index>3048:
            try:
                book=models.BookInfo()
                book.isbn=row['ISBN']

                book.name=row['book_name'].strip()
                book.autor=row['book_author']
                book.tagname=row['tag_name']

                pattern = r'\d+\.\d+'
                book_price=row['book_pice']
                if book_price:
                    match = re.search(pattern, book_price)
                    if match:
                        book_price = float(match.group())
                        book.price = book_price



                book.year=row['book_year']
                rate=row['book_rating_num']
                if rate:
                    book.rating=float(rate)

                book.publish=row['book_press']

                book_url=row['book_url']

                conten_dict=spider.get_data(book_url)
                content=conten_dict['content']
                img_content=conten_dict['img']
                if img_content:
                    img_name=encrypt.uid(row['book_name'])+'.jpg'

                    utils.save_image(img_content,img_name,'bookimage')
                    book.booklogo=os.path.join('bookimage', img_name)
                if content:
                    book.desc=content
                print(index,row['book_name'])
                book.save()

                # 将豆瓣的评论导入到 DoubanReview里面
                book_df = df2[df2['book_url'] == book_url]
                for i, col in book_df.iterrows():
                    review = models.DoubanReview()
                    review.name = col['user_name']
                    review.content = col['content_text']
                    review.book = book
                    review.create_date=col['content_time']
                    review.namelogo=col['user_avatar']
                    review.star=col['user_star']
                    review.save()
            except Exception as e:
                print(e)

if __name__ == '__main__':
    main()