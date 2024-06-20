"""
code speace
@Time    : 2024/4/10 9:34
@Author  : 泪懿:dgl
@File    : urls.py
"""
from django.urls import re_path,path
from book.views import base,booklist,manager
app_name='book'

urlpatterns=[
        path('',base.index,name='index'),
        re_path('^login/$',base.login,name='login'),
        re_path('logout/$',base.logout,name='logout'),
        re_path('^register/$',base.register,name='register'),
        re_path(r'^capth/$', base.captch, name='capth'),
        re_path(r'^persion/$', base.persion, name='persion'),
        re_path(r'^upload/$', base.upload, name='upload'),

        re_path(r'^book/$',booklist.book_index,name='book'),
        re_path(r'^book_list/$',booklist.book_list,name='book_list'),
        re_path(r'^book_detail/(?P<bookid>\d+)$',booklist.book_detail,name='book_detail'),
        re_path(r'^book_review/(?P<bookid>\d+)$',booklist.book_review,name='book_review'),

        re_path(r'^book_data/$',manager.book_data,name='book_data'),
        re_path(r'^deel_book/$',manager.deel_book,name='deel_book'),
        re_path(r'^deel_user/$',manager.deel_user,name='deel_user'),
        re_path(r'^update_form/$',manager.update_form,name='update_form'),

        re_path(r'^user_data/$',manager.user_data,name='user_data'),

        re_path(r'^manage/$',manager.manage,name='manage'),
        re_path(r'^manage/login/$',manager.manage_login,name='manage_login'),
        re_path(r'^manage/book$',manager.manage_book,name='manage_book'),
        re_path(r'^manage/user$',manager.manage_user,name='manage_user'),





]