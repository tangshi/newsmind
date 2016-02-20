# coding=utf-8

'''
A simple web app based on [Bottle](http://bottlepy.org/)
'''

import os
from urllib import parse
from datetime import date
from bottle import Bottle, abort, error, redirect, request, run, static_file, template
from news import NewsAPI, NewsData


class Task:
    def __init__(self, name=None, filepath=None):
        if filepath is not None:
            beg = filepath.rfind('/') + 1
            end = filepath.rfind(".")
            if end == -1:
                end = len(filepath)
            filename = filepath[beg:end]
            space = filename.rfind(' ')
            self.name = filename[:space]
            self.datestr = filename[space+1:]
        else:
            self.name = name
            self.datestr = date.today().strftime("%Y-%m-%d")
        self.filepath = filepath
        self.newsdata = None


bottle = Bottle()
newsapi = NewsAPI('15505', '80af212f997b4382ba62ca7d2c79f4f7')

workdir = os.getcwd()
if os.path.exists('data') is False:
    os.mkdir('data')
files = list(filter(lambda name: name.endswith(".txt"), os.listdir('data')))
tasks = []
datadir = workdir + os.sep + "data" + os.sep
for f in files:
    t = Task(filepath=(datadir + f))
    tasks.append(t)
tasks.sort(key=lambda t: t.datestr, reverse=True)


@error(404)
def error404(error):
    return template('error')


@bottle.route('/static/<filename:path>')
def sendStatic(filename):
    return static_file(filename, root='./static/')


def findTask(taskname):
    task = None
    for t in tasks:
        if t.name == taskname:
            task = t
            break
    if task is None:
        abort(code=404, text="Task dose NOT exist!")
    return task


@bottle.route('/tasks/<taskname>')
def showTask(taskname):
    task = findTask(taskname)
    if task.newsdata is None:
        task.newsdata = NewsData(newsapi, filepath=task.filepath)
    return template('taskdetail', task=task)


@bottle.route('/tasks/<taskname>', method='POST')
def refreshTask(taskname):
    task = findTask(taskname)
    task.newsdata.fetch()


@bottle.route('/deltask/<taskname>')
def deleteTask(taskname):
    global tasks
    task = findTask(taskname)
    os.remove(task.newsdata.getFilePath())
    tasks.remove(task)
    redirect('/')


def checkNewTask(taskname, channelname):
    if taskname == "" or channelname == "":
        return False
    else:
        return True


@bottle.route('/tasks', method='POST')
def createNewTask():
    taskname = request.forms.get('taskname')
    unquotedtaskname = parse.unquote(taskname)
    print("taskname:", unquotedtaskname)
    channelid = request.forms.get('channelid')
    channelname = None
    for channel in newsapi.channels:
        if channel.Id == channelid:
            channelname = channel.name
            break
    if channelname is None:
        return "Unknown channel."
    print("cannelid:", channelid, "channelname:", channelname)
    if checkNewTask(taskname, channelname) is False:
        return "Failed to create task."
    else:
        task = None
        global tasks
        for t in tasks:
            if t.name == unquotedtaskname:
                task = t
                break
        if task is None:
            task = Task(name=unquotedtaskname)
            task.newsdata = NewsData(newsapi, name=task.name, channelName=channelname)
            task.newsdata.save()
            tasks.insert(0, task)
        redirect('/tasks/' + taskname)


@bottle.route('/')
def root():
    return template('newsmind', tasks=tasks, channels=newsapi.channels)


run(bottle, host='localhost', port=8000, debug=True, reloader=True)
