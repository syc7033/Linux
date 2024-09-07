from proto.message_pb2 import Message
import ActionCfg
import Config

def SendAction(userid, msgid, protoinfo):
    strKey = ActionCfg.KEY_ACTION_LIST

    # 给protobuf协议赋值
    msg = Message()
    msg.userid = userid
    msg.msgid = msgid
    msg.string = protoinfo
    Config.grds.rpush(strKey, msg.SerializeToString())