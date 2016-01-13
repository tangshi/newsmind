'''
A simple web app based on [Bottle](http://bottlepy.org/)
'''

from bottle import route, run, template, error, static_file


@error(404)
def error404(error):
    return 'PAGE NOT FOUND !'


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static/')


@route('/')
def root():
    return template('newsmind')

run(host='localhost', port=8080, debug=True)
