import requests as rq
from bs4 import BeautifulSoup
import re
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from nltk import FreqDist
import pandas as pd
import numba
import ray
from functools import lru_cache
import os

@lru_cache()
def find_main_page_stock_news(url: str) -> str:
    news = rq.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(news.text, 'lxml')
    soup = soup.body.extract()

    for i in soup.select('ul.main li a'):
        if i.string == '주식 시장 뉴스':
            stock_url = i['href']
    return stock_url

@lru_cache()
def stock_news_list(url: str,page=None) -> list:
    news = rq.get(url + '/news/stock-market-news/', headers={'User-Agent': 'Mozilla/5.0'})
    if page is not None and news.status_code==200:
        all_title=['/'.join([url,'news/stock-market-news',str(i)]) for i in range(1,page+1,1)]
        return all_title
    else:
        all_title=url + find_main_page_stock_news(url)
        if rq.status_codes==404:
            soup = BeautifulSoup(news.text, 'lxml')
            soup = soup.body.extract()
            for i in soup.select('div.midDiv.inlineblock a'):
                if 'void' not in i['href']:
                    url = 'https://kr.investing.com/' + i['href']
                    all_title=np.append(all_title,url)
            return all_title

@ray.remote
def page_title_add(url:str)->list:
    news = rq.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(news.text, 'lxml')
    soup = soup.body.extract()
    title = []
    for i in soup.select("section#leftColumn div.largeTitle a"):
        if i.string != None and '키움' not in i.string and '시황체크' not in i.string:
            title.append(re.sub("[^a-zA-Z가-힣 ]", ' ', i.string.strip()))
            #print(re.sub("[^a-zA-Z가-힣 ]", ' ', i.string.strip()))
    title=np.array(title)
    return title


if __name__ == '__main__':
    
    ray.init(log_to_driver = False)

    url = 'https://kr.investing.com/'
    
    news_url_list=stock_news_list(url,100)
    chk=1
    while chk:
        future_to_url = [page_title_add.remote(url) for url in news_url_list]
        try:
            all_title=ray.get(future_to_url)
            chk=0
        except:
            chk=1
        
        print('완료' if chk==0 else '재실행')
        
    ray.shutdown()
    print(all_title[0])
