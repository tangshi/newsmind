# coding=utf-8

import os
import json
import time
from functools import reduce
import urllib.request
import urllib.error
from datetime import datetime, date
import jieba.analyse


class NewsError(Exception):
    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg


class NewsChannel(object):
    def __init__(self, Id, name):
        self.Id = Id
        self.name = name


class NewsAPI(object):
    def __init__(self, appid, appsign):
        self.appid = str(appid)
        self.appsign = appsign
        self.apihead = "http://route.showapi.com/109-35?showapi_appid=" + self.appid + "&showapi_sign=" + self.appsign
        self.channels = self.__getChannelList()
        if self.channels is None:
            raise NewsError('Can not fetch news channels')

    def fetchNewsData(self, channelId, page=1):
        url = self.getAPIUrl(channelId, page)
        try:
            return self.requestAPI(url)
        except urllib.error.URLError:
            raise NewsError("Can not fetch news data")

    def getAPIUrl(self, channelId, page=1):
        url = self.apihead + '&' + 'channelId' + '=' + channelId
        if page < 1:
            page = 1
        url = url + '&' + 'page' + '=' + str(page)
        url = url + "&showapi_timestamp=" + datetime.now().strftime('%Y%m%d%H%M%S')
        return url

    def requestAPI(self, url):
        try:
            newsdata = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
            if newsdata['showapi_res_code'] != 0:
                raise NewsError('response error: ' + newsdata['showapi_res_error'])
            return newsdata
        except urllib.error.URLError as urlerr:
            print(urlerr)
            raise urlerr

    def findChannel(self, channelName):
        for channel in self.channels:
            if channelName in channel.name:
                return (channel.Id, channel.name)
        return None

    def __getChannelList(self):
        url = "http://route.showapi.com/109-34?showapi_appid=" + self.appid + "&showapi_sign=" + self.appsign
        url = url + "&showapi_timestamp=" + datetime.now().strftime('%Y%m%d%H%M%S')
        channelList = []
        resp = self.requestAPI(url)
        if resp is None:
            return None
        for channelDict in resp['showapi_res_body']['channelList']:
            name = channelDict['name']
            if u'焦点' in name:
                continue
            channelId = channelDict['channelId']
            channelList.append(NewsChannel(channelId, name))
        return tuple(channelList)


class NewsItem(object):
    def __init__(self, dataDict):
        self.title = dataDict['title']
        self.pubDate = datetime.strptime(dataDict['pubDate'], "%Y-%m-%d %H:%M:%S")
        self.desc = dataDict['desc']
        if dataDict.get('hash') is not None:
            self.hash = dataDict['hash']
        else:
            link = dataDict.get('link')
            self.hash = hash(link)

    def __hash__(self):
        return self.hash

    def toDict(self):
        d = {}
        d['title'] = self.title
        d['pubDate'] = self.pubDate.strftime("%Y-%m-%d %H:%M:%S")
        d['desc'] = self.desc
        d['hash'] = self.hash
        return d


class NewsData(object):
    def __init__(self, newsapi, filepath=None, name=None, channelName=None):
        self.allPages = 0
        self.currentPage = 1
        self.maxResult = 20
        self.newsapi = newsapi
        if filepath is not None:
            self.load(filepath)
        else:
            self.channelId, self.channelName = self.newsapi.findChannel(channelName)
            self.newsItems = []
            today = date.today()
            self.startDate = today
            self.lastMarkTime = datetime(today.year, today.month, today.day)
            self.name = name
            self.keywords = []

    def getKeyWords(self, topN=20, withWeight=True, exclude=None):
        exclude_default = set([u'记者', u'新闻', u'报', u'本报', u'月', u'日'])
        if exclude is not None:
            exclude_input = set(exclude)
            exclude = exclude_default.union(exclude_input)
        else:
            exclude = exclude_default
        total = self.combineAllNewsItems()
        res = []
        for key, weight in jieba.analyse.textrank(total, topK=None, withWeight=withWeight):
            if key in exclude:
                continue
            res.append((key, weight))
        if topN:
            return res[:topN]
        else:
            return res

    def fetch(self):
        try:
            newsdata = self.newsapi.fetchNewsData(self.channelId, 1)
            newTimeStr = newsdata['showapi_res_body']['pagebean']['contentlist'][0]['pubDate']
            newMarkTime = datetime.strptime(newTimeStr, "%Y-%m-%d %H:%M:%S")
            if self.allPages < 1:
                self.currentPage = 1
                self.allPages = newsdata['showapi_res_body']['pagebean']['allPages']
                self.maxResult = newsdata['showapi_res_body']['pagebean']['maxResult']

            def process_news_data():
                nonlocal newsdata
                for newsdict in newsdata['showapi_res_body']['pagebean']['contentlist']:
                    newsitem = NewsItem(newsdict)
                    if newsitem.pubDate < self.lastMarkTime:
                        return -1
                    exists = False
                    for i in self.newsItems:
                        if newsitem.hash == i.hash:
                            exists = True
                            break
                    if not exists:
                        self.newsItems.append(newsitem)
                return 0

            process_news_data()
            for p in range(2, self.allPages + 1):
                time.sleep(1)
                self.currentPage = self.currentPage + 1
                newsdata = self.newsapi.fetchNewsData(self.channelId, self.currentPage)
                res_code = process_news_data()
                if res_code != 0:
                    break
            self.allPages = 0
            self.lastMarkTime = newMarkTime
            self.keywords = self.getKeyWords()
            self.save()
        except Exception as err:
            print(err)

    def combineAllNewsItems(self):
        def sortedkey(newsitem):
            pubDate = newsitem.pubDate
            return pubDate.year*10000 + pubDate.month*100 + pubDate.day
        orderedItems = sorted(self.newsItems, key=sortedkey, reverse=True)
        news_str_list = list(map(lambda item: item.title + '\n' + item.desc, orderedItems))
        if len(news_str_list) == 0:
            result = ""
        else:
            result = reduce(lambda ns1, ns2: ns1 + '\n\n' + ns2, news_str_list)
        return result

    def getWordsNum(self):
        if len(self.newsItems) == 0:
            return 0
        num = 0
        for item in self.newsItems:
            num = num + len(item.title) + len(item.desc)
        return num

    def getFilePath(self):
        dataDir = os.getcwd() + os.sep + "data" + os.sep
        if os.path.exists(dataDir) is False:
            os.mkdir(dataDir)
        filepath = dataDir + self.name + ' ' + self.startDate.strftime("%Y-%m-%d") + '.txt'
        return filepath

    def save(self):
        filepath = self.getFilePath()
        with open(filepath, 'w', encoding='utf-8') as f:
            try:
                toDict = self.__toDict()
                data = json.dumps(toDict, ensure_ascii=False)
                f.write(data)
            except Exception as e:
                print(e)
                raise NewsError("Error: can not save news data")

    def load(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                self.__fromDict(json.loads(f.read()))
            except Exception as err:
                print(err)
                raise NewsError("Error: can not load news data from " + filepath)

    def __fromDict(self, jsondict):
        self.name = jsondict['name']
        self.channelId, self.channelName = self.newsapi.findChannel(jsondict['channelName'])
        self.startDate = datetime.strptime(jsondict['startDate'], "%Y-%m-%d")
        self.lastMarkTime = datetime.strptime(jsondict['lastMarkTime'], "%Y-%m-%d %H:%M:%S")
        self.keywords = jsondict['keywords']
        self.newsItems = list(map(lambda iDict: NewsItem(iDict), jsondict['items']))

    def __toDict(self):
        d = {}
        d['name'] = self.name
        d['channelName'] = self.channelName
        d['startDate'] = self.startDate.strftime("%Y-%m-%d")
        d['lastMarkTime'] = self.lastMarkTime.strftime("%Y-%m-%d %H:%M:%S")
        d['keywords'] = self.keywords
        d['items'] = list(map(lambda item: item.toDict(), self.newsItems))
        return d
