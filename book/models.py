from django.db import models

# Create your models here.
from datetime import datetime
class Userinfo(models.Model):
    username=models.CharField(verbose_name='用户姓名',max_length=32,null=True)
    mobile_phone = models.CharField(verbose_name='手机号', max_length=32, )
    password = models.CharField(verbose_name='密码', max_length=32)
    email=models.EmailField(verbose_name='邮箱',max_length=32,null=True,blank=True)
    avator=models.ImageField(verbose_name='用户头像',upload_to='avatars/',null=True)

class User(models.Model):
    username = models.CharField(verbose_name='用户姓名', max_length=32, null=True)
    password = models.CharField(verbose_name='密码', max_length=32)


class BookInfo(models.Model):
    name = models.CharField(verbose_name='图书名', max_length=1255,null=True,blank=True)

    publish=models.CharField(verbose_name='出版社',max_length=64,null=True)
    autor=models.CharField(verbose_name='作者',max_length=64,null=True)
    isbn=models.CharField(verbose_name='ISBN',max_length=32,null=True,unique=True)
    tagname=models.CharField(verbose_name='标签',max_length=32,null=True)
    year=models.CharField(verbose_name='出版日期',max_length=32,null=True)
    create_datetime=models.DateField(null=True)
    price=models.DecimalField(verbose_name='价格',max_digits=10,decimal_places=1,null=True)
    rating=models.DecimalField(verbose_name='评分',max_digits=10,decimal_places=2,null=True,help_text='0-10')
    booklogo=models.ImageField(verbose_name='图片封面',upload_to='bookimage/',null=True)
    desc=models.TextField(verbose_name='介绍',null=True,help_text='换行以杠n结束')

    booktype = models.ManyToManyField(to='BookType')

class BookType(models.Model):
    TYPE_CHOICE=(
        (1,"热门图书"),
        (2,"新上书籍"),
        (3,"高分书籍")
    )
    booktype=models.IntegerField(verbose_name='书籍类型',choices=TYPE_CHOICE)





class DoubanReview(models.Model):
    content = models.TextField(verbose_name='评论', null=True)
    name = models.CharField(verbose_name='评论人',max_length=1255,null=True, blank=True, )
    namelogo = models.CharField(verbose_name='评论人头像',max_length=520,null=True, blank=True, )
    star = models.IntegerField(verbose_name='评分',  null=True)
    create_date = models.DateTimeField(verbose_name='创建时间',null=True)
    book = models.ForeignKey(verbose_name='评论图书', to='BookInfo',null=True, on_delete=models.CASCADE)
