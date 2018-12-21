from tkinter import *


def tkprinter(widgetname, full=False, width=28):
    print()
    print('WIDGET NAME: %s' % str(widgetname.__name__))
    length = '{:' + str(width) + '}'
    f = 6 if full else 1
    print('-' * int(length[2:-1]) * f)
    print((length * f).format('OPTION', 'NAME', 'NAME for DB', 'CLASS for DB', 'DEFAULT VALUE', 'CURRENT VALUE'))
    print('-' * int(length[2:-1]) * f)
    w = widgetname()
    for key in w.config():
        print(length.format(key), end='')
        if full:
            for elem in w.config()[key]:
                print(length.format(str(elem)), end='')
        print()


if __name__ == '__main__':
    tkprinter(Canvas)
