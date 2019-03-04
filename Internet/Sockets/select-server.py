"""
Сервер: обслуживает параллельно несколько клиентов с помощью select.
Использует модуль select для мультиплексирования в группе сокетов:
главных сокетов, принимающих от клиентов новые запросы на соединение,
и входных сокетов, связанных с клиентами, запрос на соединение от которых
был удовлетворен; вызов select может принимать необязательный 4­й аргумент –
0 означает "опрашивать", число n.m означает "ждать n.m секунд", отсутствие
аргумента означает "ждать готовности к обработке любого сокета".
"""

import sys, time
from select import select
from socket import socket, AF_INET, SOCK_STREAM


def now():
    return time.ctime(time.time())


myHost = ''
myPort = 50007
if len(sys.argv) == 3:  # хост/порт можно указать в командной строке
    myHost, myPort = sys.argv[1:]
numPortSocks = 2  # количество портов для подключения клиентов

# создать главные сокеты для приема новых запросов на соединение от клиентов
mainsocks, readsocks, writesocks = [], [], []
for i in range(numPortSocks):
    portsock = socket(AF_INET, SOCK_STREAM)  # создать объект сокета TCP
    portsock.bind((myHost, myPort))
    portsock.listen(5)
    mainsocks.append(portsock)  # добавить в главный список для идентификации
    readsocks.append(portsock)  # добавить в список источников select
    myPort += 1  # привязка выполняется к смежным портам

# цикл событий: слушать и мультиплексировать, пока процесс не завершится
print('select-server loop starting')

while True:
    # print(readsocks)
    readables, writeables, exceptions = select(readsocks, writesocks, [])
    for sockobj in mainsocks:  # для готовых входных сокетов
        # сокет порта: принять соединение от нового клиента
        newsock, address = sockobj.accept()  # accept не должен блокировать
        print('Connect:', address, id(newsock))  # newsock - новый сокет
        readsocks.append(newsock)  # добавить в список select, ждать
    else:
        # сокет клиента: читать следующую строку
        data = sockobj.recv(1024)  # recv не должен блокировать
        print('\tgot', data, 'on', id(sockobj))
        if not data:  # если закрыто клиентом, закрыть и удалить из списка
            sockobj.close()  # иначе повторно будет обслуживаться вызовом select
            readsocks.remove(sockobj)
        else:
            # может блокировать: в действительности для операции записи
            # тоже следовало бы использовать вызов select
            reply = 'Echo=> %s at %s' % (data, now())
            sockobj.send(reply.encode())
