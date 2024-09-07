# 使用的是redis中的list数据结构 rpush 和 blpop 阻塞式的弹出
KEY_ACTION_LIST = "KEY_ACTION_LIST"

KEY_ACTION_TASK_LIST = "KEY_ACTION_TASK_LIST"  # 任务的消息队列

ACTION_SIGN = 1   # 签到事件
ACTION_LOGIN = 2  # 登录事件
ACTION_PALY = 3   # 对局完成事件

ACTION_MAPPING = {  # 事件分发机制
    ACTION_SIGN: [KEY_ACTION_TASK_LIST],  # 签到事件要分发到任务的消息队列中,
    ACTION_LOGIN: [KEY_ACTION_TASK_LIST],
}