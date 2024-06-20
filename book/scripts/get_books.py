#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : get_books.py
@Author: smallbike
@Date  : 2024/3/19 21:54 
@Desc  : 
'''
import random
import time

import requests
from lxml import etree
from urllib import parse
from pymysql import Connection

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


def get_tags():
    """
        获取豆瓣所有书籍标签
    :return:
    """
    url = "https://book.douban.com/tag/"
    params = {
        "view": "type",
        "icn": "index-sorttags-all"
    }
    response = requests.get(url, headers=headers, params=params, timeout=10,proxies=get_procy())
    print(response)
    if response:
        tree = etree.HTML(response.text)
        tag_list = tree.xpath('//div[@class="article"]//td/a//text()')
        print(len(tag_list))
        for tag_name in tag_list:
            print(f'---> 正在处理的标签为：{tag_name}')
            tag_page_list(tag_name)


def tag_page_list(tag_name):
    """
        标签页面获取书籍
    :param tag: 标签
    :return:
    """
    tag_name = parse.quote(tag_name)
    for i in range(1, 10):
        # for i in range(1, 2):
        start = (i - 1) * 20
        url = f"https://book.douban.com/tag/{tag_name}"
        params = {
            "start": start,
            "type": "T"
        }
        response = requests.get(url, headers=headers, params=params,proxies=get_procy(), timeout=10)
        if response:
            tree = etree.HTML(response.text)
            book_url_list = tree.xpath('//li[@class="subject-item"]//h2/a/@href')
            for book_url in book_url_list:
                try:
                    with open('is_search.txt', 'r', encoding='utf-8') as fp:
                        is_save = [i.strip() for i in fp.readlines()]
                except:
                    is_save = []
                if book_url in is_save:
                    # print(f' ---------> 已经存在跳过 <------------ ')
                    continue
                book_detail(book_url, tag_name)
                time.sleep(random.randint(1, 3))
                with open('is_search.txt', 'a', encoding='utf-8') as fp:
                    fp.write(book_url + '\n')


def book_detail(book_url, tag_name):
    """
        获取书本详情
    :param book_url:
    :return:
    """
    chen_db = Connection(
        host='127.0.0.1',
        database='library_manage',
        user='root',
        password='123456'
    )
    book_dict = {}
    response = requests.get(book_url, headers=headers,proxies=get_procy(), timeout=10)
    if response:
        tree = etree.HTML(response.text)
        # TODO 书名
        book_name = ''.join(tree.xpath('//h1//text()')).strip()
        # TODO 评分
        book_rating_num = ''.join(tree.xpath('//strong//text()')).strip()
        book_infos = [i for i in [i.strip() for i in tree.xpath('//div[@id="info"]//text()') if i.strip()] if i != ':']
        book_author = ''
        book_press = ''
        book_year = ''
        book_pice = ''
        ISBN = ''
        for index, text in enumerate(book_infos):
            try:
                target_value = book_infos[index + 1]
            except:
                target_value = ''
            if '作者' in text:
                book_author = target_value
            elif '出版社:' in text:
                book_press = target_value
            elif '出版年' in text:
                book_year = target_value
            elif '定价' in text:
                book_pice = target_value
            elif 'ISBN' in text:
                ISBN = target_value

        book_dict['book_name'] = book_name
        book_dict['book_author'] = book_author
        book_dict['tag_name'] = parse.unquote(tag_name)
        book_dict['book_press'] = book_press
        book_dict['book_year'] = book_year
        book_dict['book_pice'] = book_pice
        book_dict['book_rating_num'] = book_rating_num
        book_dict['ISBN'] = ISBN
        book_dict['book_url'] = book_url

        print(f' 当前书籍的基本信息 ====> {book_dict}')
        resp = chen_db.table_insert('douban_books', book_dict)
        print(f' 保存成功 【{resp}】------> {book_name}')


if __name__ == '__main__':
    while True:
        # TODO 这个是代理池
        try:
            get_tags()
        except:
            import traceback

            print(f'报错---》{traceback.print_exc()}')
