"""
code speace
@Time    : 2024/5/30 20:19
@Author  : 泪懿:dgl
@File    : douban_reviw_spider.py
"""
import json
import random
import time

import init
import pandas as pd
import pymysql
import requests
from lxml import html
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,fil;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

def get_procy():
    tunnel = "o474.kdltps.com:15818"
    username = ""
    password = ""
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    return proxies


def get_db_df():
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
    return df


def get_reviews(bookname,book_url=None):

    subject=book_url.split("subject/")[-1].split('/')[0]
    print(bookname,subject)

    url=f'https://book.douban.com/subject/{subject}/comments/'
    pages=5#页数5
    for p in range(pages+1):
        try:
            params={
            "percent_type": "",
            "start": str(p*20),
            "limit": "20",
            "status": "P",
            "sort": "score",
            "comments_only": "1",
            "ck": "6g3K"
        }
            resp=requests.get(url,params=params,headers=headers,proxies=get_procy())
            # print(resp.text)
            data=json.loads(resp.text)
            text=data['html']
            errt=html.etree.HTML(text)
            lis=errt.xpath('//li[@class="comment-item"]')
            for li in lis:
                img=li.xpath(".//img/@src")[0]
                title=li.xpath('.//span[@class="comment-info"]/a/text()')[0]
                short=li.xpath('.//span[@class="short"]/text()')[0]
                comment_time=li.xpath('.//a[@class="comment-time"]/text()')[0]
                start=li.xpath('.//span[@class="comment-info"]/span[1]/@class')[0].split()[1].split("tar")[-1]
                data={
                    'name':title,
                    'create_date':comment_time,
                    'star':start,
                    'content':short,
                    'namelogo':img
                }
                print(data)

            time.sleep(random.random())
        except:
            continue


def main():
    df=get_db_df()
    for index,row in df.iterrows():
        book_url=row['book_url']
        bookname=row['book_name']
        get_reviews(bookname,book_url)


if __name__ == '__main__':
    main()