"""
То же, что и fork-server.py, но использует модуль signal, чтобы обеспечить
автоматическое удаление дочерних процессов-зомби после их завершения вместо
явного удаления перед приемом каждого нового соединения; действие SIG_IGN
означает игнорирование и может действовать с сигналом SIGCHLD завершения
дочерних процессов не на всех платформах; смотрите документацию
к операционной системе Linux, где описывается возможность перезапуска
вызова socket.accept, прерванного сигналом;
"""

import os, time, sys, signal
from socket import *

myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)
signal.signal(signal.SIGCHLD, signal.SIG_IGN)


def now():
    return time.ctime(time.time())


def handleClient(connection):
    time.sleep(5)
    while True:
        data = connection.recv(1024)
        if not data:
            break
        reply = 'Echo=> %s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()
    os._exit(0)


def dispatcher():
    while True:
        connection, address = sockobj.accept()
        print('Server connected by', address, 'at', now())
        childpid = os.fork()
        if childpid == 0:
            handleClient(connection)


dispatcher()
