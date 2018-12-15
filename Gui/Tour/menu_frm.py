"""
Меню на основе фреймов: пригодно для окон верхнего уровня и компонентов
"""

from tkinter import *
from tkinter.messagebox import *


def notedone():
    showerror('Not implemented', 'Not yet available')


def makemenu(parent):
    menubar = Frame(parent)
    menubar.pack(side=TOP, fill=X)

    fbutton = Menubutton(menubar, text='File', underline=0)


    file = Menu(top, tearoff=False)
    top.add_cascade(label='File', menu=file, underline=0)
    file.add_command(label='New...', command=notedone, underline=0)
    file.add_command(label='Open...', command=notedone, underline=0)
    file.add_command(label='Quit', command=win.quit, underline=0)

    edit = Menu(top, tearoff=False)
    top.add_cascade(label='Edit', menu=edit, underline=0)
    edit.add_command(label='Cut', command=notedone, underline=0)
    edit.add_command(label='Paste', command=notedone, underline=0)
    edit.add_separator()

    submenu = Menu(edit, tearoff=True)
    edit.add_cascade(label='Stuff', menu=submenu, underline=0)
    submenu.add_command(label='Spam', command=notedone, underline=0)
    submenu.add_command(label='YAQuit', command=win.quit, underline=0)


if __name__ == '__main__':
    root = Tk()
    root.title('menu_win')
    makemenu(root)
    msg = Label(root, text='Window menu basics')  # добавить что-нибудь ниже
    msg.pack(expand=YES, fill=BOTH)
    msg.config(relief=SUNKEN, width=40, height=7, bg='beige')
    root.mainloop()
