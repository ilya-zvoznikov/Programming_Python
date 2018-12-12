from tkinter import *
from Gui.Tour.quitter import Quitter

root = Tk()
scl = Scale(root, label='Простая шкала', from_=-100, to=100, tickinterval=50, resolution=10)
scl.pack(expand=YES, fill=Y)


def report():
    print(scl.get())


Quitter(root).pack(side=RIGHT)
Button(root, text='State', command=report).pack(side=RIGHT)
root.mainloop()
