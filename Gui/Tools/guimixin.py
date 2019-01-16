"""
##############################################################################
класс, “подмешиваемый” во фреймы: реализует общие методы вызова стандартных
диалогов, запуска программ, простых инструментов отображения текста и так далее;
метод quit требует, чтобы этот класс подмешивался к классу Frame (или его
производным)
##############################################################################
"""
import sys, os
# sys.path.append(os.getcwd())
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *


# from Gui.Tour.scrolledtext import ScrolledText  # или tkinter.scrolledtext
# from launchmodes import PortableLauncher, System  # или используйте модуль multiprocessing


class GuiMixin:
    def infobox(self, title, text, *args):  # используются стандартные диалоги
        return showinfo(title, text)  # *args для обратной совместимости


if __name__ == '__main__':
    # gm = GuiMixin()
    # gm.infobox('TITLE', 'SOME TEXT')
    print('Интерпретатор', sys.executable, sep='\n')
    print()
    print('CWD', os.getcwd(), sep='\n')
    print()
    print('PATH', *sys.path, sep='\n')
