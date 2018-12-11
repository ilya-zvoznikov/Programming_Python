import sys
from tkinter import Toplevel, Button, Label

win1 = Toplevel()
win2 = Toplevel()

Button(win1, text='Spam', command=sys.exit).pack()
Button(win2, text='SPAM', command=sys.exit).pack()

Label(text='Popups').pack()  # по умолчанию добавляется в корневое окно Tk()

win1.mainloop()
