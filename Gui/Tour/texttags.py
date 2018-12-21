"""
демонстрация дополнительных возможностей тегов и виджета Text
"""

from tkinter import *

root = Tk()


def hello(event):
    print('Got tag event')


# создать и настроить виджет Text

text = Text()
text.config(font=('courier', 15, 'normal'))  # общпй шрифт
text.config(width=20, height=12)
text.pack(expand=YES, fill=BOTH)
text.insert(END, 'This is\n\nthe meaning\n\nof life.\n\n')  # вставить 6 строк

# встроить окна и изображения
btn = Button(text, text='Spam', command=(lambda: hello(0)))  # встроить кнопку
btn.pack()
text.window_create(END, window=btn)
text.insert(END, '\n\n')  # встроить изображение
img = PhotoImage(file='../gifs/PythonPowered.gif')
text.image_create(END, image=img)

# применить теги к подстрокам
text.tag_add('demo', '1.5', '1.7')  # добавить ‘is’ в тег
text.tag_add('demo', '3.0', '3.3')  # добавить ‘the’ в тег
text.tag_add('demo', '5.3', '5.7')  # добавить ‘life’ в тег'
text.tag_config('demo', background='purple')  # изменить цвет тега
text.tag_config('demo', foreground='white')  # нельзя использовать короткие имена fg/bg
text.tag_config('demo', font=('times', 16, 'underline'))  # изменить шрифт тега
text.tag_bind('demo', '<Double-1>', hello)  # привязать события
root.mainloop()
