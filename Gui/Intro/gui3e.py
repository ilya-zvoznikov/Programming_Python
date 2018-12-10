import sys
from tkinter import *


def hello(event):
    print('Press twice to exit')
    # Label(None, text='Press twice to exit').pack(side=TOP)


def quit(event):
    print('Hello, I must be going...')
    sys.exit()


widget = Button(None, text='Hello event world')
widget.pack()
widget.bind('<Button-1>', hello)
widget.bind('<Double-1>', quit)
widget.mainloop()
