"""
code speace
@Time    : 2024/4/19 9:44
@Author  : 泪懿:dgl
@File    : user.py
"""
from django.template import Library
from book import models
from django.urls import reverse

register=Library()

@register.inclusion_tag('inlutions/menu.html')
def load_mune_list(request):
    """
    设置菜单
    :param request:
    :return:
    """



    data_list = [
        {'title': '全部', 'url': f"{reverse('book:book')}"},
        {'title': '热门图书', 'url': f"{reverse('book:book')}?booktype=1"},
        {'title': '新上图书', 'url': f"{reverse('book:book')}?booktype=2"},
        {'title': '高分图书', 'url':f"{reverse('book:book')}?booktype=3"},
    ]

    return {'data_list':data_list}


@register.inclusion_tag('inlutions/menu.html')
def load_manage_mune_list(request):
    """
    设置菜单
    :param request:
    :return:
    """

    data_list = [
        {'title': '主页', 'url':reverse('book:manage')},
        {'title': '图书管理', 'url':reverse("book:manage_book")},
        {'title': '用户管理', 'url':reverse('book:manage_user')},

    ]




    return {'data_list':data_list}




@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)