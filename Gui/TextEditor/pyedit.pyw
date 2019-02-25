#!/usr/bin/python
# C:\Users\hp\Desktop\_\prgm\PycharmProjects\untitled\venv\Scripts\python.exe
"""
удобный сценарий для запуска pyedit из произвольного каталога, выполняет
необходимую корректировку пути поиска модулей; sys.path при импортировании
и функции open() требуется передавать путь относительно известного пути
к каталогу со сценарием, а не относительно текущего рабочего каталога, потому
что текущим является каталог сценария, только если сценарий запускается щелчком
на ярлыке, а при вводе команды в командной строке он может находиться в любом
другом каталоге: использует путь из argv; этому файлу дано расширение .pyw,
чтобы подавить вывод окна консоли в Windows; добавьте каталог с этим сценарием
в системную переменную PATH, чтобы иметь возможность запускать его из командной
строки; также может использоваться в Unix: символы / и \ обрабатываются
переносимым образом;
"""

import sys, os

mydir = os.path.dirname(sys.argv[0])  # использовать каталог сценария для open, sys.path

sys.path.insert(1, os.sep.join([mydir] + ['..'] * 3))  # импорт: untitled – корень, 3 уровнями выше
exec(open(os.path.join(mydir, 'textEditor.py')).read())
