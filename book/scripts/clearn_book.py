"""
code speace
@Time    : 2024/4/11 18:47
@Author  : 泪懿:dgl
@File    : clearn_book.py
"""
import init

from book.models import BookInfo

def delete_books_without_cover():
    #删除没有封面的数据
    books = BookInfo.objects.all()
    for book in books:
        if not book.booklogo:
            book.delete()

from datetime import datetime

def normalize_year(year_str):
    if not year_str:
        return None

    if '年' in year_str:
        try:
            date_obj = datetime.strptime(year_str, '%Y年%m月%d日')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            try:
                date_obj = datetime.strptime(year_str, '%Y年%m月')
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                try:
                    date_obj = datetime.strptime(year_str, '%Y年')
                    return date_obj.strftime('%Y-%m-%d')
                except:
                    return None
    elif '-' in year_str:
        try:
            date_obj = datetime.strptime(year_str, '%Y-%m-%d')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            try:
                date_obj = datetime.strptime(year_str, '%Y-%m')
                return date_obj.strftime('%Y-%m-%d')
            except:
                return None
    else:
        try:
            date_obj = datetime.strptime(year_str, '%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            return None

def deel_book_create_date():
    books = BookInfo.objects.all()
    for book in books:
        deel_date=normalize_year(year_str=book.year)
        book.create_datetime=deel_date
        book.save()

if __name__ == '__main__':
    delete_books_without_cover()
    deel_book_create_date()
