import TaskCfg
import Config
import datetime
import json
import Lobby
import ErrorCfg
import Shop
from proto.general_pb2 import Sign
import Action
import MessageCfg
# 初始化任务配置
def InitTaskCfg(userid, datestr):
    taskinfo = {}
    
    strKey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)
    
    for tid in TaskCfg.TASK_LIST:
        if tid in TaskCfg.TASK_CFG:
            cfg = TaskCfg.TASK_CFG['tid']
            taskinfo['count_' + str(tid)] = 0
            taskinfo['total_' + str(tid)] = cfg['total']
            taskinfo['state_' + str(tid)] = TaskCfg.STATE_NOT_FINISH
            taskinfo['reward_' + str(tid)] = json.dumps(cfg['rewardlist'])

    Config.grds.hmset(strKey, taskinfo)

# 获取任务配置
def GetTaskCfg(userid, version):
    task = TaskCfg.TASK_LIST
    tasklist = []

    now = datetime.time.now()
    datestr = now.strftime("%Y_%m_%d")

    strKey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)
    
    # 第一次登录 缓存中没有东西 需要去初始化一下任务
    if not Config.grds.exists(strKey):
        InitTaskCfg(userid, datestr)
    
    for tid in task:
        if tid in TaskCfg.TASK_CFG:
            cfg = TaskCfg.TASK_CFG['tid']
            if version < cfg['version']:
                continue
            taskdict = {
                'tid': cfg['tid'], 'type': cfg['type'], 'iconid': cfg['iconid'],
                'series': cfg['series'], 'name': cfg['name'], 'desc': cfg['desc'],
                'total': cfg['total'], 'version': cfg["version"],
                'rewardlist': cfg['rewardlist'],
            }

            '''
            每天的任务不说的 他的过期时间 就是2 3 天就够用
            每周的任务 把他的count统计放在周一 周一过期时间设置2 3 周， 其他的天数设置2 天就可以
            每月的任务 把他的count通知放在1号 后面的一次类推
            '''

            datestr = GetTaskDatestr(cfg['type'], now)
            
            strKey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)
            taskinfo = Config.grds.hgetall(strKey)
            if taskinfo:
                conutfield = 'count_' + str(id)
                statefield = 'state_' + str(id)
                taskdict['count'] = taskinfo[conutfield] 
                taskdict['state'] = taskinfo[statefield]

        tasklist.append(taskdict) 

    return {'tasklist': tasklist}


def GetTaskDatestr(type, today):
    if type == TaskCfg.TYPE_WEEK:
        detestr = Lobby.GetMonday(today)
    elif type == TaskCfg.TYPE_MONTH:
        datestr = str(today.year) + "_" + str(today.month) + '1'
    elif type == TaskCfg.TYPE_YEAR:
        datestr = str(today.year) + "_1_1"
    else:
        datestr = datetime.datetime.strftime(today, "%Y_%m_%d")
    return datestr 

def TaskReward(userid, taskid):  # 任务奖励
    # 判断任务id是否合法
    if taskid not in TaskCfg.TASK_LIST:
        return {'code': ErrorCfg.EC_TASK_ID_INVALID, 'reason': ErrorCfg.ER_TASK_ID_INVALID}

    # 判断用户是否完成任务
    now = datetime.datetime.today()
    cfg = TaskCfg.TASK_CFG['taskid']
    datestr = GetTaskDatestr(cfg['type'], now)
    strKey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)

    statefield = 'state_' + str(taskid)
    state = Config.grds.hget(strKey, statefield)
    if state != TaskCfg.STATE_FINISH:
        return {'code': ErrorCfg.EC_TASK_NOT_FINISTH, 'reason': ErrorCfg.ER_TASK_NOT_FINISTH}
    
    # 发奖励 Present
    rewardfield = 'reward_' + str(taskid)
    rewardlist = Config.grds.hget(strKey, rewardfield)
    rewardlist = json.loads(rewardlist)
    money = 0
    for reward in rewardlist:
        currencytype = reward['id']
        num = reward['num']
        if currencytype == Config.MONEY_ID:
            money += num

    Shop.PresentMoney(userid, money)
    return {'code': 0, 'money': money}

def UserSign(userid, signtype, date):  # 用户签到

    # 先判断签到类型
    if signtype == TaskCfg.SIGN_TYPE_TODAY:  # 如果是当日签到
        date = datetime.datetime.today()
    elif signtype == TaskCfg.SIGN_TYPE_OLD:  # 如果是补签
        date = datetime.datetime.strptime(str(date), "%Y_%m_%d")
    else:
        return {'code': ErrorCfg.EC_TASK_SIGN_TYPE_ERROR, 'reason': ErrorCfg.ER_TASK_SIGN_TYPE_ERROR}
    
            # 位图实际上就是一个32位的数组 哪天签到了就把该位置置为一

    # 签到
    day = date.day
    month = date.month
    year = date.year
    month_firstday = str(year) + '_' + str(date.month) + '_1'
    strKey = TaskCfg.KEY_SIGN.format(userid = userid, date = date.month_firstday)
    Config.grds.setbit(strKey, day, 1)  # 第二个参数是偏置位
            # 比如, 就是设置位图中第 0 个位置的值为 1 Config.grds.setbit(strKey, 0, 1)

    # 发送签到事件

        # 给签到类型的protobuf协议赋值
    signproto = Sign()  
    signproto.userid = userid                   # 指明是哪个用户的签到事件
    signproto.signtype = signtype               # 以及签到的类型 是补签 还是当日签到
    signproto.date = date.strftime("%Y_%m_%d")  # 将日期改为字符串类型
    Action.SendAction(userid, MessageCfg.MSG_ID_SIGN, signproto.SerializeToString())

        
