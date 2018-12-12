"""
4 демонстрационных класса, выполняемых как независимые процессы: команды;
если теперь одно окно будет завершено щелчком на кнопке Quit, остальные
продолжат работу; в данном случае не существует простого способа вызвать все
методы report (впрочем, для организации взаимодействий между процессами можно
было бы воспользоваться сокетами и каналами), а кроме того, некоторые способы
запуска могут сбрасывать поток stdout дочерних программ и разрывать связь между
родителем и потомком;
"""

from tkinter import *
from launchmodes import PortableLauncher

demoModules = ['demoDlg', 'demoRadio', 'demoCheck', 'demoScale']

for demo in demoModules:
    PortableLauncher(demo, demo + '.py')()

root = Tk()
root.title('Processes')
Label(root, text='Multiple program demo: command lines', bg='white').pack()
root.mainloop()
