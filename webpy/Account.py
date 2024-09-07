import Config
import datetime
import DBManage
import ErrorCfg

# 检测手机号是否合理
def CheckPhonenum(phonenum):
    # 1.通过号段列表判断
    phoneList = [134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 182, 183, 184, 187, 188, 198,
            130, 131, 132, 145, 155, 156, 166, 171, 175, 176, 185, 186,
            133, 149, 153, 173, 177, 180, 181, 189, 199,
            170, 171, 172]
    # print(len(phonenum))
    # print(str(phonenum).isdigit)
    # print(phonenum[:3])    
    # print(phonenum[:3] in phoneList)
    if len(phonenum) == 11 and str(phonenum).isdigit and int(phonenum[:3]) in phoneList:
        return True
    else:
        return False

# 检测手机号是否重复
def CheckPhonenumRepeat(userid):
    ret = Config.gdb.query("select count(*) as num from user where userid = {}".format(userid))
    if ret and ret[0].num >= 1:
        return True
    
    return False


# 检测身份证号
def CheckIdCard(idcard):
    """
    检查身份证号码是否合理
    
    参数:
    idcard (str): 18位身份证号码
    
    返回:
    bool: True 表示身份证号码合理, False 表示身份证号码不合理
    """
    # 检查长度是否为18位
    if len(idcard) != 18:
        return False

    # 检查前17位是否全部为数字
    if not idcard[:17].isdigit():
        return False

    # 计算校验码
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_sum = sum([int(idcard[i]) * factors[i] for i in range(17)]) % 11
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    if idcard[17] != check_codes[check_sum]:
        return False

    # 检查出生日期是否合法
    try:
        year = int(idcard[6:10])
        month = int(idcard[10:12])
        day = int(idcard[12:14])
        if year < 1900 or year > 2100 or month < 1 or month > 12 or day < 1 or day > 31:
            return False
    except ValueError:
        return False
    return True

# 检测密码格式
import re

def CheckPwd(password):
    # 密码长度检查
    if len(password) < 8 or len(password) > 16:
        return False
    
    # 密码只能包含字母和数字
    if not re.match(r'^[a-zA-Z0-9]+$', password):
        return False
    
    return True



def InitPackage(userid, now):
    strKey = Config.KEY_PACKAGE.format(userid = userid)
    # 背包中的信息属于热点数据 需要存在redis缓存中 提高数据库的效率
    if Config.grds.exists(strKey):
        return
    else:
        result = Config.gdb.select(
            'package',
            what = '*',
            where = 'userid=$userid',
            vars = dict(userid = userid)
        )
        if result:
            packageinfo = {}
            for k, v in result[0].items():
                packageinfo[k] = v
            Config.grds.hmset(strKey, packageinfo)
        else:
            packageinfo = {
                'userid': userid,
                'money': Config.NEWUSER_DEFAULT_MONEY,
                'coin': 0,
                'prop_1001': 0,
                'prop_1002': 0,
                'prop_1003': 0,
                'prop_1006': 0,
                'prop_1007': 0,
                'freshtime': str(now),
            } 
            DBManage.InitPackge(packageinfo)
            Config.grds.hmset(strKey,packageinfo)
            Config.grds.expire(strKey, 30 * 24 * 60 * 60)
    

def InitUser(phonenum, password, nick, sex, idcard):
    now = datetime.datetime.now()
    print("now", now)
    DBManage.InsertRegisterUser(phonenum, password, nick, sex, idcard, now)
    # 初始化背包
    InitPackage(phonenum, now)

def VerifyAcconut(userid, password):
    result = Config.gdb.select(
        "user",
        what = "password",
        where = "userid=$userid",
        vars = dict(userid=userid)
    )
    print(result)
    # 如果没有密码
    if not result:
        return {'code':ErrorCfg.EC_LOGIN_USERID_ERROR, 'reason':ErrorCfg.ER_LOGIN_USERID_ERROR}

    # 有密码看是否正确
    if result[0]['password'] != password:
        return {'code':ErrorCfg.EC_LOGIN_PASSWORD_ERROR, 'reason':ErrorCfg.ER_LOGIN_PASSWORD_ERROR}
    # 登录成功
    return {'code':0}

def HandleLogin(userid, session):
    now = datetime.datetime.now()

    logininfo = {
        'freshtime': str(now)
    }
    Config.grds.hmset(Config.KEY_LOGIN.format(userid = userid), logininfo)
    Config.grds.expire(Config.KEY_LOGIN.format(userid = userid), Config.LOGIN_EXPIRETIME)
    Config.grds.expire(Config.KEY_PACKAGE.format(userid = userid), Config.LOGIN_EXPIRETIME)
    session['userid'] = userid
    DBManage.UpdateUserLastLoginTime(userid, now)
    return {'code': 0}