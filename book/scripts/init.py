"""
code speace
@Time    : 2024/4/10 10:30
@Author  : 泪懿:dgl
@File    : init.py
"""
import django
import os

basr_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys

sys.path.append(basr_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','doubanbook.settings')
django.setup()

from book import models

if __name__ == '__main__':
    for index,value in models.BookType.TYPE_CHOICE:

        book_type=models.BookType(booktype=index)
        book_type.save()