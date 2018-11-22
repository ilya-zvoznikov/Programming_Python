from tkinter import *
from tkinter.messagebox import showinfo


def reply(name):
    showinfo(title='Ответ', message='Привет, %s!' % name)


top = Tk()
top.title('Echo')
# top.iconbitmap('py-blue-trans-out.ico')

Label(top, text='Напиши имя').pack(side=TOP)
ent = Entry(top)
ent.pack(side=TOP)
btn = Button(top, text='Нажми кнопку', command=(lambda: reply(ent.get())))
btn.pack(side=LEFT)
top.mainloop()
