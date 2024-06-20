"""
code speace
@Time    : 2024/4/10 11:11
@Author  : 泪懿:dgl
@File    : utils.py
"""
from django.conf import settings
import os

def get_review_word_dict():
    review_word_dict={}

    with open('book/scripts/评分分词.txt','r',encoding='utf-8')as f:
        word_counts=f.readlines()
        for word_count in word_counts:
            if word_count:
                # print(word_count)
                try:
                    word=word_count.split(',')[0].strip()
                    count=word_count.split(',')[1].strip()
                    review_word_dict[word]=int(count)
                except:
                    continue


    return review_word_dict




def save_image(byte_data,filename,folder):
    media_path = os.path.join(settings.MEDIA_ROOT, folder)
    os.makedirs(media_path, exist_ok=True)

    with open(os.path.join(media_path,filename), 'wb') as file:
        file.write(byte_data)

if __name__ == '__main__':
    print(get_review_word_dict())
