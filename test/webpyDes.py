import web

urls = (
    '/', 'Hello',
)

app = web.application(urls, globals())  # 创建应用框架

'''
web.application源码解析
初始化函数中
def __init__(self, mapping=(), fvars={}, autoreload=None):
        if autoreload is None:
            autoreload = web.config.get("debug", False)
        self.init_mapping(mapping)
        self.fvars = fvars
        self.processors = []

        self.add_processor(loadhook(self._load))
        self.add_processor(unloadhook(self._unload))
        
        def load(self, env):
            """Initializes ctx using env."""
            ctx = web.ctx
            ctx.clear()
            ctx.status = "200 OK"
            ctx.headers = []
            ctx.output = ""
            ctx.environ = ctx.env = env
            ctx.host = env.get("HTTP_HOST")

            if env.get("wsgi.url_scheme") in ["http", "https"]:
                ctx.protocol = env["wsgi.url_scheme"]
            elif env.get("HTTPS", "").lower() in ["on", "true", "1"]:
                ctx.protocol = "https"
            else:
                ctx.protocol = "http"
            ctx.homedomain = ctx.protocol + "://" + env.get("HTTP_HOST", "[unknown]")
            ctx.homepath = os.environ.get("REAL_SCRIPT_NAME", env.get("SCRIPT_NAME", ""))
            ctx.home = ctx.homedomain + ctx.homepath

解析：
1.用mapping去接收urls元组

2.然后调用init_mapping方法将mapping路由元组转化成list路由列表的形式

形如:urls = (
    '/', 'Hello',
    '/register', 'Register',
    '/login', 'Login',
)
转化位列表形式
mapping = [['/', 'Hello'], ['register', 'Register'], ['login', 'Login']
后面框架在进行url路由的时候回遍历mapping列表

3.load中，回给ctx变量赋值，该变量和environ类似

'''

application = app.wsgifunc()  # 该框架去绑定web服务器

'''
app.wsgifunc()源码解析：

    def wsgifunc(self, *middleware):
        """Returns a WSGI-compatible function for this application."""

        def wsgi(env, start_resp):
            pass
            
        for m in middleware:
            wsgi = m(wsgi)

        return wsgi
    def handle(self):
        fn, args = self._match(self.mapping, web.ctx.path)
        return self._delegate(fn, self.fvars, args)
解析：
1.遍历中间件
2.返回一个可调用对象函数，去实现WSGI协议
'''
class Hello:
    def GET(self):
        return 'Hello'
    
if __name__ == '__main__':
    # 使用webpy框架自带的一个用于测试的小型web服务器，该web服务器支持WSGI协议
    app.run()