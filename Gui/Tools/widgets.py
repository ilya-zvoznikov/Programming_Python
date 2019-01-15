"""
##############################################################################
функции-обертки, упрощающие создание виджетов и опирающиеся на некоторые
допущения (например, режим растягивания); используйте словарь **extras
именованных аргументов для передачи таких параметров настройки, как ширина,
шрифт/цвет и других, и повторно компонуйте возвращаемые виджеты, если компоновка
по умолчанию вас не устраивает;
##############################################################################
"""

from tkinter import *

def frame(root, side=TOP, **extras):
    widget = Frame(root)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget

def label(root, side, text, **extras):
    widget = Label(root, text=text, relief=RIDGE)  # настройки по умолчанию
    widget.pack(side=side, expand=YES, fill=BOTH)  # компонуется автоматически
    if extras:
        widget.config(**extras)  # применить все дополнительные параметры
    return widget

def button(root, side, text, command, **extras):
    widget = Button(root, text=text, command=command)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget

def entry(root, side, linkvar, **extras):
    widget = Entry(root, relief=SUNKEN, textvariable=linkvar)
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget


if __name__ == '__main__':
    app = Tk()
    frm = frame(app, TOP)  # программного кода теперь требуется намного меньше!
    label(frm, LEFT, 'SPAM')
    button(frm, BOTTOM, 'Press', lambda: print('Pushed'))
    mainloop()
    
