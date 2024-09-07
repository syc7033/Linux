# -*- coding:utf-8 -*-
import logging
import logging.config


# # 实现自己的过滤器
# class LevelFilter(logging.Filter):
#     def __init__(self, level):
#         self.level = level

#     def filter(self, record):
#         return self.level >= logging.WARNING


# 配置文件的方式处理日志
logging.config.fileConfig('logging.conf')

rootLogger = logging.getLogger()
rootLogger.debug("This is a root Logger debug")

logger = logging.getLogger('applog')
logger.debug('This is a applog Logger debug')