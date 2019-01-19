# coding=utf-8
from bs4 import BeautifulSoup
import requests
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


file_path = os.getcwd() + '\\'  # 下载目录
domain = "https://cn.rti.tw"


# 获取广播剧下载链接
def get_url_list():
    novel_list_resp = requests.get('https://cn.rti.tw/radio/novelList')
    opera_soup = BeautifulSoup(novel_list_resp.text, "lxml")
    # 获取每个广播剧的div块
    for div in opera_soup.find_all("div", class_="program-item"):
        result = ''
        # 获取每个广播剧的链接
        opera_link = domain + div.find("a").get('href')
        # 获取每个广播剧的名称
        title = div.find("div", class_="title").string
        print '当前爬取广播剧：' + title
        # 访问单个广播剧页面
        novel_view_resp = requests.get(opera_link)
        view_soup = BeautifulSoup(novel_view_resp.text, "lxml")
        # 先找到第一个h2,后面紧跟的ul里有单个广播剧的所有集链接
        list_a = view_soup.find('h2').find_next_sibling('ul').find_all('a')
        num = 1
        for a in list_a:
            view_link = domain + a.get('href')
            print '获取%s单集链接%s' % (title, view_link)
            # 打开单集的播放页面
            play_resp = requests.get(view_link)
            play_soup = BeautifulSoup(play_resp.text, "lxml")
            src = play_soup.find('source').attrs['src']
            print '获取%s%s下载链接%s' % (title, num, src)
            # 将单个广播剧所有下载链接拼接
            result += "%s%s:%s\n" % (title, str(num), src)
            num += 1
        # 将单个广播剧所有下载链接保存到txt文件
        _save_src(title, result)
        print '保存%s链接完毕' % title


def _save_src(name, content):
    name = file_path + name + '.txt'
    with open(name, 'wb') as f:
        f.write(content)


def download_opera(opera):
    # 保存下载链接的txt文件路径
    path = r'' + file_path + opera
    # 文件名有中文，需要解码为unicode
    path = path.decode('utf-8')
    # 将下载链接全部读出来
    with open(path, 'rb') as f:
        links = f.readlines()
    # 循环下载
    for link in links:
        name, url = link.split(':', 1)
        name = name.decode('utf-8')
        url = url.split('\n')[0]
        # 下载MP4文件的路径
        file_name = "%s%s.mp4" % (file_path, name)
        print file_name, url
        _download_file(file_name, url)
        print "%s下载完毕" % name


def _download_file(name, url):
    r = requests.get(url)
    with open(name, 'wb') as f:
        f.write(r.content)


if __name__ == '__main__':
    # 获取所有广播剧下载链接并保存成一个个txt
    # get_url_list()
    # 单独下载某个广播剧(其实可以在抓下载链接的时候就下载，但我得先试听一集感兴趣才下载哦)
    download_opera('冰窟窿.txt')