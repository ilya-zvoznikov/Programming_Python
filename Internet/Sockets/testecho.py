import sys
from launchmodes import QuietPortableLauncher

numclients = 8  # количество клиентов для тестирования сервера


def start(cmdline):
    QuietPortableLauncher(cmdline, cmdline)()


# start('echo-server.py')  # запустить сервер локально, если еще не запущен

args = ' '.join(sys.argv[1:])  # передать имя сервера, если он запушен удаленно

for i in range(numclients):
    start('echo-client.py %s' % args)  # запустить 8? клиентов для тестирования сервера
