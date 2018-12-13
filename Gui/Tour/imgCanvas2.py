gifdir = "../gifs/"
from tkinter import *
from sys import argv

filename = argv[1] if len(argv) > 1 else 'ora-lp4e.gif'  # имя файла в командной строке
win = Tk()
img = PhotoImage(file=gifdir + filename)
can = Canvas(win)
can.pack(fill=BOTH)
can.config(width=img.width(), height=img.height())
can.create_image(2, 2, image=img, anchor=NW)
win.mainloop()
