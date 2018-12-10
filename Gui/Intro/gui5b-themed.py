from tkinter import *


class ThemedButton(Button):  # настраивает стиль
    def __init__(self, parent=None, **configs):  # для всех экземпляров
        Button.__init__(self, parent, **configs)  # описание параметров
        self.pack()  # смотрите в главе 8
        self.config(fg='red', bg='black', font=('courier', 12), relief=RAISED, bd=5)


B1 = ThemedButton(text='spam')
B2 = ThemedButton(text='eggs')
B2.pack(expand=YES, fill=BOTH)
mainloop()
