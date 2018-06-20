#-*- coding:utf-8 -*-
#@Time     :2018/6/19 02:26 
#@Author   :Kanseii
#@Emai     :kanseii@yahoo.com
#@File     :server.py
#@Software :PyCharm
import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 5550))

sock.listen(5)
print('Server', socket.gethostbyname('localhost'), 'listening ...')

mydict = dict() #定义字典
mylist = list() #定义列表(元组)


# 把whatToSay传给除了exceptNum的所有人
def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum:
            try:
                c.send(whatToSay.encode())
            except:
                pass


def subThreadIn(myconnection, connNumber):
    nickname = myconnection.recv(1024).decode()
    mydict[myconnection.fileno()] = nickname
    mylist.append(myconnection)
    print('connection', connNumber, ' has nickname :', nickname)
    tellOthers(connNumber, '【系统提示：' + mydict[connNumber] + ' 进入聊天室】')
    while True:
        try:
            recvedMsg = myconnection.recv(1024).decode()
            if recvedMsg:
                print(mydict[connNumber], ':', recvedMsg)
                tellOthers(connNumber, mydict[connNumber] + ' :' + recvedMsg)
                #break
        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            print(mydict[connNumber], 'exit, ', len(mylist), ' person left')
            tellOthers(connNumber, '【系统提示：' + mydict[connNumber] + ' 离开聊天室】')
            myconnection.close()
            return


while True:
    connection, addr = sock.accept()
    print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        # connection.settimeout(5)
        buf = connection.recv(1024).decode()
        if buf == '1':
            connection.send(b'welcome to server!')

            # 为当前连接开辟一个新的线程
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()

        else:
            connection.send(b'please go out!')
            connection.close()
    except:
        pass



