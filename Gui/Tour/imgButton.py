from tkinter import *

gifdir = "../gifs/"

win = Tk()
img = PhotoImage(file=gifdir + "pythonwin.gif")
Button(win, image=img).pack()
win.mainloop()
