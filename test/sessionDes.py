import web
'''
web.session.Session是webpy框架下用于获取用户session的接口，该接口共有3个参数
参一：框架名称
参二：获取到session后存储到哪
    选择一：存储到磁盘上的session目录下
        session = web.session.Session(app, web.session.DiskStore('session'))
        
    选择二：存储到mysql数据库中
        session = web.session.Session(app, web.session.DBStore(Config.gdb, 'session'))
    选择三：存储到redis缓存中
        session = web.session.Session(app, RedisStore(Config.grds, Config.SESSION_EXPIRETIME))
            
'''
