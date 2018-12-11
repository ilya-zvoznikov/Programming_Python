from tkinter import *

root = Tk()
labelfont = ('system', 20, 'bold')  # семейство, размер, стиль
widget = Label(root, text='Loading...')
widget.config(bg='black', fg='#00ff00')  # желтый текст на черном фоне
widget.config(font=labelfont)  # использовать увеличенный шрифт
widget.config(height=3, width=20)  # начальный размер: строк,символов
widget.config(cursor='watch')  # форма курсора при наведении на виджет - "песочные часики"
widget.pack(expand=YES, fill=BOTH)
root.mainloop()
