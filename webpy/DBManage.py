import Config
import datetime
def InsertRegisterUser(phonenum, password, nick, sex, idcard, now):
    Config.gdb.insert(
        "user",
        userid = int(phonenum),
        password = password,
        secpassword = Config.DEFAULT_SECPASSWORD,
        nick = nick,
        sex = sex,
        idcard = idcard,
        status = Config.USER_STATUS_NORMAL,
        createtime = now,
        lastlogintime = now,
    )

def UpdateUserLastLoginTime(userid, now):
    Config.gdb.update(
        "user",
        lastlogintime = now,
        where = "userid=$userid",
        vars = dict(userid=userid)
    )

def InitPackge(packageinfo):
    result = Config.gdb.insert(
        'package',
        **packageinfo
    )
def ShopBuyUpdatePackage(userid ,money, now):
    Config.gdb.update(
        'package',
        where = 'userid = $userid',
        vars = dict(userid = userid),
        money = money,
        freshtime = now
    )

def UpdateProp(userid, propdict, now):
    propstr = ''
    for k,v in propdict.items():
        propstr += str(k) + '=' + str(v) + ','
    Config.gdb.query("update package set {propstr} freshtime = '{now}' where userid = {userid}".format(propstr = propstr, now = now, userid = userid))