import logging

# basicConfig函数
logging.basicConfig(filename = 'demo2.log', filemode = 'w', 
    format='%(asctime)-8s|%(levelname)-8s|%(filename)-8s|%(lineno)s:  %(message)s',  # 加一些公共信息和具体的消息
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)  # 公共信息为: 时间 + 日志级别 + 输出到指定文件 + 行号


logging.debug("This is debug log")  # 这是一个DEBUG级别的日志
logging.info("This is info log")  # 这是一个INFO级别的日志
logging.warning("This is warning log")  # 这是一个warning级别的日志
logging.error("This is error log")  # 这是一个ERROR级别的日志
logging.critical("This is critical log")  # 这是一个CRITICAL级别的日志

name = '施易辰'
age = 21
sex = '男'
logging.debug(f"姓名：{name}, 年龄：{age}");
