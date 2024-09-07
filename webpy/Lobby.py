import Config
import datetime
from proto.general_pb2 import Mail
import json
import Service
def GetMoney(userid):
    strKey = Config.KEY_PACKAGE.foramt(userid = userid)
    money = 0
    if Config.grds.exists(strKey):
        money = int(Config.grds.get(strKey, 'money'))
    else:
        result = Config.gdb.select('packge', what='*', where = 'userid=$userid', vars = dict(userid=userid))
        if result:
            packageinfo = {
                'userid': userid,
                'money': result[0]['money'],
                'coin': result[0]['coin'],
                'prop_1001': result[0]['prop_1001'],
                'prop_1002': result[0]['prop_1002'],
                'prop_1003': result[0]['prop_1003'],
                'prop_1006': result[0]['prop_1006'],
                'prop_1007': result[0]['prop_1007'],
                'freshtime': result[0]['freshtime'],
            }
            Config.grds.hmset(strKey, packageinfo)
            Config.grds.expire(strKey, 30 * 24 * 60 * 60)
            money = int(result[0]['money'])
    return money

def GetMonday(today):
    today = datetime.datetime.strptime(str(today), "%Y-%m-%d")
    return datetime.datetime.strftime(today - datetime.timedelta(today.weekday(), "%Y_%m_%d"))
        
            
def SendMail(mailinfo):
    if not mailinfo:
        pass

    mailproto = Mail()
    for id in mailinfo['useridlist']:
        mailproto.userid.append(id)
    mailproto.title = mailinfo['title']
    mailproto.type = mailinfo['type']
    mailproto.context = mailinfo['context']
    mailproto.title = mailinfo['title']
    mailproto.title = mailinfo['title']
    attach = {}
    for k, v in mailinfo['attach'].items():
        attach[k] = v
    mailproto.attach = json.dumps(attach)
    mailproto['getattach'] = 0
    mailproto['hasaatch'] = 0
    if attach:
        mailproto['hasattach'] = 1

    # 发送给邮件服务器
    Service.SendSvrd('ip', 8080, mailproto.SerializeToString())

def GetMailList(userid):
    # 拼邮件列表的key
    strKeyList = Config.KEY_LOGIN.format(userid = userid)
    mailIdList = Config.grds.lrange(strKeyList, 0, -1)
    mailList = []
    for mailId in mailIdList:
        strKey = Config.KEY_MAIL_DETAIL.format(mailid = mailId)
        result = Config.grds.hgetall(strKey)
        if not result:
            Config.grds.lrem(strKeyList, mailId, 0)
            continue

        mailinfo = {}
        mailinfo['mailid'] = mailId
        mailinfo['title'] = result['title']
        mailinfo['type'] = result['type']
        mailinfo['getattach'] = result['getattach']
        mailinfo['context'] = result['context']
        mailList.append(mailinfo)
    return mailList

def MailDel(userid, mailid):
    strKeyList = Config.KEY_MAIL_LIST.format(userid = userid)
    Config.grds.lrem(strKeyList, mailid, 0)
    strKey = Config.KEY_MAIL_DETAIL.format(mailid = mailid)
    Config.grds.delete(strKey)

def MailDelAll(userid):
    strKeyList = Config.KEY_MAIL_LIST.format(userid = userid)
    mailidlist = Config.grds.lrange(strKeyList, 0, -1)
    for mailid in mailidlist:
        Config.grds.lrem(strKeyList, mailid, 0)
        strKey = Config.KEY_MAIL_DETAIL.format(mailid)
        Config.grds.delete(strKey)
    return {'code': 0}