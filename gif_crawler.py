#coding=utf-8
import requests
from bs4 import BeautifulSoup
import shutil
import re
import time



def get_gif_urls(content):
    output = []
    soup = BeautifulSoup(content)
    for link in soup.find_all('a'):
        href = link.get('href')
        if href != None and 'gif' in href and 'blogspot.com' in href:
            output.append(href)
    '''for img in soup.find_all('img'):
        src = img.get('src')
        if src != None and 'gif' in src and 'blogspot.com' in src:
            output.append(src)'''
    return output

def get_gif(url, path):
    if 'http:' not in url and 'https:' not in url:
        return
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            f.close()

def get_page_list(url):
    page_list = []
    p = re.compile(r'http://hornydragon\.blogspot\.tw/\d+/\d+/\d+.+')
    #p = re.compile(r'http://hornydragon\.blogspot\.tw/.+')
    content = requests.get(url).text
    soup = BeautifulSoup(content)
    next_page_url = None
    hfeed = soup.find('div', {"class": 'hfeed'})
    for link in hfeed.find_all('a'):
        href = link.get('href')
        if p.match(href) != None:
            page_list.append(href)
    for link in soup.find_all('a'):
        href = link.get('href')
        if link.text.strip() == u'下一頁':
            next_page_url = href
    return {'page_list':page_list,'next_page_url':next_page_url}

if __name__ == '__main__':
    next_page_url = 'http://hornydragon.blogspot.com/search/label/%E9%9B%9C%E4%B8%83%E9%9B%9C%E5%85%AB%E7%9F%AD%E7%AF%87%E6%BC%AB%E7%95%AB%E7%BF%BB%E8%AD%AF?&max-results=50'
    while True:
        print next_page_url
        page_list_dic = get_page_list(next_page_url)
        print page_list_dic
        for page_url in page_list_dic['page_list']:
            print '>>> ' + page_url
            content = requests.get(page_url).text
            gif_urls = get_gif_urls(content)
            for gif_url in gif_urls:
                path1 = gif_url.split('/')[-2] + gif_url.split('/')[-1]
                path2 = page_url.split('/')[-1].split('.')[0]
                get_gif(gif_url, 'gifs/' + path2 + '_' +path1)
            time.sleep(1)
        if page_list_dic['next_page_url'] == None:
            break
        next_page_url = page_list_dic['next_page_url']
        time.sleep(3)

