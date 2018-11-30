"""##############################################################################
Тестирует сценарии Python в каталоге, передает им аргументы командной строки,
выполняет перенаправление stdin, перехватывает stdout, stderr и код завершения,
чтобы определить наличие ошибок и отклонений от предыдущих результатов
выполнения. Запуск сценариев и управление потоками ввода-вывода производится
с помощью переносимого модуля subprocess (как это делает функция os.popen3
в Python 2.X). Потоки ввода-вывода всегда интерпретируются модулем subprocess
как двоичные. Стандартный ввод, аргументы, стандартный вывод и стандартный вывод
ошибок отображаются в файлы, находящиеся в подкаталогах.
Этот сценарий командной строки позволяет указать имя тестируемого каталога
и флаг принудительной генерации выходного файла. Этот программный код можно было
бы упаковать в функцию, однако то обстоятельство, что результатами сценария
являются сообщения и выходные файлы, снижает практическую пользу модели вызов/
возвращаемое значение.
Дополнительные возможные расширения: можно было бы реализовать по несколько
наборов аргументов командной строки и/или входных файлов для каждого
тестируемого сценария и запускать их по несколько раз (использовать функцию glob
для выборки нескольких файлов “.in*” в каталоге Inputs).
Возможно, было бы проще хранить все файлы, необходимые для проведения тестов,
в одном и том же каталоге, но с различными расширениями, однако с течением
времени их объем мог бы оказаться слишком большим.
В случае ошибок можно было бы сохранять содержимое потоков вывода stderr
и stdout в подкаталоге Errors, но я предпочитаю иметь ожидаемый/фактический
вывод в подкаталоге Outputs.
##############################################################################"""

import os, sys, glob, time
from subprocess import Popen, PIPE

# конфигурационные аргументы
testdir = sys.argv[1] if len(sys.argv) > 1 else os.curdir
forcegen = len(sys.argv) > 2
print('Start tester:', time.asctime())
print('in', os.path.abspath(testdir))


def verbose(*args):
    print('-' * 80)
    for arg in args:
        print(arg)


def quiet(*args):
    pass


trace = quiet

# отбор сценариев для тестирования
testpatt = os.path.join(testdir, 'Scripts', '*.py')
testfiles = glob.glob(testpatt)
testfiles.sort()
trace(os.getcwd(), *testfiles)

numfail = 0
for testpath in testfiles:  # протестировать все сценарии
    testname = os.path.basename(testpath)  # отбросить путь к файлу

    # получить входной файл и аргументы для тестируемого сценария
    infile = testname.replace('.py', '.in')
    inpath = os.path.join(testdir, 'Inputs', infile)
    indata = open(inpath, 'rb').read() if os.path.exists(inpath) else b''

    argfile = testname.replace('.py', '.args')
    argpath = os.path.join(testdir, 'Args', argfile)
    argdata = open(argpath).read() if os.path.exists(argpath) else ''

    # местоположение файлов для сохранения stdout и stderr,
    # очистить предыдущие результаты
    outfile = testname.replace('.py', '.out')
    outpath = os.path.join(testdir, 'Outputs', outfile)
    outpathbad = outpath + '.bad'
    if os.path.exists(outpathbad): os.remove(outpathbad)

    errfile = testname.replace('.py', '.err')
    errpath = os.path.join(testdir, 'Errors', errfile)
    if os.path.exists(errpath): os.remove(errpath)

    # запустить тестируемый сценарий, переправив потоки ввода-вывода
    pypath = sys.executable
    command = '%s %s %s' % (pypath, testpath, argdata)
    trace(command, indata)
    process = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.stdin.write(indata)
    process.stdin.close()
    outdata = process.stdout.read()
    errdata = process.stderr.read()
    exitstatus = process.wait()
    trace(outdata, errdata, exitstatus)

    # проанализировать результаты
    if exitstatus != 0:
        print('ERROR status:', testname, exitstatus)  # код заверш. и/или stderr

    if errdata:
        print('ERROR stream:', testname, errpath)  # сохр. текст ошибки
        open(errpath, 'wb').write(errdata)

    if exitstatus or errdata:  # оба признака ошибки
        numfail += 1  # можно получить код завершения + код ошибки
        open(outpathbad, 'wb').write(outdata)  # сохранить вывод
    elif not os.path.exists(outpath) or forcegen:
        print('generating:', outpath)  # создать файл, если
        open(outpath, 'wb').write(outdata)  # необходимо
    else:
        priorout = open(outpath, 'rb').read()  # или сравнить с прежними результатами
        if priorout == outdata:
            print('passed:', testname)
        else:
            numfail += 1
            print('FAILED output:', testname, outpathbad)
            open(outpathbad, 'wb').write(outdata)

print('Finished:', time.asctime())
print(' % s tests were run, % s tests failed.' % (len(testfiles), numfail))
