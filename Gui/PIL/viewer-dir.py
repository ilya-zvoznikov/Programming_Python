"""
выводит все изображения, найденные в каталоге, открывая новые окна
GIF-файлы поддерживаются стандартными средствами tkinter, но JPEG-файлы будут
пропускаться при отсутствии пакета PIL
"""

import os, sys
from tkinter import *
from PIL.ImageTk import PhotoImage  # <== требуется для JPEG и др. форматов

imgdir = 'images'
if len(sys.argv) > 1: imgdir = sys.argv[1]
imgfiles = os.listdir(imgdir)  # не включает полный путь к каталогу

main = Tk()
main.title('Viewer')
quit = Button(main, text='Quit all', command=main.quit, font=('courier', 25))
quit.pack()
savephotos = []

for imgfile in imgfiles:
    imgpath = os.path.join(imgdir, imgfile)
    win = Toplevel()
    win.title(imgfile)
    try:
        imgobj = PhotoImage(file=imgpath)
        Label(win, image=imgobj).pack()
        print(imgpath, imgobj.width(), imgobj.height())  # размер в пикселях
        savephotos.append(imgobj)  # сохранить ссылку
    except:
        errmsg = 'skipping % s\n % s' % (imgfile, sys.exc_info()[1])
        Label(win, text=errmsg).pack()
