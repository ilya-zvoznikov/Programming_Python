from tkinter import *
from Gui.Tour.quitter import Quitter


def fetch():
    print('Input => “%s”' % ent.get())
    # ent.delete('0', END)


root = Tk()
ent = Entry(root, show='*')  # от меня: отображать все символы звездочкой (полезно для паролей)
ent.insert(0, 'Type words here')
ent.pack(side=TOP, fill=X)

ent.focus()

ent.bind('<Return>', (lambda event: fetch()))
ent.bind('<Button-1>',
         (lambda event: ent.delete('0', END)))  # от меня: очищать поле при клике мышкой, чтоб руками не удалять
btn = Button(root, text='Fetch', command=fetch)
btn.pack(side=LEFT)
Quitter(root).pack(side=RIGHT)
root.mainloop()
