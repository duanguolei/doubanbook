"""
code speace
@Time    : 2024/4/11 16:11
@Author  : 泪懿:dgl
@File    : booklist.py
"""
import uuid
import re

from book.forms.base import RegisterModelFrom,LoginModelForm
from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from book import models
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q,Count
from book.uitls.captacher import get_img_code
import datetime
from book.uitls.pagination import Pagination

def book_index(request):

    search=request.GET.get('search')
    booktype=request.GET.get('booktype')
    book_type_choice=models.BookType.TYPE_CHOICE
    try:
        booktype=int(booktype)
    except:
        booktype=None

    if search:
        search=str(search)
        queryset = models.BookInfo.objects.filter(
            Q(publish__icontains=search) |
            Q(autor__icontains=search) |
            Q(isbn__icontains=search) |
            Q(name__icontains=search))

        if booktype:
            queryset = queryset.filter(booktype__booktype=booktype)
    else:
        queryset = models.BookInfo.objects.filter().order_by('-id')
        if booktype:
            queryset=queryset.filter(booktype__booktype=booktype)

    title=''
    if booktype:
        if booktype==1:
            title='热门图书'
            queryset=queryset.annotate(review_count=Count('doubanreview')).order_by('-review_count')

        if booktype==2:
            queryset = queryset.order_by('-create_datetime')
            title='新上图书'
        if booktype==3:
            queryset = queryset.order_by('-rating')
            title='高分图书'
    else:
        title='全部图书'
    page_object=Pagination(
        current_page=request.GET.get('page'),
        all_count=queryset.count(),
        base_url=request.path_info,
        per_page=32,
        query_params=request.GET,

    )


    col_num = 8
    books_item = []

    result =  queryset[page_object.start:page_object.end]



    if len(result)>1:
        for i in range(0, len(result) - 1, col_num):

            books_item.append(result[i:i + col_num])
    elif len(result)==1:
        books_item.append([result[0]])

    return render(request,'book_list.html',{'books_item': books_item, 'page_html': page_object.page_html(),'title':title })

@csrf_exempt
def book_list(request):
    books=models.BookInfo.objects.filter().values()[:100]

    return JsonResponse({'statsus':True,'data':list(books)})

def book_detail(request,bookid):
    book_obj=models.BookInfo.objects.filter(id=bookid).first()

    queryset = models.DoubanReview.objects.filter(
             book=book_obj
    ).order_by('-id')


    page_object = Pagination(
                current_page=request.GET.get('page'),
                all_count=queryset.count(),
                base_url=request.path_info,
                per_page=10,
                query_params=request.GET)

    result = queryset[page_object.start:page_object.end]


    review_star_list={}
    for item in result:

        star=item.star
        star_list = [1] *(star//10)
        if star % 10 >5:
            star_list.append(1)
        less_len = 5 - len(star_list)
        star_list.extend([0]*less_len)
        review_star_list[item.id]=star_list


    desc=book_obj.desc
    if desc:
        html_text = re.sub(r'\n', '</p><p>', desc)
        html_text = f'<p>{html_text}</p>'

        book_obj.desc=html_text
    else:
        book_obj.desc='<p>暂无介绍</p>'


    book_vating=book_obj.rating
    if book_vating:
        vating=int(book_vating * 10)

        star=int(round(vating/20,0))
        vatings_list=[1]*star
        if vating%20>10:
            vatings_list.append(1)


        less_len=5-len(vatings_list)
        vatings_list.extend([0]*less_len)

    else:
        vatings_list = [0]*5



    return render(request,'bookinfo.html',{'book':book_obj,
                                           'page_html': page_object.page_html(),
                                           'reviews':result,
                                           'vatings_list':vatings_list,
                                           'review_star_list':review_star_list})

import datetime
def book_review(request,bookid):
    star=request.GET.get('star')
    content=request.GET.get('content')
    book_obj = models.BookInfo.objects.filter(id=bookid).first()
    book_review=models.DoubanReview()
    book_review.book=book_obj
    book_review.name=request.manage.user.username
    book_review.namelogo=request.manage.user.avator.url
    book_review.content=content
    book_review.star = int(star) * 10
    now_date=datetime.datetime.now()

    book_review.create_date= now_date

    book_review.save()

    return JsonResponse({'status':True})

