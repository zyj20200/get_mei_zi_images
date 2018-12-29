# -*- coding:utf-8 -*-

import os
import time
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    'Referer': 'http://www.mmjpg.com/tag/xinggan'
}

## tag/xinggan 性感首页
url = "http://www.mmjpg.com/tag/xinggan"

html = requests.get(url).text
soup1 = etree.HTML(html)
## 性感的页数
all_page = int(soup1.xpath('/html/body/div[3]/div[1]/div[2]/a[8]/@href')[0].split('/')[-1])
## 创建"美图"文件夹,存储图片
path = '美图/'
is_exists = os.path.exists(path)
if not is_exists:
    print('美图--文件夹不存在.....')
    print('创建文件夹--美图')
    os.mkdir(path)
    print('创建成功')
else:
    print('文件夹已存在')

print('-'*30)
while 1:
    print('下载:1  ')
    print('退出:0  ')
    print('强制退出请按:ctrl + c')
    flag = input('请输入代码:')
    if flag == '0':
        break
    elif flag == '1':

        for page in range(all_page):
            url = "http://www.mmjpg.com/tag/xinggan/%d" % (page + 1)
            html = requests.get(url).text
            soup1 = etree.HTML(html)

            # 性感每一页总共15个人物
            for i in range(15):
                path = "/html/body/div[3]/div[1]/ul/li[%d]/a/@href" % (i + 1)
                # 每个人物的 首页 url
                tep_url = soup1.xpath(path)
                # 人物id  referer需要人物的id
                id = int(tep_url[0].split('/')[-1].replace('.jpg', ''))

                dir_name = '美图/' + str(id)
                os.mkdir(dir_name)
                # 人物标题
                title = soup1.xpath('/html/body/div[3]/div[1]/ul/li[%d]/span[1]/a/text()' % (i + 1))[0]
                # 首页的内容
                pic_page = requests.get(tep_url[0]).text
                # 解析首页内容
                soup2 = etree.HTML(pic_page)
                # 该人物的图片数量
                page_num = int(soup2.xpath('//*[@id="page"]/a[7]/text()')[0])
                # 获取人物首页图片的url
                # [img]http://fm.shiyunjj.com/2018/1502/1ie6.jpg[/img]
                pic_url = soup2.xpath('//*[@id="content"]/a/img/@src')[0]
                # 1ie6.jpg
                detail_url_end = pic_url.split('/')[-1]
                # http://fm.shiyunjj.com/2018/1502/
                detail_url_top = pic_url.replace(detail_url_end, '')
                # 下载图片
                for i in range(page_num):
                    # referer
                    detail_url = "http://www.mmjpg.com/mm/%d/%d" % (id, i + 1)
                    headers['Referer'] = detail_url

                    # 获取图片链接
                    html_detail = requests.get(detail_url).text
                    soup3 = etree.HTML(html_detail)
                    pic = soup3.xpath('//*[@id="content"]/a/img/@src')[0]

                    # 下载图片
                    with open(dir_name + '/' + str(i + 1) + '.jpg', 'wb') as f:
                        print('正在下载：', dir_name + '/' + str(i + 1) + 'jpg')
                        f.write(requests.get(pic, headers=headers).content)
                        print('强制退出请按:ctrl + c')

                    # time.sleep(0.5)
    else:
        print('代码输入有误,请重新输入!!!')
        print('-'*30)

