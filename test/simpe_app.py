from wsgiref.simple_server import make_server



'''
手写一个简易的应用框架，该框架必须是一个可调用对象，并且需要接收两个参数

参一：环境变量(字典)
参二：回调函数(返回)

'''
def login():
    return 'login'

def register():
    return 'register'


urls = {  # 该urls是通过一个最简单的字典映射的方式
    '/login': login,
    '/register': register
}

def simpe_app(environ, start_respone):
    path = environ.get('PATH_INFO')
    if path is None and path not in urls.key():
        start_respone('404 not found', [('Content-type', 'text/plain')])
        return [b'404 not found']
    
    func = urls.get(path)
    if path is None:
        start_respone('404 not found', [('Content-type', 'text/plain')])
        return [b'404 not found']
    
    start_respone('200 OK', [('Content-type', 'text/plain')])
    return [func().endcode]

server = make_server('192.168.211.129', 8081, app = simpe_app)

server.serve_forever()


'''
Server组件都干了什么？
首先由于中间件的存在，你现在的Server不一定接收的是浏览器传来的http信息，有可能是中间件传来的
如果是中间件传来的需要把之前web服务器封装好的environ变量存在当前的environ变量中，构建新的environ
1.根据客户端传来的http协议内容或者是之前webServer中间件的uwsgi内容构建新的environ变量

2.定义一个回调函数start_respone,用于接收返回的状态和响应头

3.调用可调用对象，将上面的两个参数传递给该对象

4.接收返回结果，将请求的结果返回
'''
