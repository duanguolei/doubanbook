"""
code speace
@Time    : 2024/4/13 11:50
@Author  : 泪懿:dgl
@File    : init_manage_user.py
"""

import init
from book.models import User
user=User(username='admin',password='123456')
user.save()

