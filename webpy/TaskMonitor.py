from proto.message_pb2 import Message
from proto.general_pb2 import Sign
import ActionCfg
import Config
import MessageCfg
import TaskCfg
import datetime
import Task

def TaskMonitor():
    while True:
        strKey = ActionCfg.KEY_ACTION_TASK_LIST  # 读任务的消息队列
        res = Config.grds.blpop(strKey)
        msg = Message()
        msg.ParseFromString(res)

        msgid = int(msg.id) & MessageCfg.MSG_ID
        if msgid == MessageCfg.MSG_ID_SIGN:
            signinfo = Sign()
            signinfo.ParseFromString(msg.string)  
            userid = int(signinfo.userid)
            date = signinfo.date

            for id in TaskCfg.TASK_LIST:
                if id not in TaskCfg.TASK_CFG:
                    continue
                cfg = TaskCfg.TASK_CFG[id]
                if cfg['action'] != ActionCfg.ACTION_SIGN:
                        continue
                datestr = datetime.datetime.strptime(str(date), "%Y-%m-%d")
                datestr = Task.GetTaskDatestr(cfg['type'] ,datestr)
                strKey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)
                if not Config.grds.exists(strKey):
                     Task.InitTaskCfg(userid, datestr)
                countfield = 'conut_' + str(id)
                totalfield = 'total_' + str(id)
                statefield = 'state_' + str(id)
                count = Config.grds.hincrby(strKey, countfield, 1)
                total = int(Config.grds.hget(strKey, totalfield))
                state = int(Config.grds.hget(strKey, statefield))

                # 判断任务是否完成
                if count >= total and state == TaskCfg.STATE_NOT_FINISH:
                     Config.grds.hset(strKey, statefield, TaskCfg.STATE_FINISH)

                     # 通知客户端

        elif msgid == MessageCfg.MSG_ID_LOGIN:
             pass

if __name__ == '__main__':
    TaskMonitor()
                     

