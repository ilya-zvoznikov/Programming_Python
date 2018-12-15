from tkinter import *
from Gui.Tour.menu_win import makemenu

root = Tk()

for i in range(3):
    win = Toplevel(root)
    makemenu(win)
    Label(win,
          text=('Window №%d' % (i + 1)),
          bg='black',
          fg='green',
          font=('system', 40, 'bold'),
          width=15,
          height=5).pack(expand=YES, fill=BOTH)

root.mainloop()
