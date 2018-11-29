"""Отыскивает наибольший файл с исходным программным кодом на языке Python,
присутствующий в пути поиска модулей.
Пропускает каталоги, которые уже были просканированы; нормализует пути и регистр
символов, обеспечивая корректность сравнения; включает в выводимые результаты
счетчики строк. Здесь недостаточно использовать os.environ[‘PYTHONPATH’]:
этот список является лишь подмножеством списка sys.path."""

import sys, os, pprint

trace = 0  # 1=каталоги, 2=+файлы

visited = {}
allsizes = []

for srcdir in sys.path:
    for (thisDir, sunsHere, filesHere) in os.walk(srcdir):
        if trace > 0:
            print(thisDir)
        thisDir = os.path.normpath(thisDir)
        fixcase = os.path.normcase(thisDir)
        if fixcase in visited:
            continue
        else:
            visited[fixcase] = True
        for filename in filesHere:
            if filename.endswith('.py'):
                if trace > 1:
                    print('...', filename)
                pypath = os.path.join(thisDir, filename)
                try:
                    pysize = os.path.getsize(pypath)
                except os.error:
                    print('skipping', pypath, sys.exc_info()[0])
                else:
                    pylines = len(open(pypath, 'rb').readlines())
                    allsizes.append((pysize, pylines, pypath))

print('By size...')
allsizes.sort()
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])
print('By lines...')
allsizes.sort(key=lambda x: x[1])
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])
