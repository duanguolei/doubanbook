"""
code speace
@Time    : 2024/4/12 20:32
@Author  : 泪懿:dgl
@File    : spark_init_class.py
"""
import init
from book import models
from django.db.models import Count

from pyspark.sql import SparkSession
from pyspark.sql.functions import when


def classification_book():

    new_year=2024
    review_count=200#评论大于这个为热门图书
    rating=9#分数高于这个为高分读书

    spark = SparkSession.builder \
        .appName("BookAnalysis") \
        .getOrCreate()


    books_with_review_count =models.BookInfo.objects.annotate(review_count=Count('doubanreview'))

    def get_create_year(book):
        return book.create_datetime.year if book.create_datetime else None

    book_data = [(book.id, get_create_year(book), book.review_count, float(book.rating) if book.rating else None) for
                 book in books_with_review_count]
    book_df = spark.createDataFrame(book_data, ['book_id', 'create_year', 'review_count', 'rating'])


    book_df = book_df.withColumn('new_date_flag', when(book_df.create_year >= new_year, 1).otherwise(0)) \
        .withColumn('hote_flag', when(book_df.review_count > review_count, 1).otherwise(0)) \
        .withColumn('high_flag', when(book_df.rating > rating, 1).otherwise(0))


    result_df = book_df.select('book_id', 'new_date_flag', 'hote_flag', 'high_flag').toPandas()

    hote_type_object=models.BookType.objects.filter(booktype=1).first()
    new_type_object=models.BookType.objects.filter(booktype=2).first()
    high_type_object=models.BookType.objects.filter(booktype=3).first()


    result_list = result_df.to_dict(orient='records')
    for item in result_list:
        new_date_flag=item['new_date_flag']
        hote_flag=item['hote_flag']
        high_flag=item['high_flag']
        id=item['book_id']
        book=models.BookInfo.objects.filter(id=id).first()
        if new_date_flag:
            if  new_type_object not in book.booktype.all():
                book.booktype.add(new_type_object)

        else:
            if new_type_object in book.booktype.all():
                book.booktype.remove(new_type_object)

        if high_flag:
            if high_type_object not in book.booktype.all():
                book.booktype.add(high_type_object)
        else:
            if high_type_object in book.booktype.all():
                book.booktype.remove(high_type_object)

        if hote_flag:
            if hote_type_object not in book.booktype.all():
                book.booktype.add(hote_type_object)
        else:
            if hote_type_object in book.booktype.all():
                book.booktype.remove(hote_type_object)

        book.save()
    print('新上图书数量', len(result_df[result_df['new_date_flag'] == 1]))
    print('热门图书数量', len(result_df[result_df['hote_flag'] == 1]))
    print('高分图书数量', len(result_df[result_df['high_flag'] == 1]))
    spark.stop()




if __name__ == '__main__':
    classification_book()


