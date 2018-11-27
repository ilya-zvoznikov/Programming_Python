"""экземпляры класса Thread, сохраняющие информацию о состоянии и обладающие
методом run() для запуска потоков выполнения; в реализации используется
высокоуровневый и Java-подобный метод join класса Thread модуля threading
(вместо мьютексов и глобальных переменных), чтобы известить главный родительский
поток о завершении дочерних потоков; подробности о модуле threading ищите
в руководстве по стандартной биб­лиотеке;"""

import threading


class MyThread(threading.Thread):
    def __init__(self, myId, count, mutex):
        self.myId = myId
        self.count = count
        self.mutex = mutex
        threading.Thread.__init__(self)

    def run(self):
        for i in range(self.count):
            with self.mutex:
                print('[%s] => %s' % (self.myId, i))


stdoutmutex = threading.Lock()
threads = []
for i in range(10):
    thread = MyThread(i, 100, stdoutmutex)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
print('Main thread exiting')
