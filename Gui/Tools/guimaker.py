"""
##############################################################################
Расширенный Frame, автоматически создающий меню и панели инструментов в окне.
GuiMakerFrameMenu предназначен для встраивания компонентов (создает меню на
основе фреймов).
GuiMakerWindowMenu предназначен для окон верхнего уровня (создает меню Tk8.0).
Пример древовидной структуры приводится в реализации самотестирования (и
в PyEdit).
##############################################################################
"""

import sys
from tkinter import *
from tkinter.messagebox import showinfo


class GuiMaker(Frame):
    menuBar = []
    toolBar = []
    helpButton = True  # устанавливать в start()

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.start()
        self.makeMenuBar()
        self.makeToolBar()
        self.makeWidgets()

    def makeMenuBar(self):
        """
        создает полосу меню вверху (реализация меню Tk8.0 приводится ниже)
        expand=no, fill=x, чтобы ширина оставалась постоянной
        :return:
        """
        menubar = Frame(self, relief=RAISED, bd=2)
        menubar.pack(side=TOP, fill=X)

        for (name, key, items) in self.menuBar:
            mbutton = Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self.addMenuItems(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.helpButton:
            Button(menubar, text='Help', cursor='gumby', relief=FLAT, command=self.help).pack(side=RIGHT)

    def addMenuItems(self, menu, items):
        for item in items:
            if item == 'separator':
                menu.add_separator({})
            elif type(item) == list:
                for num in item:
                    menu.entryconfig(num, state=DISABLED)
            elif type(item[2]) != list:
                menu.add_command(label = item[0],
                                 )