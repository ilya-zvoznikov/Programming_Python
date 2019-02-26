"""
На стороне сервера: открывает сокет на указанном порту, ожидает
поступления сообщения от клиента и отправляет его обратно; порождает
дочерний процесс для обслуживания каждого соединения с клиентом;
дочерние процессы совместно используют дескрипторы родительских сокетов;
прием ветвления процессов менее переносим, чем прием на основе потоков выполнения, -
он не поддерживается в Windows, если не используется Cygwin или
подобная ей оболочка;
"""

import os, time, sys
from socket import *  # получить конструктор сокетов и константы

myHost = ''  # компьютер­сервер, '' означает локальный хост
myPort = 50007  # использовать незарезервированный номер порта

sockobj = socket(AF_INET, SOCK_STREAM)  # создать объект сокета TCP
sockobj.bind((myHost, myPort))  # связать с номером порта сервера
sockobj.listen(5)  # не более 5 ожидающих запросов


def now():  # текущее время на сервере
    return time.ctime(time.time())


activeChildren = []


def reapChildren():  # убрать завершившиеся дочерние процессы
    while activeChildren:  # иначе может переполниться системная таблица
        pid, stat = os.waitpid(0, os.WNOHANG)  # не блокировать сервер, если дочерний процесс не завершился
        if not pid:
            break
        activeChildren.remove(pid)


def handleClient(connection):  # дочерний процесс: ответить, выйти
    time.sleep(5)  # имитировать блокирующие действия
    while True:  # чтение, запись в сокет клиента до получения признака eof, когда сокет будет закрыт клиентом
        data = connection.recv(1024)
        if not data:
            break
        reply = 'Echo=>%s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()
    os._exit(0)


def dispatcher():  # пока процесс работает
    while True:  # ждать запроса очередного клиента
        connection, address = sockobj.accept()  # передать процессу для обслуживания
        print('Server connected by', address, 'at', now())
        reapChildren()  # теперь убрать завершившиеся потомки
        childPid = os.fork()  # копировать этот процесс
        if childPid == 0:  # в дочернем процессе: обслужить
            handleClient(connection)
        else:  # иначе: ждать следующего запроса
            activeChildren.append(childPid)  # добавить с список активных потомков


dispatcher()
