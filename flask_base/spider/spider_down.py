import requests
import json
import traceback
from bs4 import BeautifulSoup
from collections import OrderedDict


import os
def mkdir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False
#    现在需要搞定ID 的问题  biquge
#    批量控制下载 多线程控制章节下载 多进程控制小说下载  针对首次下载的小说
#    对于每天更新的小说  统一计算需要的更新 然后统一下载  多线程获取更新 多线程下载
#

#    两种下载模式    存在小说 每天的下载  和 不存在小说 批量下载 要对这两方面进行优化
#    https://www.biquge.lu/book/39651/504548085.html
def down_chapter(story_id, chapter_id, name, story_name):
    url = "https://www.biquge.lu/book/%s/%s.html"%(story_id,chapter_id)
    respons = requests.get(url)
    respons.encoding = 'gbk'
    chapter_text = respons.text.replace('\r', '\n')
    chapter_text = chapter_text.replace('<script>app2();</script>', '')
    chapter_text = chapter_text.replace('(%s)'%url, '')
    chapter_text = chapter_text.replace('chaptererror();', '')
    chapter_text = chapter_text.replace('请记住本书首发域名：www.biquge.lu。笔趣阁手机版阅读网址：m.biquge.lu', '')
    soup = BeautifulSoup(chapter_text, "html.parser")

    div_list = soup.find("div", id="content")
    chapter_strs = div_list.get_text('\n','<br/>')
    chapter_strs.replace("请记住本书首发域名：www.biquge.lu。笔趣阁手机版阅读网址：m.biquge.lu", "")
    mkdir("./story_data/%s"%story_name)
    json_out = OrderedDict()
    json_out['story_name'] = story_name
    json_out['name'] = name
    json_out['content_str'] = chapter_strs
    try:
        with open("./story_data/%s/%s.json" % (story_name, name), "w", encoding='utf-8') as f:
            json.dump(json_out, f, indent=4, ensure_ascii=False, )
    except Exception as e:
        print(e)
        print(traceback.print_exc())



#    剑来    id    作者    时间    状态    千里杀一人，十步不愿行。（大道朝天官方一群，群号码：311875513，大道朝天官方二群，群号码：220593959，欢迎加入）    分类    字数：906579
# 大道朝天 id


def getdown_id():
    path_file = "download_id_list.txt"
    download_id_list = {}
    if os.path.exists(path_file):
        file = open(path_file,'r')
        for line in file.readlines():
            # 读取文档内容，循环存入漫画id
            download_id_list[line.strip().split('\t')[0]] = [line.strip().split('\t')[1],line.strip().split('\t')[2]]
    else:
        file = open(path_file,'w')
        file.close()

    return download_id_list
def writedown_id(shuhui_load_dict,manhua_data_dict,load_id_list):
    for key in list(shuhui_load_dict.keys()):
        if int(key) in manhua_data_dict:
            continue
        else:
            del shuhui_load_dict[key]

    for key in load_id_list:
        shuhui_load_dict[key] = manhua_data_dict[key]

    with open("download_id_list.txt",'w') as file:
        file.writelines(dict_to_text(shuhui_load_dict))

def dict_to_text(data_dict):
    outstr = ""
    for key in data_dict:
        outstr = outstr + str(key) + '\t' + str(data_dict[key][0]) + '\t' + str(data_dict[key][1]) + '\n'
    return outstr



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







check_down_story("43597")
# down_chapter("39651","504548085","123",'123')