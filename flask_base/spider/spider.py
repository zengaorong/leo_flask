# coding=utf-8
import requests
import json
import traceback
from bs4 import BeautifulSoup
from collections import OrderedDict


"""
爬虫api：
    搜索结果页：get_index_result(search)
    小说章节页：get_chapter(url)
    章节内容：get_article(url)
"""
class DdSpider(object):

    # def __init__(self):
    #     self.headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
    #     }

    def parse_url(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                # 处理一下网站打印出来中文乱码的问题
                resp.encoding = 'utf-8'
                return resp.text
            return None
        except ConnectionError:
            print('Error.')
        return None


    #    小说 作者 更新时间 状态 id   同时需要同步数据库
    def check_down_story(id):
        # url = "http://www.biquge.lu/book/%s/" % "39651"
        url = "http://www.biquge.lu/book/%s/" % id
        print(url)
        respons = requests.get(url)
        respons.encoding = 'gbk'
        soup = BeautifulSoup(respons.text.replace('\r', '\n'), 'html.parser')
        chapter_soup = soup.find('div', {'class', 'listmain'})
        small = soup.find('div',{'class', 'small'})
        chapter_list = chapter_soup.find_all('dd')
        updata_time = soup.find_all('meta')
        story_name = soup.find('h2').string
        print(story_name)

        hmap_test = {}
        # hmap_test[small.find_all('span')[0].string.split('：')[0].strip()] = small.find_all('span')[0].string.split('：')[1].strip()

        #    截取 作者：烽火戏诸侯
        author_name = small.find_all('span')[0].string.split('：')[1].strip()
        #    截取 分类：修真小说
        story_type = small.find_all('span')[1].string.split('：')[1].strip()
        #    截取 状态：连载
        story_state = small.find_all('span')[2].string.split('：')[1].strip()
        #    截取 字数：2600272
        story_words = small.find_all('span')[3].string.split('：')[1].strip()
        #    截取 更新时间：2019-11-20 23:59:00
        story_uptime = small.find_all('span')[4].string.split('：')[1].strip()
        #    截取 最新章节：<a href="/book/43597/77576986.html">第六百七十一章 天寒加衣</a>
        story_upchapter_id = small.find_all('span')[5].find('a')['href'].split('/')[-1].replace('.html','')
        story_upchapter_name = small.find_all('span')[5].find('a').string

        hmap_test['作者'] = author_name
        hmap_test['分类'] = story_type
        hmap_test['状态'] = story_state
        hmap_test['字数'] = story_words
        hmap_test['最新章节id'] = story_upchapter_id
        hmap_test['最新章节'] = story_upchapter_name
        hmap_test['更新时间'] = story_uptime
        hmap_id = "biquge.lu" + id

        # import redis
        # conn=redis.Redis(host='127.0.0.1',port=6379)
        # conn.hmset(hmap_id,hmap_test)

        print(small.find_all('span'))
        #  作者-0 分类-1 状态-2 字数-3 更新时间-4 最新章节-5 最新章节id
        print(small.find_all('span')[0].string.split('：')[1].strip())
        print(small.find_all('span')[1].string)
        print(small.find_all('span')[2].string)
        print(small.find_all('span')[3].string)
        print(small.find_all('span')[4].string)
        print(small.find_all('span')[5].find('a')['href'].split('/')[-1].replace('.html',''))
        print(small.find_all('span')[5].find('a').string)



        chapter_dict = OrderedDict()
        for chapter in chapter_list:
            chapter_id = chapter.find('a')['href'].split('/')[-1].replace('.html','')
            chapter_name = chapter.find('a').string
            if chapter_id in chapter_dict:
                chapter_dict.pop(chapter_id)

            chapter_dict[chapter_id] = chapter_name

        for chapter_id in chapter_dict:
            pass
            # down_chapter(id, chapter_id, chapter_dict[chapter_id], story_name)





    # # 搜索结果页数据
    # def get_index_result(self, search, page=0):
    #     if page == 0:
    #         url = 'http://zhannei.baidu.com/cse/search?s=1682272515249779940&entry=1&q={search}'.format(search=search)
    #     else:
    #         url = 'http://zhannei.baidu.com/cse/search?q={search}&p={page}&s=1682272515249779940'.format(
    #             search=search, page=page)
    #     resp = self.parse_url(url)
    #     html = etree.HTML(resp)
    #     titles = html.xpath('//*[@id="results"]/div/div/div/h3/a/@title')
    #     urls = html.xpath('//*[@id="results"]/div/div/div/h3/a/@href')
    #     images = html.xpath('//*[@id="results"]/div/div/div/a/img/@src')
    #     authors = html.xpath('//*[@id="results"]/div/div/div/div/p[1]/span[2]/text()')
    #     profiles = html.xpath('//*[@id="results"]/div/div/div/p/text()')
    #     styles = html.xpath('//*[@id="results"]/div/div/div/div/p[2]/span[2]/text()')
    #     times = html.xpath('//*[@id="results"]/div/div/div/div/p[3]/span[2]/text()')
    #     for title, url, image, author, profile, style, tim in zip(titles, urls, images, authors, profiles, styles,
    #                                                               times):
    #         data = {
    #             'title': title.strip(),
    #             'url': url,
    #             'image': image,
    #             'author': author.strip(),
    #             'profile': profile.strip().replace('\u3000', '').replace('\n', ''),
    #             'style': style.strip(),
    #             'time': tim.strip()
    #         }
    #         yield data

    # # 小说章节页数据
    # def get_chapter(self, url):
    #     resp = self.parse_url(url)
    #     html = etree.HTML(resp)
    #     chapters = html.xpath('//*[@id="main"]/div/dl/dd/a/text()')
    #     urls = html.xpath('//*[@id="main"]/div/dl/dd/a/@href')
    #     for chapter_url, chapter in zip(urls, chapters):
    #         data = {
    #             'url': str(url) + chapter_url,
    #             'chapter': chapter
    #         }
    #         yield data
    #
    # # 章节内容页数据
    # def get_article(self, url):
    #     resp = self.parse_url(url)
    #     html = etree.HTML(resp)
    #     content = html.xpath('//*[@id="content"]/text()')
    #     return '<br>'.join(content)


dd = DdSpider()
# for i in dd.get_index_result('诛仙',page=0):
#     print(i)
print(dd.get_article('http://www.23us.cc/html/138/138189/7009918.html'))

