import logging

# 如果不创建记录器和处理器，他会自动创建一个日志级别为WARNING的logger和handler
# logging.debug("无法输出")

# 记录器(笔)
logger = logging.getLogger('dq.zz.applog')

# 记录器设置日志级别
logger.setLevel(logging.DEBUG)

# 处理器(纸)
streamHandler = logging.StreamHandler(stream=None)
fileHandler = logging.FileHandler('demo3.log', mode = 'w')

# 设置处理器的日志级别
streamHandler.setLevel(logging.DEBUG)
fileHandler.setLevel(logging.DEBUG)

# 记录器中添加处理器(笔纸绑定)
logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

# 格式化器
formatter = logging.Formatter(
    "%(asctime)s|%(levelname)-8s|%(filename)-8s|%(lineno)-3s:  %(message)s",
)

# 处理器添加格式化器
streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

# 过滤器
flt = logging.Filter('dq.zz')
streamHandler.addFilter(flt)
# 记录器和处理器都有日志级别最后的日志级别按最严格的级别算 比如DEBUG和WARNING最后级别就是WARNING
logger.debug("你好啊")
logger.debug("你好啊")
logger.debug("你好啊")
logger.debug("你好啊")

