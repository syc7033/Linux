import web
import Account
import json
import ErrorCfg
import Error
import Config
import logging
import logging.config
import Shop
import Task
import Lobby
from RedisStore import RedisStore

urls = (  # 路由
    '/', 'Hello',
    '/register', 'Register',
    '/login', 'Login',
    '/shop/cfg', 'Shop_cfg',
    '/shop/buy', 'Shop_buy',
    '/task/cfg', 'Task_cfg',
    '/task/reward', 'Task_reward',
    '/sign', 'Sign',
    '/mail/send', 'Mail_send',
    '/mail/list', 'Mail_list',
    '/mail/del', 'Mail_del',
    '/mail/getattach', 'Mail_getattach',
    '/mail/delete/all', 'Mail_del_all'
)

print(Config.gdb)

app = web.application(urls, globals())
application = app.wsgifunc() # webpy可以外接服务器（uWSGI服务器，提供了uwsgi接口协议和WSGI接口协议的webServer）

logging.config.fileConfig("logging.conf")
logger = logging.getLogger('applog')


# 通过web.session.Session接口获取session
if web.config.get('_session') is None:
    # session = web.session.Session(app, web.session.DBStore(Config.gdb, 'session'))
    session = web.session.Session(app, RedisStore(Config.grds, Config.SESSION_EXPIRETIME))  # 获取session中
    web.config._session = session
else:
    session = web.config._session

# logger.debug(f"session {session}")

def CatchError(func):  # 捕获异常的装饰器
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
    return wrapper

def CheckLogin(func):  # 检测登录装饰器
    def wrapper(*arg, **kwargs):
        # 登录检查，看session的userid字段是否存在
        if session.__dict__.has_key('userid'):
            return func(*arg, **kwargs)
        else:
            return Error.errorResult({ErrorCfg.EC_LOGIN_INVALID, ErrorCfg.ER_LOGIN_INVALID})
    return wrapper


class Hello:  # 欢迎功能类
    @CatchError
    def GET(self):
        return 'Hello, '


 # CatchError(Post())
class Register:  # 注册功能类
    @CatchError  # CatchError(Post)
    def POST(self):
        req = web.input(phonenum = '', password = '', nick = '', sex = '', idcard = '') 

        phonenum = req.phonenum
        password = req.password
        nick = req.nick
        sex = req.sex
        idcard = req.idcard

        # 检测手机号格式
        if not Account.CheckPhonenum(phonenum):
            return Error.errorResult(ErrorCfg.EC_REGISTER_PHONENUM_TYPE_ERROR, ErrorCfg.ER_REGISTER_PHONENUM_TYPE_ERROR)
        
        # 检测手机号是否重复
        if Account.CheckPhonenumRepeat(phonenum):
            return Error.errorResult(ErrorCfg.EC_REGISTER_PHONENUM_REPEAT_ERROR, ErrorCfg.ER_REGISTER_PHONENUM_REPEAT_ERROR)
        
        # 检测身份证格式
        if not Account.CheckIdCard(idcard):
            return Error.errorResult(ErrorCfg.EC_REGISTER_ID_CARD_TYPE_ERROR, ErrorCfg.ER_REGISTER_ID_CARD_TYPE_ERROR)
        
        #检测密码格式
        if not Account.CheckPwd(password):
            return Error.errorResult(ErrorCfg.EC_REGISTER_PWD_TYPE_ERROR, ErrorCfg.ER_REGISTER_PHONENUM_TYPE_ERROR)
       
        #注册账号
        Account.InitUser(phonenum, password, nick, sex, idcard)
        return json.dumps({'code': 0})

class Login:  # 注册功能类
    @CatchError
    def POST(self):
        req = web.input(userid = '', pwd = '')

        userid = req.userid
        pwd = req.pwd

        # 校验
        result = Account.VerifyAcconut(userid, pwd)
        if result['code'] != 0:
            return Error.errorResult(result['code'], result['reason'])
        
        # 登录处理
        result = Account.HandleLogin(userid, session)
        if result['code'] != 0:
            return Error.errorResult(ErrorCfg.EC_LOGIN_HANDLE_ERROR, ErrorCfg.ER_LOGIN_HANDLE_ERROR)
        return json.dumps({'code':0})

class Shop_cfg():  # 获取商城配置类
    @CatchError
    @CheckLogin
    def GET(self):
        req = web.input(version = '')

        version = int(req.version)

        shopcfg = Shop.GetShopCfg(version)
        return json.dumps({'code': 0, 'shopcfg': shopcfg})

class Shop_buy():  # 商城购买类
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', propid = '', pronum = '', shopversion = '', version = '')

        userid = int(req.userid)
        propid = int(req.propid)
        propnum = int(req.propnum)
        shopversion = int(req.shopversion)
        version = int(req.version)

        dictInfo = Shop.ShopBuy(userid, propid, propnum, shopversion, version)
        
        return json.dumps({'code': 0, 'dictInfo': dictInfo})

class Task_cfg:  # 获取任务配置
    @CatchError
    @CheckLogin
    def GET(self):
        req = web.input(userid = '', version = '')
        userid = int(req.userid)
        version = int(req.version)
        taskcfg = Task.GetTaskCfg(userid, version)
        return json.dumps({'code': 0, 'taskcfg': taskcfg})

class Task_reward:  # 任务奖励
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', taskid = '')
        userid = req.userid
        taskid = req.taskid
        rewardinfo = Task.TaskReward(userid, taskid)
        if rewardinfo['code'] != 0:
            return Error.errorResult(rewardinfo['code'], rewardinfo['reason'])
        return json.dumps({'code': 0, 'rewardinfo': rewardinfo})

class Sign:  # 签到
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', signtype = '', date = '')  # signtype可能回补签 和补签的日期
        userid = int(req.userid)
        signtype = int(req.signtype)
        date = req.date
        signinfo = Task.UserSign(userid, signtype, date)
        if signinfo['code'] != 0:
            return Error.errorResult(signinfo['code'], signinfo['reason'])
        return json.dumps({'code': 0, 'signinfo': signinfo})



class Mail_send:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(useridlist = '', type = '', title = '', context = '', attach = '', fromuserid = '', isglobal = ' ')
        Lobby.SendMail(req)

class Mail_list:
    @CatchError
    @CheckLogin
    def GET(self):
        req = web.input(userid = '')
        userid = req.userid;
        mailinfo = Lobby.GetMailList(userid)
        return json.dumps({'code': 0, 'mailinfo': mailinfo})

class Mail_del:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', mailid = '')
        userid = req.userid;
        mailid = req.mailid
        Lobby.MailDel(userid, mailid)
        return json.dumps({'code': 0})
        