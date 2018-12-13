"""
отображает изображение с помощью стандартного объекта PhotoImage из библиотеки tkinter; данная реализация может работать с GIF-файлами, но не может
обрабатывать изображения в формате JPEG; использует файл с изображением, имя
которого указано в командной строке, или файл по умолчанию; используйте Canvas
вместо Label, чтобы обеспечить возможность прокрутки, и т.д.
"""

import os, sys
from tkinter import *  # использовать стандартный объект PhotoImage

# работает с форматом GIF, а для работы с форматом JPEG
# требуется пакет PIL

imgdir = 'images'
imgfile = 'london-2010.gif'
if len(sys.argv) > 1:  # аргумент командной строки задан?
    imgfile = sys.argv[1]
imgpath = os.path.join(imgdir, imgfile)
win = Tk()
win.title(imgfile)
imgobj = PhotoImage(file=imgpath)
Label(win, image=imgobj).pack()  # прикрепить к метке Label
print(imgobj.width(), imgobj.height())  # вывести размеры в пикселях,
win.mainloop()  # пока объект не уничтожен
