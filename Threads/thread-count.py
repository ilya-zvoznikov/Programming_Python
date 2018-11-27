"""запускает 5 копий функции в параллельных потоках;
функция time.sleep используется, чтобы главный поток не завершился слишком рано,
т.к. на некоторых платформах это приведет к завершению остальных потоков выполнения;
поток вывода std.out - общий;
результаты, выводимые потоками выполнения, могут перемешиваться произвольным образом"""

import _thread as thread, time


def counter(myId, count):
    for i in range(count):
        time.sleep(1)
        print('[%s] => %s' % (myId, i))


for i in range(5):
    thread.start_new_thread(counter, (i, 5))

time.sleep(6)
print('Main thread exiting')
