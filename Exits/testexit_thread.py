"""порождает потоки выполнения и следит за изменениями в глобальной памяти; обычно
потоки завершаются при возврате из выполняемой в них функции, но поток может
завершиться, вызвав функцию _thread.exit(); функция _thread.exit играет ту
же роль, что и функция sys.exit, и возбуждает исключение SystemExit; потоки
взаимодействуют через глобальные переменные, по мере надобности блокируемые;
ВНИМАНИЕ: на некоторых платформах может потребоваться придать атомарность
вызовам функций print/input -- из-за совместно используемых потоков вводавывода;"""

import _thread as thread

exitstat = 0


def child():
    global exitstat  # используется глобальная переменная процесса,
    exitstat += 1  # совместно используемая всеми потоками
    threadid = thread.get_ident()
    print('Hello from child', threadid, exitstat)
    thread.exit()
    print('never reached')


def parent():
    while True:
        thread.start_new_thread(child, ())
        if input() == 'q':
            break


if __name__ == '__main__':
    parent()
