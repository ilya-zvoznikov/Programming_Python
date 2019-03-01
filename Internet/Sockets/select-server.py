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
