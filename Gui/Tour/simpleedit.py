"""
за счет наследования добавляет в ScrolledText типичные инструменты
редактирования; аналогичного результата можно было бы добиться, применив прием
композиции (встраивания); ненадежно! -- надмножество функций имеется в PyEdit;
"""

from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename
from Gui.Tour.quitter import Quitter
from Gui.Tour.scrolledtext import ScrolledText


class SimpleEditor(ScrolledText):
    def __init__(self, parent=None, file=None):
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, text='Save', command=self.onSave).pack(side=LEFT)
        Button(frm, text='Cut', command=self.onCut).pack(side=LEFT)
        Button(frm, text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, text='Find', command=self.onFind).pack(side=LEFT)
        Quitter(frm).pack(side=LEFT)
        ScrolledText.__init__(self, parent, file=file)
        self.text.config(font=('courier', '9', 'normal'))

    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()
            open(filename, 'w').write(alltext)

    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)
        self.text.delete(SEL_FIRST, SEL_LAST)
        self.clipboard_clear()
        self.clipboard_append(text)

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass

    def onFind(self):
        target = askstring('SimpleEditor', 'Search String?')
        if target:
            where = self.text.search(target, INSERT, END)
            if where:
                print(where)
                pastit = where + ('+ % dc' % len(target))  # индекс за целью
                self.text.tag_remove(SEL, '1.0', END) # снять выделение
                self.text.tag_add(SEL, where, pastit)  # выделить найденное
                self.text.mark_set(INSERT, pastit)  # установить метку вставки
                self.text.see(INSERT)  # прокрутить текст
                self.text.focus()  # выбрать виджет Text


if __name__ == '__main__':
    if len(sys.argv) > 1:
        SimpleEditor(file=sys.argv[1]).mainloop()  # имя файла в ком. строке
    else:
        SimpleEditor().mainloop()  # или нет: пустой виджет
