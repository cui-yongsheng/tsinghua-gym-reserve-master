import logging

# 既把日志输出到控制台， 还要写入日志文件
class Logger():
    def __init__(self, logname="info", loglevel=logging.DEBUG, loggername=None):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(loglevel)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logname)
        fh.setLevel(loglevel)
        formatter = logging.Formatter('[%(levelname)s]%(asctime)s %(filename)s:%(lineno)d: %(message)s')
        fh.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)

    def getlog(self):
        self.logger.fatal("get logger")
        return self.logger

