"""
code speace
@Time    : 2024/4/10 15:44
@Author  : 泪懿:dgl
@File    : encrypt.py
"""
import hashlib
import uuid

from django.conf import settings

def md5(string):
    hash_objects=hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_objects.update(string.encode('utf-8'))
    return hash_objects.hexdigest()

def uid(string):
    data="{}-{}".format(
        str(uuid.uuid4()),string
    )
    return md5(data)