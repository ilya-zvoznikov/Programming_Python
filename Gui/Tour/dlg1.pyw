from tkinter import *
from tkinter.messagebox import *


def callback():
    if askyesno('Verify', 'Do you really want to quit?'):
        showwarning('Yes', 'Quit not yet implemented')
    else:
        showinfo('No', 'Quit has been canceled')


errmsg = 'Sorry, no Spam allowed!'
Button(text='Spam', command=(lambda: showerror('Spam', errmsg))).pack(fill=X)
Button(text='Quit', command=callback).pack(fill=X)
mainloop()
