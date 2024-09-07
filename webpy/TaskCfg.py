import Config
import ActionCfg

KEY_TASK = "KEY_TASK_{userid}_{date}"

ID_INVALID = -1
ID_SIGN = 20001
ID_SIGN_SEVENDAYS = 20002
ID_PLAY_SERIES_1 = 20003
ID_PLAY_SERIES_2 = 20004
ID_PLAY_SERIES_3 = 20005

TYPE_DAY = 1
TYPE_WEEK = 2
TYPE_MONTH = 3
TYPE_YEAR = 4

TASK_LIST = [
    ID_SIGN,            # 每日签到任务
    ID_SIGN_SEVENDAYS,  # 每周签到任务
    ID_PLAY_SERIES_1,   # 每日对局5场任务 系列一
    ID_PLAY_SERIES_2,   # 每日对局10场任务 系列二
    ID_PLAY_SERIES_3,   # 每日对局20场任务 系列三
]
STATE_INVALID = -1    # 无效状态
STATE_NOT_FINISH = 1  # 未完成状态
STATE_FINISH = 2      # 已完成状态
STATE_AWARDED = 3     # 已领取奖励状态

TASK_CFG = {
    # series: 放的是他的前置任务
    ID_SIGN: {'tid': ID_SIGN, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_SIGN,'iconid': 20001, 'series': ID_INVALID, 'name': "每日签到", 'desc': "每日签到后领取奖励",'count': 1, 'total': 1, 'version':10000,'state': STATE_INVALID,'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}]},
    ID_SIGN_SEVENDAYS: {'tid': ID_SIGN_SEVENDAYS, 'type': TYPE_WEEK, 'action': ActionCfg.ACTION_SIGN ,'iconid': 20002, 'series': ID_INVALID, 'name': "每周签到", 'desc': "签到7天后领取奖励",'count': 1, 'total': 7, 'version':10000,'state': STATE_INVALID, 'rewardlist':[{'id': Config.MONEY_ID, 'num': 10000}]},
    ID_PLAY_SERIES_1: {'tid': ID_PLAY_SERIES_1, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_PALY, 'iconid': 20003, 'series': ID_INVALID, 'name': "每日对局5场", 'desc': "每日对局5场后领取奖励",'count': 1, 'total': 5, 'version':10000,'state': STATE_INVALID, 'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}]},
    ID_PLAY_SERIES_2: {'tid': ID_PLAY_SERIES_2, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_PALY, 'iconid': 20004, 'series': ID_PLAY_SERIES_1, 'name': "每日对局10场", 'desc': "每日对局10场后领取奖励",'count': 1, 'total': 10, 'version':10000,'state': STATE_INVALID, 'rewardlist':[{'id': Config.MONEY_ID, 'num': 2000}]},
    ID_PLAY_SERIES_3: {'tid': ID_PLAY_SERIES_3, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_PALY, 'iconid': 20005, 'series': ID_PLAY_SERIES_2, 'name': "每日对局20场", 'desc': "每日对局20场后领取奖励",'count': 1, 'total': 20, 'version':10000,'state': STATE_INVALID, 'rewardlist':[{'id': Config.MONEY_ID, 'num': 5000}]},
    # 实例 描述一下 ID_PLAY_SERIES_3
    # 任务号是ID_PLAY_SERIES_3、任务类型是每日任务、图标号是20005、必须完成系列2每日对局10场才能开启该任务、任务名是每日对象20场、任务具体描述是每日对局20场后领取奖励、进度是20为满、客户端版本号是10000、奖励列表是奖励5000游戏币
}

SIGN_TYPE_TODAY = 1
SIGN_TYPE_OLD = 2

KEY_SIGN = "KEY_SIGN_{userid}_{date}"