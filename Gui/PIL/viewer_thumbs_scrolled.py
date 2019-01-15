"""
расширенная версия сценария просмотра изображений: отображает миниатюры на
кнопках фиксированного размера, чтобы обеспечить равномерное их размещение,
и добавляет возможность прокрутки при просмотре больших коллекций изображений,
отображая миниатюры в виджете Canvas с полосами прокрутки; требует наличия биб-
лиотеки PIL для отображения изображений в таких форматах, как JPEG, и повторно
использует инструменты создания миниатюр и просмотра единственного изображения из
сценария viewer_thumbs.py; предостережение/что сделать: можно также реализовать
возможность прокрутки при отображении единственного изображения, если его размеры
оказываются больше размеров экрана, которое сейчас обрезается в Windows; более
полная версия представлена в виде приложения PyPhoto в главе 11;
"""

import sys, math
from tkinter import *
from PIL.ImageTk import PhotoImage
from viewer_thumbs import makeThumbs, ViewOne


def viewer(imgdir, kind=Toplevel, numcols=None, height=300, width=300):
    """
    использует кнопки фиксированного размера и холст с возможностью прокрутки;
 определяет размер области прокрутки (всего холста) и располагает
 миниатюры по абсолютным координатам x,y холста; предупреждение:
 предполагается, что все миниатюры имеют одинаковые размеры
    :param imgdir:
    :param kind:
    :param numcols:
    :param height:
    :param width:
    :return:
    """
    win = kind()
    win.title('Simple viewer: ' + imgdir)
    quit = Button(win, text='Quit', command=win.quit, bg='beige')
    quit.pack(side=BOTTOM, fill=X)

    canvas = Canvas(win, borderwidth=0)
    vbar = Scrollbar(win)
    hbar = Scrollbar(win, orient='horizontal')

    vbar.pack(side=RIGHT, fill=Y)
    hbar.pack(side=BOTTOM, fill=X)
    canvas.pack(side=TOP, expand=YES, fill=BOTH)

    vbar.config(command=canvas.yview)
    hbar.config(command=canvas.xview)
    canvas.config(yscrollcommand=vbar.set)
    canvas.config(xscrollcommand=hbar.set)
    canvas.config(height=height, width=width)
    thumbs = makeThumbs(imgdir)
    numthumbs = len(thumbs)
    if not numcols:
        numcols = int(math.ceil(math.sqrt(numthumbs)))
    numrows = int(math.ceil(numthubs / numcols))

    linksize = max(thumbs[0][1].size)
    fullsize = (0, 0,                                # координаты верхнего левого угла
        (linksize * numcols), (linksize * numrows))  # координаты нижнего правого угла
    canvas.config(scrollregion=fullsize)

    rowpos = 0
    savephotos = []

    while thumbs:
        thumbsrow, thumbs = thumbs[:numcols], thumbs[numcols:]
        colpos = 0
        for (imgfile, imgobj) in thumbsrow:
            photo = PhotoImage(imgobj)
            link = Button(canvas, image=photo)
            handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
            link.config(command=handler, width=linksize, height=linksize)
            link.pack(side=LEFT, expand=YES)
            canvas.create_window(colpos, rowpos, anchor=NW, window=link, width=linksize, height=linksize)
            colpos += linksize
            savephotos.append(photo)
        rowpos += linksize
    return win, savephotos

if __name__ == '__main__':
    imgdir = 'images' if len(sys.argv) < 2 else sys.argv[1]
    main, save = viewer(imgdir, kind=Tk)
    main.mainloop()
