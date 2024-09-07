import logging

# 1.获取记录器
logger = logging.getLogger('applog')  # 应用框架的记录器

# 2.设置记录器日志级别
logger.setLevel(logging.DEBUG)

# 3.获取处理器
consoleHandler = logging.StreamHandler(stream=None)  # 输出到控制台（屏幕上）
# fh = logging.FileHandler()  # 输出到磁盘（文件中）

# 4.给记录器添加处理器
logger.addHandler(consoleHandler)

# 5.创建格式化器
formatter = logging.Formatter(
    "%(asctime)s|%(levelname)-8s|%(filename)s|%(lineno)s:     %(message)s"
)

# 6.给处理器添加格式化器
consoleHandler.setFormatter(formatter)

# 设置处理器日志级别
consoleHandler.setLevel(logging.WARNING)

logger.debug("fsdkafjlsd")
