# Author:chen wei
# Date : 2020-11-29
# 编写一个函数, 当函数被调用时，将调用的时间记录在日志中, 日志文件的保存位置建议为：/var/log/python- 当前日期 /xxxx.log

import logging
import time
import os

# 获取当前的目录
current_dir1 = os.path.dirname(__file__)
# 获取当前的日期
riqi_time = time.strftime("%Y-%m-%d", time.localtime())
# 创建日志文件的上一层目录名称
yiji_mulu = 'python-' + riqi_time
# 获取日志文件所在目录的名称
log_path = '{}/{}'.format(current_dir1, yiji_mulu)
# 判断的路径是否存在，若不存在，再创建目录
if os.path.exists(log_path):
    print("当前日期的目录已经存在！")
else:
    os.mkdir(log_path)

file_path = log_path + '/test1.log'
print(file_path)

logging.basicConfig(filename=file_path,
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(name)-8s %(levelname)-8s [line: %(lineno)d] %(message)s')

# 测试被调用的函数
def test1():
    print("我被调用了")


if __name__ == '__main__':
    test1()
    logging.info('我被调用了 ')
