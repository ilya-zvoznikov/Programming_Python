"""Отыскивает наибольший файл с исходным программным кодом на языке Python в дереве
каталогов.
Поиск выполняется в каталоге стандартной библиотеки, отображение результатов
выполняется с помощью модуля pprint.

trace - переключатель - выводить или нет все найденные папки и файлы"""

import sys, os, pprint

trace = False
if sys.platform.startswith('win'):
    dirname = r'C:\Users\hp\AppData\Local\Programs\Python\Python37-32\lib'
else:
    dirname = r'/usr/lib/python'

allsizes = []
for (thisDir, subsHere, filesHere) in os.walk(dirname):
    if trace:
        print(thisDir)
    for filename in filesHere:
        if filename.endswith('.py'):
            if trace:
                print('...', filename)
            fullname = os.path.join(thisDir, filename)
            fullsize = os.path.getsize(fullname)
            allsizes.append((fullsize, fullname))

allsizes.sort()
pprint.pprint(allsizes[:2])
pprint.pprint(allsizes[-2:])
