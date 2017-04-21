#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2017-1-12 15:24:21
# Author     : cc
# Description: tcp client

import socket
import time
import sys
import os


class MyTcpClient:
    def __init__(self, ip='127.0.0.1', port=60000):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Prepare for connecting...')

    # socket连接
    def connect(self):
        self.socket.connect((self.ip, self.port))

    # 接收文件
    def recv_file(self, filename):
        print('starting recv file: %s' % filename)

        f = open(filename, 'wb')
        while True:
            data = self.socket.recv(4096)
            if data == b'EOF':
                print('recv file: %s success!' % filename)
                break
            f.write(data)
        f.close()
        # 错误写法，待查
        # with open(filename, 'wb') as f:
        #     data = self.socket.recv(4096)
        #     if data == b'EOF':
        #         print('recv file: %s success!' % filename)
        #     else:
        #         f.write(data)

    # 发送文件
    def send_file(self, filename):
        print('starting send file: %s' % filename)

        f = open(filename, 'rb')
        while True:
            data = f.read(4096)
            if not data:
                break
            self.socket.sendall(data)
        f.close()
        # 错误的写法，有空再想想
        # with open(filename, 'rb') as f:
        #     data = f.read(4096)
        #     self.socket.sendall(data)

        time.sleep(1)
        self.socket.send(b'EOF')
        print('send file: %s success!' % filename)

    # 与服务端通信，判断是否连接
    def confirm(self, client_cmd):
        self.socket.send(bytes(client_cmd, 'utf-8'))
        print('talk to server: %s' % client_cmd)
        data = self.socket.recv(4096)
        if data == b'ready':
            return True

    # 主动断开与服务端的连接
    def exit(self):
        self.socket.close()


# 发送文件接口
def put_file(filename, ip='127.0.0.1', port=60000):
    if not os.path.exists(filename):
        print('%s:file is not exists' % filename)
        return False

    client = MyTcpClient(ip, port)
    client.connect()
    if client.confirm('put %s' % filename):
        client.send_file(filename)
        client.exit()
        return True
    else:
        print('server get error!')
        client.exit()
        return False


# 获取文件接口
def get_file(filename, ip='127.0.0.1', port=60000):
    client = MyTcpClient(ip, port)
    client.connect()
    if client.confirm('get %s' % filename):
        client.recv_file(filename)
        client.exit()
        return True
    else:
        print('server get error!')
        client.exit()
        return False


# 命令行模式
def main(ip='127.0.0.1', port=60000):
    client = MyTcpClient(ip, port)
    client.connect()
    while True:
        client_cmd = input('>>')
        if not client_cmd:
            continue
        try:
            action, filename = client_cmd.split()
            if action == 'put':
                if client.confirm(client_cmd):
                    client.send_file(filename)
                else:
                    print('server get error!')
            elif action == 'get':
                if client.confirm(client_cmd):
                    client.recv_file(filename)
                else:
                    print('server get error!')
            elif action == 'exit':
                client.exit()
                break
            else:
                print('undefined client_cmd: %s' % client_cmd)
        except Exception as e:
            print('client_cmd error: %s' % str(e))


if __name__ == '__main__':
    main('172.20.232.1')
    #put_file('test.png')





