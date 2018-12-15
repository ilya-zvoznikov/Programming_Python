"""
использует кнопки фиксированного размера для миниатюр, благодаря чему
достигается еще более стройное размещение; размеры определяются по объектам
изображений, при этом предполагается, что для всех миниатюр был установлен один
и тот же максимальный размер; по сути именно это и делают графические интерфейсы
файловых менеджеров;
"""

import os, sys, math
from tkinter import *
from PIL import Image  # для миниатюр
from PIL.ImageTk import PhotoImage  # для полноразмерных JPEG


def makeThumbs(imgdir, size=(100, 100), subdir='thumbs'):
    """
    создает миниатюры для всех изображений в каталоге; для каждого изображения
создается и сохраняется новая миниатюра или загружается существующая;
при необходимости создает каталог thumb;
возвращает список кортежей (имя_файла_изображения, объект_миниатюры);
для получения списка файлов миниатюр вызывающая программа может также
воспользоваться функцией listdir в каталоге thumb; для неподдерживаемых
типов файлов может возбуждать исключение IOError, или другое;
ВНИМАНИЕ: можно было бы проверять время создания файлов;
    :param imgdir:
    :param size:
    :param subdir:
    :return thumbs:
    """

    thumbdir = os.path.join(imgdir, subdir)
    if not os.path.exists(thumbdir):
        os.mkdir(thumbdir)

    thumbs = []
    for imgfile in os.listdir(imgdir):
        thumbpath = os.path.join(thumbdir, imgfile)
        if os.path.exists(thumbpath):
            thumbobj = Image.open(thumbpath)
            thumbs.append((imgfile, thumbobj))
        else:
            print('making', thumbpath)
            imgpath = os.path.join(imgdir, imgfile)
            try:
                imgobj = Image.open(imgpath)
                imgobj.thumbnail(size, Image.ANTIALIAS)
                imgobj.save(thumbpath)
                thumbs.append((imgfile, imgobj))
            except:
                print('Skipping', imgpath)

    return thumbs


class ViewOne(Toplevel):
    """
    открывает одно изображение в новом окне; ссылку на объект PhotoImage
требуется сохранить: изображение будет утрачено при утилизации объекта;
    """

    def __init__(self, imgdir, imgfile):
        Toplevel.__init__(self)
        self.title(imgfile)
        imgpath = os.path.join(imgdir, imgfile)
        imgobj = PhotoImage(file=imgpath)
        Label(self, image=imgobj).pack()
        print(imgpath, imgobj.width(), imgobj.height())
        self.savephoto = imgobj


def viewer(imgdir, kind=Toplevel, cols=None):
    """
    создает окно с миниатюрами для каталога с изображениями: по одной кнопке с
миниатюрой для каждого изображения;
используйте параметр kind=Tk, чтобы вывести миниатюры в главном окне, или
Frame (чтобы прикрепить к фрейму); значение imgfile изменяется в каждой
итерации цикла: ссылка на значение должна сохраняться по умолчанию;
объекты PhotoImage должны сохраняться: иначе при утилизации изображения
будут уничтожены;
компонует в ряды фреймов (в противоположность сеткам, фиксированным
размерам, холстам);
    :param imgdir:
    :param kind:
    :param cols:
    :return win, savephotos:
    """

    win = kind()
    win.title('Viewer:' + imgdir)
    quit = Button(win, text='Qiut', command=win.quit, bg='beige')
    quit.pack(fill=X, side=BOTTOM)
    thumbs = makeThumbs(imgdir)
    if not cols:
        cols = int(math.ceil(math.sqrt(len(thumbs))))
    savephotos = []

    while thumbs:
        thumbsrow, thumbs = thumbs[:cols], thumbs[cols:]
        row = Frame(win)
        row.pack(fill=BOTH)
        for (imgfile, imgobj) in thumbsrow:
            size = max(imgobj.size)
            photo = PhotoImage(imgobj)
            link = Button(row, image=photo)
            handler = lambda savefile=imgfile: ViewOne(imgdir, savefile)
            link.config(command=handler, width=size, height=size)
            link.pack(side=LEFT, expand=YES)
            savephotos.append(photo)
    return win, savephotos


if __name__ == '__main__':
    imgdir = (len(sys.argv) > 1 and sys.argv[1]) or 'images'
    main, save = viewer(imgdir, kind=Tk)
    main.mainloop()
