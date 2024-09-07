import web
import redis

# 连接数据库

DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'root'
DB_PWD = '123456'
DB_NAME = 'game_test'

gdb = web.database(
    dbn = 'mysql',
    host = DB_HOST,
    port = DB_PORT,
    user = DB_USER,
    pw = DB_PWD,
    db = DB_NAME
)

RDS_HOST = '127.0.0.1'
RDS_PORT = 6379
RDS_PASSWORD = '123456'

NEWUSER_DEFAULT_MONEY = 10000



grds = redis.Redis(
    host = RDS_HOST,
    port = RDS_PORT,
    password = RDS_PASSWORD
)
# grds.set('name', 'zhangsan')

DEFAULT_SECPASSWORD = '123456'


USER_STATUS_NORMAL = 0
USER_STATUS_FREEZE = 1

# 账号
KEY_PACKAGE = "KEY_PACKAGE_{userid}"
KEY_LOGIN = "KEY_LOGIN_{userid}"

# 过期时间
SESSION_EXPIRETIME = 30
LOGIN_EXPIRETIME = 30

# 货币号
MONEY_ID = 800
COIN_ID = 900

# 邮件
KEY_MAIL_LIST = "KEY_MAIL_LIST_{userid}" 
KEY_MAIL_DETAIL = "KEY_MAIL_DETAIL_{mailid}"