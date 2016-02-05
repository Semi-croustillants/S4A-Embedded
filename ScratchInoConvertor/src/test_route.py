from bottle import route, run, request


@route('/')
def hello():
    return "Hello World!"


@route('/arduinize', method='POST')
def arduinize():
    print request.json
    return 'json_string'

run(host='localhost', port=8080, debug=True)
