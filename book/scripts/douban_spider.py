"""
code speace
@Time    : 2024/4/10 10:31
@Author  : 泪懿:dgl
@File    : douban_spider.py
"""
import requests
from lxml import html
import time
import random

class BookContent_spider:
    def __init__(self):
        self.headers={
    "GET": "/subject/36150423/ HTTP/1.1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": 'bid=x5VLq66PESY; _pk_id.100001.3ac3=f6815a94c16fb62e.1712672835.; __yadk_uid=QtDGSFIjXhjgzn3XWjzl5xzItAafCwQT; _ga=GA1.1.491807915.1712672848; _ga_RXNMP372GL=GS1.1.1712713439.2.0.1712713439.60.0.0; ct=y; viewed="35496106_2035162_36780601_36294882_36150423_36754770_36414410_26801676"; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1712729605%2C%22https%3A%2F%2Fwww.bing.com%2F%22%5D; _pk_ses.100001.3ac3=1; ap_v=0,6.0; dbcl2="262286464:L4CvVeTUAVM"; ck=ACcv; push_noty_num=0; push_doumail_num=0',
    "Host": "book.douban.com",
    "Referer": "https://book.douban.com/annual/2023/?fullscreen=1&source=navigation",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "sec-ch-ua": "\"Chromium\";v=\"124\", \"Microsoft Edge\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

    def get_data(self,url):
        resp=requests.get(url,headers=self.headers)
        errt=html.etree.HTML(resp.text)

        img_url=errt.xpath('//a[@class="nbg"]//img/@src')

        if img_url:
            img_url=img_url[0]
            img_content = self.down_img(img_url)
        else:
            img_content=''

        content = errt.xpath('//div[@id="link-report"]//div[@class="intro"]//p//text()')

        if '展开全部' in ''.join(content):
           content = errt.xpath('////div[@id="link-report"]//span[@class="all hidden"]//div[@class="intro"]//p//text()')

        if content:
            content='\n'.join(content)
        else:
            content=''
        time.sleep(random.uniform(0.01,0.05))

        return {'content':content,'img':img_content}


    def down_img(self,url):

        resp = requests.get(url)

        return resp.content

if __name__ == '__main__':
    spider=BookContent_spider()
    url='https://book.douban.com/subject/35496106/'
    spider.get_data(url)



