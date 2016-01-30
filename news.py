# coding=utf-8

import os
import json
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
        except Exception:
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
            if len(name) > 4:
                name = name[:-2]
            else:
                name = name.replace('最新', '新闻')
            channelId = channelDict['channelId']
            channelList.append(NewsChannel(channelId, name))
        return tuple(channelList)


class NewsItem(object):
    def __init__(self, dataDict):
        self.title = dataDict['title']
        self.pubDate = datetime.strptime(dataDict['pubDate'], "%Y-%m-%d %H:%M:%S")
        self.desc = dataDict['desc']
        self.hash = hash(dataDict['link'])

    def __hash__(self):
        return self.hash

    def toDict(self):
        return selt.__dict__


class NewsData(object):
    def __init__(self, newsapi, channelName=None, filepath=None):
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

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        self.__index = self.__index + 1
        if self.__index >= len(self.newsItems):
            raise StopIteration()
        return self.newsItems[self.__index - 1]

    def __contains__(self, item):
        for i in self.newsItems:
            if item.hash == i.hash:
                return True
        return False

    def getKeyWords(self, topN=10, withWeight=True, exclude=None):
        exclude_default = set([u'记者', u'新闻', u'报', u'本报', u'月', u'日'])
        if exclude is not None:
            exclude_input = set(exclude)
            exclude = exclude_default.union(exclude_input)
        else:
            exclude = exclude_default
        total = self.combineAllNewsItems()
        res = []
        for key, weight in jieba.analyse.textrank(total, topN+len(exclude), withWeight):
            if key in exclude:
                continue
            res.append((key, weight))
        return res[:topN]

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
                    if newsitem not in self.newsItems:
                        self.newsItems.append(newsitem)
                return 0

            process_news_data()
            for p in range(2, self.allPages + 1):
                self.currentPage = self.currentPage + 1
                newsdata = self.newsapi.fetchNewsData(self.channelId, self.currentPage)
                res_code = process_news_data()
                if res_code != 0:
                    break
            self.lastMarkTime = newMarkTime
        except Exception as err:
            print(err)

    def combineAllNewsItems(self):
        orderedItems = sorted(self.newsItems, key=lambda d: d.year*10000+d.month*100+d.day, reverse=True)
        news_str_list = map(lambda item: item.title + '\n' + item.desc, orderedItems)
        return reduce(lambda ns1, ns2: ns1 + '\n\n' + ns2, news_str_list)

    def save(self, name=None):
        dataDir = os.getcwd() + os.sep + "data" + os.sep
        if os.path.exists(dataDir) is False:
            os.mkdir(dataDir)
        if name is None:
            name = self.channelName
        filepath = dataDir + name + ' ' + self.startDate.strftime("%Y-%m-%d" + '.txt')
        with open(filepath, 'w') as f:
            self.name = name
            try:
                data = json.dumps(self, default=self.__toDict)
                f.write(data)
            except Exception as e:
                print(e)
                raise NewsError("Error: can not save news data")

    def load(self, filepath, newsapi):
        with open(filepath, 'r') as f:
            try:
                self.__fromDict(json.loads(f.read()))
            except Exception as err:
                print(err)
                raise NewsError("Error: can not load news data from " + filepath)

    def __fromDict(self, jsondict):
        self.name = jsondict['name']
        self.channelId, self.channelName = self.newsapi.findChannel(jsondict['channelName'])
        self.startDate = jsondict['startDate']
        self.lastMarkTime = jsondict['lastMarkTime']
        self.newsItems = list(map(lambda iDict: NewsItem(iDict), jsondict['items']))

    def __toDict(self):
        d = {}
        d['name'] = self.name
        d['channelName'] = self.channelName
        d['startDate'] = self.startDate.strftime("%Y-%m-%d")
        d['lastMarkTime'] = self.lastMarkTime.strftime("%Y-%m-%d %H:%M:%S")
        d['items'] = list(map(lambda item: item.toDict(), self.newsItems))
        return d
