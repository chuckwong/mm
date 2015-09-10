__author__ = 'Chuck'
# -*- coding:utf-8 -*-

import urllib2
import urllib
import re
import os
import tool
# from bs4 import BeautifulSoup

class Spider:

    def __init__(self):
        # self.proxy_support = urllib2.ProxyHandler({'http': 'http://'})
        self.headers = {
            'Referer': 'http://192.168.31.4:8080/?url=http%3A%2F%2Fmm.taobao.com%2Fjson%2Frequest_top_list.htm',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36',
        }
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'
        self.tool = tool.Tool()

    def getPage(self, pageIndex):
        url = self.siteURL + '?page=' + str(pageIndex)
        req = urllib2.Request(url, headers=self.headers)
        response = urllib2.urlopen(req)
        # print response.read().decode('gbk')
        return response.read().decode('gbk')

    def getContents(self, pageIndex):
        page = self.getPage(pageIndex)
        pattern = re.compile(r'<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            contents.append([item[0], item[1], item[2], item[3], item[4]])
        return contents

    def getDetailPage(self, infoURL):
        response = urllib2.urlopen(infoURL)
        return response.read().decode('gbk')

    def getBrief(self, page):
        pattern = re.compile(r'<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        result = re.search(pattern, page)
        return self.tool.replace(result.group(1))

    def getAllImg(self, page):
        pattern = re.compile(r'<div class="mm-aixiu-content".*?>(.*?)<!--', re.S)
        content = re.search(pattern, page)
        patternImg = re.compile(r'<img.*?src="(.*?)"', re.S)
        images = re.findall(patternImg, content.group(1))
        return images

    def saveImgs(self, images, name):
        number = 1
        print u"发现", name, u"共有", len(images), u"张照片"
        for imageURL in images:
            splitPath =imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = name + "/" + str(number) + "." + fTail
            self.saveImg(imageURL, fileName)
            number += 1

    def saveIcon(self, iconURL, name):
        splitPath = iconURL.split('.')
        fTail = splitPath.pop()
        fileName = name + "/icon." + fTail
        self.saveImg(iconURL, fileName)

    def saveBrief(self, content, name):
        fileName = name + "/" + name + ".txt"
        f = open(fileName, "w+")
        print u"正在保存个人信息为", fileName
        f.write(content.encode('utf-8'))
        f.close()

    def saveImg(self, imageURL, fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在保存图片为", fileName
        f.close()

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print u"新建了名字叫做", path, u"的文件夹"
            os.makedirs(path)
            return True
        else:
            print u"名为", path, "的文件夹已经存在"
            return False

    def savePageInfo(self, pageIndex):
        contents = self.getContents(pageIndex)
        for item in contents:
            #item[0]个人详情URL, item[1]头像URL, item[2]姓名, item[3]年龄, item[4]居住地
            print u"发现MM, 名字:", item[2], item[3], u"岁", "居住地: ", item[4]
            print u"保存信息到本地 --- ", item[2]
            print u"详细个人地址", item[0]
            detailURL = item[0]
            detailPage = self.getDetailPage(detailURL)
            brief = self.getBrief(detailPage)
            images = self.getAllImg(detailPage)
            self.mkdir(item[2])
            self.saveBrief(brief, item[2])
            self.saveIcon(item[1], item[2])
            self.saveImgs(images, item[2])

    def savePagesInfo(self, start, end):
        for i in range(start, end + 1):
            print u"正在第", i, u"页找MM"
            self.savePageInfo(i)

spider = Spider()
spider.savePagesInfo(1, 10)



