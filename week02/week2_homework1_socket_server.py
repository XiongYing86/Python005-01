# Author: chen wei
# Date : 2020-12-06
'''
不使用开源框架，基于 TCP 协议改造 echo 服务端和客户端代码，实现服务端和客户端可以传输单个文件的功能
'''
# 服务端
import socket
import os, json

HOST = 'localhost'
PORT = 10003

# 创建一个socket对象
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF_INET:IPV4， SOCK_STREAM：TCP协议
# 对象s绑定到指定的地址和端口上
s.bind((HOST, PORT))
# 只接受1个链接
s.listen(1)

# 建立连接
while True:
    # 建立客户端连接
    conn, addr = s.accept()
    print(f'Connect by {addr}')
    # 接收文件属性数据,创建文件
    jsonObj = json.loads(conn.recv(1024).decode('GBK'))  # linux上用 utf-8
    print(f'接收到数据 {jsonObj}')
    # print('接收到数据',jsonObj)
    if not jsonObj:
        os.mknod(jsonObj['name'])
    msg = json.dumps({'name': '消息', '信号': '创建成功'})
    # 回数据确认已经建立新文件
    conn.send(msg.encode('GBK'))
    # 接收数据
    size = 0
    sizeValue = int(jsonObj['size'])
    print('开始接收数据')
    with open(jsonObj['name'], 'wb') as file:
        while size < sizeValue:
            value = sizeValue - size
            if value > 1024:
                getdate = conn.recv(1024)
            else:
                getdate = conn.recv(value)
            file.write(getdate)
            size += 1024
    print('结束')
    # 关闭连接
    conn.close()
