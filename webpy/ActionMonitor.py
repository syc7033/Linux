import ActionCfg
import Config
from proto.message_pb2 import Message
import MessageCfg

def ActionMonitor():
    while True:
        strKey = ActionCfg.KEY_ACTION_LIST
        res = Config.grds.blpop(strKey)
        msg = Message()
        msg.ParseFromString(res)

        # 根据事件分发配置，发送数据
        msgid = int(msg.msgid) & MessageCfg.MSG_ID
        if msgid == MessageCfg.MSG_ID_SIGN:
            for key in ActionCfg.ACTION_MAPPING[ActionCfg.ACTION_SIGN]:
                Config.grds.rpush(key, res)
        elif msgid == MessageCfg.MSG_ID_LOGIN:
            for key in ActionCfg.ACTION_MAPPING[ActionCfg.ACTION_LOGIN]:
                Config.grds.rpush(key, res)

if __name__ == '__main__':
    ActionMonitor()