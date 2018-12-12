"""
создает модальный диалог с формой;
данные должны извлекаться до уничтожения окна с полями ввода
"""

from tkinter import *
from Gui.Tour.entry2 import makeform, fetch, fields


def show(entries, popup):
    fetch(entries)  # извлечь данные перед уничтожением окна!
    popup.destroy()  # если инструкции поменять местами, сценарий будет возбуждать исключение


def ask():
    popup = Toplevel()
    ents = makeform(popup, fields)
    Button(popup, text='OK', command=(lambda: show(ents, popup))).pack()
    popup.bind('<Return>', (lambda event: show(ents, popup)))
    popup.grab_set()
    popup.focus_set()
    popup.wait_window()


root = Tk()
Button(root, text='Dialog', command=ask).pack()
root.mainloop()
