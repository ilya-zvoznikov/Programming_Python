"""
На стороне сервера: открывает сокет с указанным номером порта, ожидает
появления сообщения от клиента и отправляет это же сообщение обратно;
продолжает возвращать сообщения клиенту, пока не будет получен признак eof
при закрытии сокета на стороне клиента; для обслуживания клиентов порождает
дочерние потоки выполнения; потоки используют глобальную память совместно
с главным потоком; этот прием является более переносимым, чем ветвление:
потоки выполнения действуют в стандартных версиях Python для Windows,
тогда как прием ветвления - нет.
"""

import time, _thread as thread  # или использовать threading.Thread().start()
from socket import *

myHost = ''
myPort = 50007

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.bind((myHost, myPort))
sockobj.listen(5)


def now():
    return time.ctime(time.time())


def handleClient(connection, address):
    time.sleep(5)
    while True:
        data = connection.recv(1024)
        if not data:
            break
        reply = 'Echo=> %s at %s' % (data, now())
        connection.send(reply.encode())
    connection.close()
    print('Server disconnected by', address, 'at', now())


def dispatcher():
    while True:
        connection, address = sockobj.accept()
        print('Server connected by', address, 'at', now())
        thread.start_new_thread(handleClient, (connection, address))


dispatcher()
