"""
Демонстрация модуля signal; номер сигнала передается в аргументе командной
строки, а отправить сигнал этому процессу можно с помощью команды оболочки
"kill ­N pid"; на моем компьютере с Linux SIGUSR1=10, SIGUSR2=12, SIGCHLD=17
и обработчик SIGCHLD остается действующим, даже если не восстанавливается
в исходное состояние: все остальные обработчики сигналов переустанавливаются
интерпретатором Python после получения сигнала, но поведение сигнала SIGCHLD
не регламентируется и его реализация оставлена за платформой;
модуль signal можно также использовать в Windows, но в ней доступны
лишь несколько типов сигналов; в целом сигналы не очень хорошо переносимы;
"""

import sys, signal, time


def now():
    return time.asctime()


def onSignal(signum, stackframe):  # обработчик сигнала на Python
    print('Got signal', signum, 'at', now())  # большинство обработчиков
    if signum == signal.SIGCHLD:  # не требуется переустанавливать
        print('sigchld caugth')  # кроме обработчика sigchld
        # signal.signal(signal.SIGCHLD, onSignal)


signum = int(sys.argv[1])
signal.signal(signum, onSignal)  # установить обработчик сигнала
while True:
    signal.pause()
