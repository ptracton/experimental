from bottle import route, run, template, error


@error(404)
def error404(error):
    return 'Nothing here'


@route('/')
@route('/hello/<name>')
def index(name='Stranger'):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
