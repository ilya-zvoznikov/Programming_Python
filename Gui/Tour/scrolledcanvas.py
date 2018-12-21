"""
Простой компонент холста с вертикальной прокруткой
"""

from tkinter import *


class ScrolledCanvas(Frame):
    def __init__(self, parent=None, color='brown'):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        canv = Canvas(self, bg=color, relief=SUNKEN)
        canv.config(width=300, height=200, scrollregion=(0, 0, 1000, 1000), highlightthickness=0)

        xbar = Scrollbar(self)
        xbar.config(command=canv.xview, orient='horizontal')
        canv.config(xscrollcommand=xbar.set)
        xbar.pack(side=BOTTOM, fill=X)

        sbar = Scrollbar(self)
        sbar.config(command=canv.yview)
        canv.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        canv.pack(side=LEFT, expand=YES, fill=BOTH)

        self.fillContent(canv)
        canv.bind('<Double-1>', self.onDoubleClick)
        self.canvas = canv

    def fillContent(self, canv):
        for i in range(10):
            canv.create_text(150, 50 + i * 100, text='spam' + str(i), fill='beige')

    def onDoubleClick(self, event):
        print(event.x, event.y)
        print(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))


if __name__ == '__main__':
    ScrolledCanvas().mainloop()
