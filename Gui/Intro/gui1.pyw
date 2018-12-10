from tkinter import *  # импортировать виджет

root = Tk()
widget = Label(root)  # создать его
widget.config(text='Hello GUI world!')
widget.pack(side=TOP, expand=YES, fill=BOTH)
root.title('gui.py')
root.mainloop()  # запустить цикл событий
