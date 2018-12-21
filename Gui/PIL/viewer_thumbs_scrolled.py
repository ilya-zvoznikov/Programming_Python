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
from Gui.PIL.viewer_thumbs import makeThumbs, ViewOne


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

# ПРОГРАММА НЕ ЗАКОНЧЕНА!!!
