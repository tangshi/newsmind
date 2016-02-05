# coding=utf-8

'''
A simple web app based on [Bottle](http://bottlepy.org/)
'''

import os
from urllib import parse
from news import NewsAPI, NewsData
from bottle import route, run, template, error, static_file, abort, request, redirect


'''
init global variables
load all exists tasks
'''
newsapi = NewsAPI('15505', '80af212f997b4382ba62ca7d2c79f4f7')
if os.path.exists('data') is False:
    os.mkdir('data')
files = list(filter(lambda name: name.endswith(".txt"), os.listdir('data')))
tasks = []
dataDir = os.getcwd() + os.sep + "data" + os.sep
for f in files:
    try:
        t = NewsData(newsapi, filepath=(dataDir + f))
        tasks.append(t)
    except:
        pass
tasks.sort(key=lambda nd: nd.startDate, reverse=True)


@error(404)
def error404(error):
    return 'PAGE NOT FOUND !'


@route('/static/<filename:path>')
def sendStatic(filename):
    return static_file(filename, root='./static/')


@route('/tasks/<taskname>')
def showTask(taskname):
    task = None
    for t in tasks:
        if t.name == taskname:
            task = t
            break
    if task is None:
        abort(code=404, text="Task dose NOT exist!")
    # TODO return task detail page
    return taskname


@route('/newtask')
def newTask():
    return template('newtask', channels=newsapi.channels)


def checkNewTask(taskname, channelname):
    if taskname == "" or channelname == "":
        return False
    else:
        return True


@route('/newtask', method='POST')
def createNewTask():
    taskname = request.forms.get('taskname')
    unquotedtaskname = parse.unquote(taskname)
    print("taskname: ", unquotedtaskname)
    channelid = request.forms.get('channelid')
    print("cannelid: ", channelid)
    channelname = None
    for channel in newsapi.channels:
        if channel.Id == channelid:
            channelname = channel.name
            break
    if channelname is None:
        return "<p>Unknown channel.</p>"
    print(unquotedtaskname, channelname)
    # TODO create a new task
    if checkNewTask(taskname, channelname):
        redirect('/tasks/' + taskname)
    else:
        return "<p>Failed.</p>"


@route('/')
def root():
    # tasknames = list(map(lambda t: t.name, tasks))
    return template('newsmind', tasknames=files)

run(host='localhost', port=8080, debug=True)
