"""
##############################################################################
Тест: “python ...\Tools\visitor.py dir testmask [строка]”. Использует
классы и подклассы для сокрытия деталей использования функции os.walk при
обходе и поиске; testmask – битовая маска, каждый бит в которой определяет
тип самопроверки; смотрите также: подклассы visitor_*/.py; вообще подобные
фреймворки должны использовать псевдочастные имена вида __X, однако в данной
реализации все имена экспортируются для использования в подклассах и клиентами;
переопределите метод reset для поддержки множественных, независимых объектовобходчиков, требующих обновлений в подклассах;
##############################################################################
"""

import os, sys


class FileVisitor:
    """
    Выполняет обход всех файлов, не являющихся каталогами, ниже startDir
(по умолчанию '.'); при создании собственных обработчиков
файлов/каталогов переопределяйте методы visit*; аргумент/атрибут context
является необязательным и предназначен для хранения информации,
специфической для подкласса; переключатель режима трассировки trace: 0 -
нет трассировки, 1 - подкаталоги, 2 – добавляются файлы
    """

    def __init__(self, context=None, trace=2):
        self.fcount = 0
        self.dcount = 0
        self.context = context
        self.trace = trace

    def run(self, startDir=os.curdir, reset=True):
        if reset:
            self.reset()
        for (thisDir, dirsHere, filesHere) in os.walk(startDir):
            self.visitdir(thisDir)
            for fname in filesHere:
                fpath = os.path.join(thisDir, fname)  # для некаталогов fname не содержит пути
                self.visitfile(fpath)

    def reset(self):
        self.fcount = self.dcount = 0  # используется обходчиками, выполняющими обход независимо

    def visitdir(self, dirpath):  # вызывается для каждого каталога
        self.dcount += 1  # переопределить или расширить
        if self.trace > 0:
            print(dirpath, '...')

    def visitfile(self, filepath):  # вызывается для каждого файла
        self.fcount += 1  # переопределить или расширить
        if self.trace > 1: print(self.fcount, '=>', filepath)


class SearchVisitor(FileVisitor):
    """
    Выполняет поиск строки в файлах, находящихся в каталоге startDir и ниже;
в подклассах: переопределите метод visitmatch, списки расширений, метод
candidate, если необходимо; подклассы могут использовать testexts, чтобы
определить типы файлов, в которых может выполняться поиск (но могут также
переопределить метод candidate, чтобы использовать модуль mimetypes для
определения файлов с текстовым содержимым: смотрите далее)
    """
    skipexts = []
    testexts = ['.txt', '.py', '.pyw', '.html', '.c', '.h']  # допустимые расш.

    # skipexts = ['.gif', '.jpg', '.pyc', '.o', '.a', '.exe'] # или недопустимые расширения

    def __init__(self, searchkey, trace=2):
        FileVisitor.__init__(self, searchkey, trace)
        self.scount = 0

    def reset(self):  # в независимых обходчиках
        self.scount = 0

    def candidate(self, fname):  # переопределить, если желательно
        ext = os.path.splitext(fname)[1]  # использовать модуль mimetypes
        if self.testexts:
            return ext in self.testexts  # если допустимое расширение
        else:  # или, если недопустимое
            return ext not in self.skipexts  # расширение

    def visitfile(self, fname):  # поиск строки
        FileVisitor.visitfile(self, fname)
        if not self.candidate(fname):
            if self.trace > 0: print('Skipping', fname)
        else:
            text = open(fname).read()  # 'rb' для недекодируемого текста
            if self.context in text:  # или text.find() != -1
                self.visitmatch(fname, text)
                self.scount += 1

    def visitmatch(self, fname, text):  # обработка совпадения
        print('%s has %s' % (fname, self.context))  # переопределить


if __name__ == '__main__':
    # логика самотестирования
    dolist = 1
    dosearch = 2  # 3 = список и поиск
    donext = 4  # при добавлении следующего тест


    def selftest(testmask):
        if testmask & dolist:
            visitor = FileVisitor(trace=2)
            visitor.run(sys.argv[2])
            print('Visited %d files and %d dirs' % (visitor.fcount, visitor.dcount))
        if testmask & dosearch:
            visitor = SearchVisitor(sys.argv[3], trace=0)
            visitor.run(sys.argv[2])
            print('Found in %d files, visited %d' % (visitor.scount, visitor.fcount))


    selftest(int(sys.argv[1]))  # например, 3 = dolist | dosearch
