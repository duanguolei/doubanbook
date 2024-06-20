"""
code speace
@Time    : 2024/4/11 22:19
@Author  : 泪懿:dgl
@File    : auth.py
"""
class Manage(object):
    def __init__(self):
        self.user=None
        #存储当前用户
        self.level=None


from django.utils.deprecation import MiddlewareMixin
from book import models
from book.models import User
from django.shortcuts import redirect,reverse
from django.http import HttpResponseRedirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self,request):
        """
        保存每次处理请求之前的用户验证信息
        :param request:
        :return:
        """
        manage=Manage()
        userid=request.session.get('user_id',)
        level=request.session.get('level')

        manage.idnumber=userid
        if level:
            user_obj=User.objects.filter(id=userid).first()
            manage.level=1
        else:
            user_obj = models.Userinfo.objects.filter(id=userid).first()

        if user_obj:
            manage.user = user_obj

        request.manage=manage






