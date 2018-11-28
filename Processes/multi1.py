"""основы применения пакета multiprocessing: класс Process по своему действию
напоминает класс threading.Thread, но выполняет функцию в отдельном процессе,
а не в потоке; для синхронизации можно использовать блокировки, например, для
вывода текста; запускает новый процесс интерпретатора в Windows, порождает
дочерний процесс в Unix;"""

import os
from multiprocessing import Process, Lock


def whoami(label, lock):
    msg = '%s: name:%s, pid:%s'
    with lock:
        print(msg % (label, __name__, os.getpid()))


if __name__ == '__main__':
    lock = Lock()
    whoami('function lock', lock)

    p = Process(target=whoami, args=('spawn child', lock))
    p.start()
    p.join()

    for i in range(5):
        Process(target=whoami, args=(('run process %s' % i), lock)).start()

    with lock:
        print('Main process exiting')
