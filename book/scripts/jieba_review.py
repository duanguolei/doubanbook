"""
code speace
@Time    : 2024/4/25 13:56
@Author  : 泪懿:dgl
@File    : jieba_review.py
"""
import init
from book import models
from book.uitls import utils
import jieba
from collections import Counter

def jieba_word_counter(valuelist):
    with open('cn_stopwords.txt','r',encoding='utf-8')as f:
        #停用词
        stop_words=[i.strip() for i in f.readlines() if i]

    total_wrds = []
    for value in valuelist:
        if value:
            value = value[0]
            words = jieba.lcut(value)
            # print(value)
            for word in words:
                if word not in stop_words:
                    total_wrds.append(word)

    counter = Counter(total_wrds)

    return counter

if __name__ == '__main__':
    reviews = models.DoubanReview.objects.values_list('content')
    counter=jieba_word_counter(reviews)
    with open('评分分词.txt','w',encoding='utf-8')as f:
        for key,value in counter.items():
            f.write(key)
            f.write(',')
            f.write(str(value))
            f.write('\n')


