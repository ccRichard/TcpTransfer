#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2017-1-12 15:54:35
# Author     : cc
# Description: tcp server

import socketserver
import time


class MyTcpServer(socketserver.BaseRequestHandler):

    # 接收文件
    def recv_file(self, filename):
        print('starting recv file: %s' % filename)
        f = open(filename, 'wb')
        self.request.send(b'ready')
        while True:
            data = self.request.recv(4096)
            if data == b'EOF':
                print('recv file: %s success!' % filename)
                break
            f.write(data)
        f.close()
        # 以下写法不行，当文件大于4096的时候会出错，虽然大概能明白，但有空还要再好好理解下
        # self.request.send(b'ready')
        # with open(filename, 'wb') as f:
        #     data = self.request.recv(4096)
        #     if data == b'EOF':
        #         print('recv file: %s success!' % filename)
        #     else:
        #         f.write(data)

    # 发送文件
    def send_file(self, filename):
        print('starting send file: %s' % filename)
        self.request.send(b'ready')
        f = open(filename, 'rb')
        while True:
            data = f.read(4096)
            if not data:
                break
            self.request.sendall(data)
        f.close()

        # with open(filename, 'rb') as f:
        #     data = f.read(4096)
        #     self.request.send(data)

        time.sleep(1)
        self.request.send(b'EOF')
        print('send file: %s success!' % filename)

    # 监听
    def handle(self):
        print('get connection from:', self.client_address)

        # 接收超时
        self.request.settimeout(600)

        while True:
            try:
                data = self.request.recv(4096)
                if not data:
                    print('break this connection! wating for another connection...')
                    break
                else:
                    print('get data from client_cmd: %s' % data)
                    try:
                        action, filename = data.split()
                        if action == b'put':
                            self.recv_file(filename)
                        elif action == b'get':
                            self.send_file(filename)
                        else:
                            print('undefined client_cmd: %s' % data)
                            continue

                    except Exception as e:
                        print('client_cmd error: %s' % str(e))

            except Exception as ex:
                print('server error at: %s' % str(ex))
                break

if __name__ == '__main__':
    host = ''
    port = 60000
    s = socketserver.ThreadingTCPServer((host, port), MyTcpServer)
    s.serve_forever()
