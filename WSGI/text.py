from wsgiref.simple_server import make_server
import sys
import time

class ResponeTimingMiddleware(object):
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        start_time = time.time()
        response = self.app(environ, start_response)
        response_time = (time.time() - start_time) * 1000
        time_text = "记录请求耗时时间中间件输出\n\n 本次耗时：{:.10f}ms \n\n\n".format(response_time)
        return [*response, time_text.encode('utf-8')]

def login(req):
    print(req)
    return 'login\n\n'

def register(req):
    print(req)
    return 'register\n\n'

def home(req):
    print(req)
    return 'home\n\n'

def index(req):
    print(req)
    return 'index\n\n'

all_url = {
    '/login': login,
    '/register': register,
    '/home': home,
    '/index': index
}

def simple_app(environ, start_response):
    url = environ.get('PATH_INFO')
    params = environ.get('QUERY_STRING')

    if url is None or url not in all_url.keys():
        start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
        return [b'404 Not Found']
    
    res = all_url.get(url)
    if res is None:
        start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
        return [b'404 Not Found']
    return_body = []
    return_body.append(res(params))
    for k,v in environ.items():
        return_body.append("{} : {}".format(k,v))
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return ['\n'.join(return_body).encode('utf-8')]

application = ResponeTimingMiddleware(simple_app)
server = make_server('192.168.211.140', 8081, application)
server.serve_forever()