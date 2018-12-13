from tkinter import *

gifdir = "../gifs/"

win = Tk()
img = PhotoImage(file=gifdir + "ora-lp4e.gif")
can = Canvas(win)
can.pack(fill=BOTH)
can.create_image(20, 20, image=img, anchor=NW)  # координаты x, y
win.mainloop()
