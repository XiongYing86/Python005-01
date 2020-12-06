# Author: chen wei
# Date : 2020-12-06
'''
不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端可以传输单个文件的功能
'''
# 客户端
import socket
import json, os

# 建立json数据，包含文件名以及大小
data = {}
# chuanshufile = os.path.abspath('index.html') # 指定要传输的文件（当前目录下），若要传输当前文件，可以用sys.argv[0]获取
chuanshufile = os.path.abspath('BlueDream_1080.jpg') # 传输图片
# print(chuanshufile)
# csfile = chuanshufile.split('\\')[-1]
# print(csfile)
data['size'] = os.path.getsize(chuanshufile)
# print(data['size'])
name = chuanshufile.split('\\')[-1]
data['name'] = name
jsonString = json.dumps(data).encode('GBK')  # Linux上用utf-8

# print(jsonString)

HOST = 'localhost'
PORT = 10003

# 创建1个socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET:是 IPV4 SOCK_STREAM:TCP协议
s.connect((HOST, PORT))
# 发送文件属性信息
s.send(jsonString)
# 接收服务端发过来的确认信息
s.recv(1024)
# 发送文件数据
size = 0
with open(chuanshufile, 'rb') as f:
    while size < data['size']:
        fileData = f.read(1024)
        s.send(fileData)
        size += 1024
# 关闭连接
s.close()