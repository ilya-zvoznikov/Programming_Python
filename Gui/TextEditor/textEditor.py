"""
##############################################################################
PyEdit 2.1: Текстовый редактор и компонент на Python/tkinter.

Использует текстовый виджет из библиотеки Tk, меню и панель инструментов
GuiMaker для реализации полнофункционального текстового редактора, который
может выполняться, как самостоятельная программа, или прикрепляться к другим
графическим интерфейсам, как компонент. Используется также в PyMailGUI
и PyView для редактирования сообщений электронной почты и примечаний к файлам
изображений. Кроме того, используется в PyMailGUI и PyDemos во всплывающем
режиме для отображения текстовых файлов и файлов с исходными текстами.
Новое в версии 2.1 (4 издание)
- работает под управлением Python 3.X (3.1)
- добавлен пункт "grep" меню и диалог: многопоточный поиск в файлах
- проверяет все окна на наличие несохраненных изменений при завершении
- поддерживает произвольные кодировки для файлов: в соответствии с настройками
в файле textConfig.py
- переработаны диалоги поиска с заменой и выбора шрифта, чтобы обеспечить
возможность одновременного вывода нескольких диалогов
- вызывает self.update() перед вставкой текста в новое окно
- различные улучшения в реализации операции Run Code, как описывается
в следующем разделе
2.1 улучшения в реализации операции Run Code:
- после команды chdir использует базовое имя запускаемого файла, а не
относительные пути
- в Windows использует инструмент запуска, поддерживающий передачу аргументов
командной строки
- операция Run Code наследует преобразование символов обратного слеша от
модуля launchmodes (необходимость в этом уже отпала)
Новое в версии 2.0 (3 издание)
- добавлен простой диалог выбора шрифта
- использует прикладной интерфейс Tk 8.4 к стеку отмен, чтобы добавить
поддержку отмены/возврата (undo/redo) операций редактирования
- запрос подтверждения при выполнении операций Quit, Open, New, Run
выполняется, только если имеются несохраненные изменения
- поиск теперь по умолчанию выполняется без учета регистра символов
- создан модуль с настройками для начальных значений
шрифта/цвета/размера/чувствительности к регистру при поиске
TBD (и предложения для самостоятельной реализации):
- необходимость учета регистра символов при поиске можно было бы задавать в
графическом интерфейсе (а не только в файле с настройками)
- при поиске по файлу или в операции Grep можно было бы использовать поддержку
регулярных выражений, реализованную в модуле re (см. следующую главу)
- можно было бы попробовать реализовать подсветку синтаксиса (как в IDLE или в
других редакторах)
- можно было бы попробовать проверить завершение работы программы методом
quit() в неподконтрольных окнах
- можно было бы помещать в очередь каждый результат, найденный в диалоге Grep,
чтобы избежать задержек
- можно было бы использовать изображения на кнопках в панели инструментов (как
в примерах из главы 9)
- можно было бы просматривать строки, чтобы определить позицию вставки Tk для
оформления отступов в окне Info
- можно было бы поэкспериментировать с проблемой кодировок в диалоге "grep"
(смотрите примечания в программном коде);
##############################################################################
"""

Version = '2.1'
import sys, os  # платформа, аргументы, инструменты запуска, базовые виджеты, константы, стандартные диалоги
from tkinter import *
from tkinter.filedialog import Open, SaveAs
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter.simpledialog import askstring, askinteger
from tkinter.colorchooser import askcolor
from Gui.Tools.guimaker import *  # Frame + построители меню/панелей инструментов

# общие настройки
try:
    import textConfig  # начальный шрифт и цвета

    configs = textConfig.__dict__  # сработает, даже если модуль отсутствует в пути поиска или содержит ошибки
except:
    configs = {}

helptext = """PyEdit, версия %s
апрель 2010
(2.0: январь, 2006)
(1.0: октябрь, 2000)
Программирование на Python, 4 издание
Марк Лутц (Mark Lutz), для издательства O'Reilly Media, Inc.
Программа и встраиваемый компонент текстового редактора,
написанный на Python/tkinter. Для быстрого доступа к операциям
использует отрывные меню, панели инструментов и горячие клавиши в меню.

Дополнения в версии %s:
- поддержка 3.X
- новый диалог "grep" поиска во внешних файлах
- проверка несохраненных изменений при завершении
- поддержка произвольных кодировок для файлов
- допускает одновременный вывод нескольких диалогов
поиска с заменой и выбора шрифта
- различные улучшения в операции Run Code

Дополнения в предыдущей версии:
- диалог выбора шрифта
- неограниченное количество отмен/возвратов
- quit/open/new/run предлагают сохранить, только
если есть несохраненные изменения
- поиск выполняется без учета регистра символов
- модуль с начальными настройками textConfig.py
"""

START = '1.0'  # индекс первого символа: строка=1, столбец=0

# не понимаю, зачем нужны эти переменные; точно такие же есть в самом tkinter
# SEL_FIRST = SEL + '.first'  # отобразить тег sel в индекс
# SEL_LAST = SEL + '.last'  # то же, что 'sel.last'

FontScale = 0  # использовать увеличенный шрифт в Linux
if sys.platform[:3] != 'win':
    FontScale = 3


##############################################################################
# Главные классы: реализуют графический интерфейс редактора, операции
# разновидности GuiMaker должны подмешиваться в более специализированные
# подклассы, а не наследоваться непосредственно, потому что этот класс
# принимает множество форм.
##############################################################################

class TextEditor:  # смешать с классом Frame, имеющим меню/панель инструментов
    startfiledir = '.'  # для диалогов
    editwindows = []  # для проверки при завершении

    # Настройки порядка выбора кодировки
    # импортируется в класс, чтобы обеспечить возможность переопределения в
    # подклассе

    if __name__ == '__main__':
        from textConfig import (  # мой каталог в пути поиска
            opensAskUser, opensEncoding,
            savesUseKnownEncoding, savesAskUser, savesEncoding)
    else:
        from .textConfig import (  # 2.1: всегда из этого пакетаq   q
            opensAskUser, opensEncoding,
            savesUseKnownEncoding, savesAskUser, savesEncoding)

    ftypes = [('All files', '*'),  # для диалога открытия файла
              ('Text files', '.txt'),  # настроить в подклассе или
              ('Python files', '.py')]  # устанавливать в каждом экземпляре

    colors = [{'fg': 'black', 'bg': 'white'},  # список цветов для выбора
              {'fg': 'yellow', 'bg': 'black'},  # первый элемент по умолчанию
              {'fg': 'white', 'bg': 'blue'},  # переделать по-своему или
              {'fg': 'black', 'bg': 'beige'},  # использовать элемент выбора
              {'fg': 'yellow', 'bg': 'purple'},  # PickBg/Fg
              {'fg': 'black', 'bg': 'brown'},
              {'fg': 'lightgreen', 'bg': 'darkgreen'},
              {'fg': 'darkblue', 'bg': 'orange'},
              {'fg': 'orange', 'bg': 'darkblue'}]

    fonts = [('courier', 9 + FontScale, 'normal'),  # шрифты, нейтральные
             ('courier', 12 + FontScale, 'normal'),  # в отношении платформы
             ('courier', 10 + FontScale, 'bold'),  # (семейство, размер, стиль)
             ('courier', 10 + FontScale, 'italic'),  # или вывести в списке
             ('times', 10 + FontScale, 'normal'),  # увеличить в Linux
             ('helvetica', 10 + FontScale, 'normal'),  # использовать
             ('ariel', 10 + FontScale, 'normal'),  # 'bold italic' для 2
             ('system', 10 + FontScale, 'normal'),  # а также 'underline'
             ('courier', 20 + FontScale, 'normal')]

    def __init__(self, loadFirst='', loadEncode=''):
        if not isinstance(self, GuiMaker):
            raise TypeError('TextEditor needs a GuiMaker mixin')
        self.setFileName(None)
        self.lastfind = None
        self.openDialog = None
        self.saveDialog = None
        self.knownEncoding = None  # 2.1 кодировки: заполняется Open или Save
        self.text.focus()  # иначе придется щелкнуть лишний раз
        if loadFirst:
            self.update()  # 2.1: иначе строка 2;
            self.onOpen(loadFirst, loadEncode)  # см. описание в книге

    def start(self):  # вызывается из GuiMaker.__init__
        self.menuBar = [  # настройка меню/панелей
            ('File', 0,
             [('Open...', 0, self.onOpen),
              ('Save', 0, self.onSave),
              ('Save As', 5, self.onSaveAs),
              ('New', 0, self.onNew),
              'separator',
              ('Quit', 0, self.onQuit)]
             ),
            ('Edit', 0,
             [('Undo', 0, self.onUndo),
              ('Redo', 0, self.onRedo),
              'separator',
              ('Cut', 0, self.onCut),
              ('Copy', 1, self.onCopy),
              ('Paste', 0, self.onPaste),
              'separator',
              ('Delete', 0, self.onDelete),
              ('Select All', 0, self.onSelectAll)]
             ),
            ('Search', 0,
             [('Goto', 0, self.onGoto),
              ('Find', 0, self.onFind),
              ('Refind', 0, self.onRefind),
              ('Change...', 0, self.onChange),
              ('Grep', 3, self.onGrep)]
             ),
            ('Tools', 0,
             [('Pick Font...', 6, self.onPickFont),
              ('Font List', 0, self.onFontList),
              'separator',
              ('Pick Bg...', 3, self.onPickBg),
              ('Pick Fg...', 0, self.onPickFg),
              ('Color List', 0, self.onColorList),
              'separator',
              ('Info...', 0, self.onInfo),
              ('Clone', 1, self.onClone),
              ('Run Code', 0, self.onRunCode)]
             )]

        self.toolBar = [
            ('Save', self.onSave, {'side': LEFT}),
            ('Cut', self.onCut, {'side': LEFT}),
            ('Copy', self.onCopy, {'side': LEFT}),
            ('Paste', self.onPaste, {'side': LEFT}),
            ('Find', self.onRefind, {'side': LEFT}),
            ('Help', self.help, {'side': RIGHT}),
            ('Quit', self.onQuit, {'side': RIGHT})]

    def makeWidgets(self):  # вызывается из GuiMaker.__init__
        name = Label(self, bg='black', fg='white')  # ниже меню, выше панели
        name.pack(side=TOP, fill=X)  # компоновка меню/панелей, фрейм GuiMaker компонуется сам

        vbar = Scrollbar(self)
        hbar = Scrollbar(self, orient='horizontal')
        text = Text(self, padx=5, wrap='none')  # запретить перенос строк
        text.config(undo=1, autoseparators=1)  # 2.0, по умолчанию 0, 1

        vbar.pack(side=RIGHT, fill=Y)
        hbar.pack(side=BOTTOM, fill=X)  # скомпоновать текст последним, иначе обрежутся полосы прокрутки
        text.pack(side=TOP, fill=BOTH, expand=YES)

        text.config(yscrollcommand=vbar.set)  # вызывать vbar.set при
        text.config(xscrollcommand=hbar.set)  # перемещении по тексту
        vbar.config(command=text.yview)  # вызывать text.yview при прокрутке
        hbar.config(command=text.xview)  # или hbar['command']=text.xview

        # 2.0: применить пользовательские настройки или умолчания
        startfont = configs.get('font', self.fonts[0])
        startbg = configs.get('bg', self.colors[0]['bg'])
        startfg = configs.get('fg', self.colors[0]['fg'])
        text.config(font=startfont, bg=startbg, fg=startfg)
        if 'height' in configs:
            text.config(height=configs['height'])
        if 'width' in configs:
            text.config(width=configs['width'])
        self.text = text
        self.filelabel = name

    ##########################################################################
    # Операции меню File
    ##########################################################################

    def my_askopenfilename(self):  # объекты запоминают каталог/файл последней операции
        if not self.openDialog:
            self.openDialog = Open(initialdir=self.startfiledir, filetypes=self.ftypes)
        return self.openDialog.show()

    def my_asksaveasfilename(self):  # объекты запоминают каталог/файл последней операции
        if not self.saveDialog:
            self.saveDialog = SaveAs(initialdir=self.startfiledir, filetypes=self.ftypes)
        return self.saveDialog.show()

    def onOpen(self, loadFirst='', loadEncode=''):
        """
        2.1: полностью переписан для поддержки Юникода; открывает в текстовом
        режиме с кодировкой, переданной в аргументе, введенной пользователем,
        заданной в модуле textconfig или с кодировкой по умолчанию;
        в крайнем случае открывает файл в двоичном режиме и отбрасывает
        символы \r в Windows, если они присутствуют, чтобы обеспечить
        нормальное отображение текста; содержимое извлекается и возвращается в
        виде строки str, поэтому при сохранении его требуется кодировать:
        сохраняет кодировку, используемую здесь;
        предварительно проверяет возможность открытия файла;
        мы могли бы также вручную загружать и декодировать bytes в str, чтобы
        избежать необходимости выполнять несколько попыток открытия, но этот
        прием подходит не для всех случаев;
        порядок выбора кодировки настраивается в локальном textConfig.py:
        1) сначала применяется кодировка, переданная клиентом (например,
        кодировка из заголовка сообщения электронной почты)
        2) затем, если opensAskUser возвращает True, применяется кодировка,
        введенная пользователем (предварительно в диалог записывается
        кодировка по умолчанию)
        3) затем, если opensEncoding содержит непустую строку, применяется
        эта кодировка: 'latin-1' и так далее.
        4) затем выполняется попытка применить кодировку
        sys.getdefaultencoding()
        5) в крайнем случае выполняется чтение в двоичном режиме и
        используется алгоритм, заложенный в библиотеку Tk
        :param loadFirst:
        :param loadEncode:
        :return:
        """

        if self.text_edit_modified():  # 2.0
            if not askyesno('PyEdit', 'Text has changed: discard changes?'):
                return

        file = loadFirst or self.my_askopenfilename()
        if not file:
            return

        if not os.path.isfile(file):
            showerror('PyEdit', 'Could not open file ' + file)
            return

        # применить известную кодировку, если указана
        # (например, из заголовка сообщения электронной почты)
        text = None  # пустой файл = '' = False: проверка на None!
        if loadEncode:
            try:
                text = open(file, 'r', encoding=loadEncode).read()
                self.knownEncoding = loadEncode
            except (UnicodeError, LookupError, IOError):  # Lookup: ошибка в имени
                pass

        # применить кодировку, введенную пользователем,
        # предварительно записать в диалог следующий вариант, как значение
        # по умолчанию
        if text == None and self.opensAskUser:
            self.update()  # иначе в некоторых случаях диалог не появится
            askuser = askstring('PyEdit', 'Enter Unicode encoding for open',
                                initialvalue=(self.opensEncoding or sys.getdefaultencoding() or ''))
            if askuser:
                try:
                    text = open(file, 'r', encoding=askuser).read()
                    self.knownEncoding = askuser
                except (UnicodeError, LookupError, IOError):
                    pass

        # применить кодировку из файла с настройками (может быть, выполнять
        # эту попытку до того, как запрашивать кодировку у пользователя?)
        if text == None and self.opensEncoding:
            try:
                text = open(file, 'r', encoding=self.opensEncoding).read()
                self.knownEncoding = self.opensEncoding
            except (UnicodeError, LookupError, IOError):
                pass

        # применить системную кодировку по умолчанию (utf-8 в windows;
        # всегда пытаться использовать utf8?)
        if text == None:
            try:
                text = open(file, 'r', encoding=sys.getdefaultencoding()).read()
                self.knownEncoding = sys.getdefaultencoding()
            except (UnicodeError, LookupError, IOError):
                pass

        # крайний случай: использовать двоичный режим
        # возможности Tk
        if text == None:
            try:
                text = open(file, 'rb').read()  # строка bytes для отображения и последующего сохранения
                text = text.replace(b'\r\n', b'\n')
                self.knownEncoding = None
            except IOError:
                pass

        if text == None:
            showerror('PyEdit', 'Could not decode and open file ' + file)
        else:
            self.setAllText(text)
            self.setFileName(file)
            self.text.edit_reset()  # 2.0: очистка стеков undo/redo
            self.text.edit_modified(0)  # 2.0: сбросить флаг наличия изменений

    def onSave(self):
        self.onSaveAs(self.currfile)  # may be None

    def onSaveAs(self, forcefile=None):
        """
        2.1: полностью переписан для поддержки Юникода: виджет Text всегда
        возвращает содержимое в виде строки str, поэтому нам необходимо
        побеспокоиться о кодировке, чтобы сохранить файл, независимо от
        режима, в котором открывается выходной файл (для двоичного режима
        необходимо будет получить bytes, а для текстового необходимо указать
        кодировку); пытается применить кодировку, использовавшуюся при
        открытии или сохранении (если известна), предлагаемую пользователем,
        указанную в файле с настройками, и системную кодировку по умолчанию;
        в большинстве случаев можно использовать системную кодировку по
        умолчанию;
        в случае успешного выполнения операции сохраняет кодировку для
        использования в дальнейшем, потому что это может быть первая операция
        Save после операции New или вставки текста вручную; в файле
        с настройками можно определить, чтобы обе операции, Save и Save As,
        использовали последнюю известную кодировку (однако если для операции
        Save это оправданно, то в случае с операцией Save As это не так
        очевидно); графический интерфейс предварительно записывает эту
        кодировку в диалог, если она известна;
        выполняет text.encode() вручную, чтобы избежать создания файла; для
        текстовых файлов автоматически выполняется преобразование символов
        конца строки: в Windows добавляются символы \r, отброшенные при
        открытии файла в текстовом (автоматически) или в двоичном (вручную)
        режиме; Если содержимое вставлялось вручную, здесь необходимо
        предварительно удалить символы \r, иначе они будут продублированы;
        knownEncoding=None перед первой операцией Open или Save, после New
        и если операция Open открыла файл в двоичном режиме;
        порядок выбора кодировки настраивается в локальном textConfig.py:
        1) если savesUseKnownEncoding > 0, применить кодировку, использованную
        в последней операции Open или Save
        2) если savesAskUser = True, применить кодировку, указанную
        пользователем (предлагать известную в качестве значения по
        умолчанию?)
        3) если savesEncoding - непустая строка, применить эту кодировку:
        'utf-8' и так далее
        4) в крайнем случае применить sys.getdefaultencoding()
        :param forcefile:
        :return:
        """

        filename = forcefile or self.my_asksaveasfilename()
        if not filename:
            return

        text = self.getAllText()  # 2.1: строка str, без символов \r,
        encpick = None  # даже если текст читался/вставлялся в двоичном виде

        # применить известную кодировку, использовавшуюся в последней операции
        # Open или Save, если известна
        if self.knownEncoding and (  # известна?
                (forcefile and self.savesUseKnownEncoding >= 1) or  # для Save?
                (not forcefile and self.savesUseKnownEncoding >= 2)):  # для SaveAs?
            try:
                text.encode(self.knownEncoding)
                encpick = self.knownEncoding
            except UnicodeError:
                pass

        # применить кодировку, введенную пользователем,
        # предварительно записать в диалог следующий вариант, как значение
        # по умолчанию
        if not encpick and self.savesAskUser:
            self.update()  # иначе в некоторых случаях диалог не появится
            askuser = askstring('PyEdit', 'Enter Unicode encoding for save',
                                initialvalue=(self.knownEncoding or
                                              self.savesEncoding or
                                              sys.getdefaultencoding() or ''))
        if askuser:
            try:
                text.encode(askuser)
                encpick = askuser
            except (UnicodeError, LookupError):
                pass

        # применить кодировку из файла с настройками
        if not encpick and self.savesEncoding:
            try:
                text.encode(self.savesEncoding)
                encpick = self.savesEncoding
            except (UnicodeError, LookupError):
                pass

        # применить системную кодировку по умолчанию (utf8 в windows)
        if not encpick:
            try:
                text.encode(sys.getdefaultencoding())
                encpick = sys.getdefaultencoding()
            except (UnicodeError, LookupError):
                pass

        # открыть в текстовом режиме, чтобы автоматически выполнить
        # преобразование символов конца строки и применить кодировку
        if not encpick:
            showerror('PyEdit', 'Could not encode for file ' + filename)
        else:
            try:
                file = open(filename, 'w', encoding=encpick)
                file.write(text)
                file.close()
            except:
                showerror('PyEdit', 'Could not write file ' + filename)
            else:
                self.setFileName(filename)  # может быть вновь созданным
                self.text.edit_modified(0)  # 2.0: сбросить флаг изменений
                self.knownEncoding = encpick  # 2.1: запомнить кодировку
                # не сбрасывать стеки undo/redo!

    def onNew(self):
        """
        запускает редактирование совершенно нового файла в текущем окне;
        смотрите метод onClone, который вместо этого создает независимое окно
        редактирования;
        :return:
        """
        if self.text_edit_modified():  # 2.0
            if not askyesno('PyEdit', 'Text has changed: discard changes?'):
                return

        self.setFileName(None)
        self.clearAllText()
        self.text.edit_reset()  # 2.0: очистить стеки undo/redo
        self.text.edit_modified(0)  # 2.0: сбросить флаг наличия изменений
        self.knownEncoding = None  # 2.1: кодировка неизвестна

    def onQuit(self):
        """
        вызывается выбором операции Quit в меню/панели инструментов и щелчком
        на кнопке X в заголовке окна;
        2.1: не завершать приложение при наличии несохраненных изменений;
        2.0: не выводить запрос на подтверждение, если нет изменений в self;
        перемещен в классы окон верхнего уровня ниже, так как его
        реализация может зависеть от особенностей использования: операция Quit
        в графическом интерфейсе может вызывать метод quit() для завершения,
        destroy() – чтобы просто закрыть окно Toplevel, Tk или фрейм
        с редактором, эта операция может даже вообще не предоставляться,
        если редактор присоединяется, как компонент; проверяет self на наличие
        несохраненных изменений, а если предполагается вызов метода quit(),
        главные окна должны также проверить наличие несохраненных изменений
        в других окнах, присутствующих в глобальном списке процесса;
        :return:
        """

        assert False, 'onQuit must be defined in window-specific subclass'

    def text_edit_modified(self):
        """
        2.1: теперь действует! кажется, проблема заключалась в типе bool
        результата в tkinter;
        2.0: self.text.edit_modified() не работает в Python 2.4: выполнить
        проверку вручную;
        :return:
        """
        return self.text.edit_modified()

    ##########################################################################
    # Операции меню Edit
    ##########################################################################

    def onUndo(self):  # 2.0
        try:  # tk8.4 поддерживает стеки undo/redo
            self.text.edit_undo()  # возбуждает исключение, если стеки пустые
        except TclError:  # меню открывается для быстрого доступа к операциям
            showinfo('PyEdit', 'Nothing to undo')

    def onRedo(self):  # 2.0: возврат отмененной операции редактирования
        try:
            self.text.edit_redo()
        except TclError:
            showinfo('PyEdit', 'Nothing to redo')

    def onCopy(self):  # получить текст, выделенный мышью
        if not self.text.tag_ranges(SEL):  # сохранить в системном буфере
            showerror('PyEdit', 'No text selected')
        else:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)

    def onDelete(self):  # удалить выделенный текст без сохранения
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.text.delete(SEL_FIRST, SEL_LAST)

    def onCut(self):
        if not self.text.tag_ranges(SEL):
            showerror('PyEdit', 'No text selected')
        else:
            self.onCopy()  # сохранить и удалить выделенный текст
            self.onDelete()

    def onPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
        except TclError:
            showerror('PyEdit', 'Nothing to paste')
            return
        self.text.insert(INSERT, text)  # вставить в текущую позицию курсора
        self.text.tag_remove(SEL, '1.0', END)
        self.text.tag_add(SEL, INSERT + '-%dc' % len(text), INSERT)
        self.text.see(INSERT)  # выделить, чтобы можно было вырезать

    def onSelectAll(self):
        self.text.tag_add(SEL, '1.0', END + '-1c')  # выделить весь текст
        self.text.mark_set(INSERT, '1.0')  # переместить позицию в начало
        self.text.see(INSERT)  # прокрутить в начало

    ##########################################################################
    # Операции меню Search
    # ЗАГЛУШКИ!!! ДОПИСАТЬ!!!
    ##########################################################################

    def onGoto(self, forceline=None):
        line = forceline or askinteger('PyEdit', 'Enter line number')
        self.text.update()
        self.text.focus()
        if line is not None:
            maxindex = self.text.index(END + '-1c')
            maxline = int(maxindex.split('.')[0])
            if line > 0 and line <= maxline:
                self.text.mark_set(INSERT, '%d.0' % line)  # перейти к строке
                self.text.tag_remove(SEL, '1.0', END)  # снять выделение
                self.text.tag_add(SEL, INSERT, 'insert + 1l')  # выделить строку
                self.text.see(INSERT)  # прокрутить до строки
            else:
                showerror('PyEdit', 'Bad line number')

    def onFind(self, lastkey=None):
        key = lastkey or askstring('PyEdit', 'Enter search string')
        self.text.update()
        self.text.focus()
        self.lastfind

##########################################################################################
# ТУТ ОСТАНОВИЛСЯ
##########################################################################################


    def onRefind(self):
        pass

    def onChange(self):
        pass

    def onDoChange(self, findtext, changeto):
        pass

    def onGrep(self):
        pass

    def onDoGrep(self, dirname, filenamepatt, grepkey, encoding):
        pass

    def grepThreadProducer(self, filenamepatt, dirname, grepkey, encoding, myqueue):
        pass

    def grepThreadConsumer(self, grepkey, encoding, myqueue, mypopup):
        pass

    def grepMatchesList(self, matches, grepkey, encoding):
        pass

    ##########################################################################
    # Операции меню Tools
    # ЗАГЛУШКИ!!! ДОПИСАТЬ!!!
    ##########################################################################

    def onFontList(self):
        pass

    def onColorList(self):
        pass

    def onPickFg(self):
        pass

    def onPickBg(self):
        pass

    def pickColor(self, part):
        pass

    def onInfo(self):
        pass

    def onClone(self, makewindow=True):
        pass

    def onRunCode(self, parallelmode=True):
        pass

    def onPickFont(self):
        pass

    def onDoFont(self, family, size, style):
        pass

    ##########################################################################
    # Прочие утилиты, полезные за пределами этого класса
    ##########################################################################

    def isEmpty(self):
        return not self.getAllText()

    def getAllText(self):
        return self.text.get('1.0', END + '-1c')  # извлечь текст как строку str

    def setAllText(self, text):
        """
        вызывающий: должен предварительно вызвать self.update(), если только
        что был прикреплен, иначе начальная позиция может оказаться не в
        первой, а во второй строке (2.1; ошибка Tk?)
        :param text:
        :return:
        """
        self.text.delete('1.0', END)  # записать текстовую строку в виджет
        self.text.insert(END, text)  # или '1.0'; текст = bytes или str
        self.text.mark_set(INSERT, '1.0')  # переместить точку ввода в начало
        self.text.see(INSERT)

    def clearAllText(self):
        self.text.delete('1.0', END)

    def getFileName(self):
        return self.currfile

    def setFileName(self, name):  # смотрите также: onGoto(linenum)
        self.currfile = name  # для последующего сохранения
        self.filelabel.config(text=str(name))

    def senKnownEncoding(self, encoding='utf-8'):  # 2.1: для сохранения
        self.knownEncoding = encoding  # иначе будут использованы настройки, запрос?

    def setBg(self, color):
        self.text.config(bg=color)  # для установки вручную из программы

    def setFg(self, color):
        self.text.config(fg=color)  # 'black', шестнадцатеричная строка

    def setFont(self, font):
        self.text.config(font=font)  # ('семейство', 'размер', 'стиль')

    def setHeight(self, lines):  # по умолчанию = 24 строки x 80 символов
        self.text.config(height=lines)  # можно также взять из textCongif.py

    def setWidth(self, chars):
        self.text.config(width=chars)

    def clearModified(self):
        self.text.edit_modified(0)  # сбросить флаг наличия изменений

    def isModified(self):  # были изменения с момента
        return self.text_edit_modified()  # последнего сброса флага?

    def help(self):
        showinfo('About PyEdit', helptext % ((Version,) * 2))


# -----------------------------------------------------------------------------
# 2.1: в quit(), не завершать без предупреждения, если в процессе открыты
# другие окна редактора и в них имеются несохраненные изменения - изменения
# будут потеряны, потому что все остальные окна тоже закрываются, включая
# множественные родительские окна Tk, включающие редактор; для слежения за
# всеми окнами PyEdit используется список экземпляров, созданных в процессе;
# это может оказаться чрезмерной мерой (если вместо quit() вызывается
# destroy(), когда достаточно проверить только дочернее окно редактирования
# уничтожаемого родителя), но лучше перестраховаться; метод onQuit перемещен
# сюда, потому что его реализация отличается для окон разных типов и может
# присутствовать не во всех окнах;
#
# предполагается, что TextEditorMainPopup никогда не будет играть роль
# родителя для других окон редактирования - дочерние виджеты Toplevel
# уничтожаются вместе со своими родителями; это не позволяет предотвратить
# закрытие из-за пределов классов PyEdit (метод quit в tkinter доступен
# во всех виджетах, и любой виджет может быть родителем для Toplevel!);
# ответственность за проверку наличия изменений в содержимом редактора
# полностью возлагается на клиента; обратите внимание, что в данной ситуации
# привязка события <Destroy> не даст ровным счетом ничего, потому что его
# обработчик не может выполнять операции с графическим интерфейсом, такие как
# проверка наличия изменений и извлечение текста, - дополнительную информацию
# об этом событии смотрите в книге и в модуле destroyer.py;
# -----------------------------------------------------------------------------

########################################
# когда текстовый редактор владеет окном
########################################

class TextEditorMain(TextEditor, GuiMakerWindowMenu):
    """
    главное окно редактора PyEdit, которое вызывает метод quit() при
    выполнении операции Quit графического интерфейса для завершения
    приложения и конструирует меню в окне; родителем может быть окно Tk,
    по умолчанию, окно Tk, создаваемое явно, или объект Toplevel:
    родитель должен быть окном и, вероятно, окном Tk, чтобы избежать закрытия
    без предупреждения вместе с родителем; при выполнении операции Quit
    графического интерфейса все главные окна PyEdit проверяют остальные окна
    PyEdit, открытые в процессе, на наличие несохраненных изменений, поскольку
    вызов метода quit() здесь приведет к завершению всего приложения; фрейм
    редактора необязательно должен занимать окно целиком (окно может включать
    и другие компоненты: смотрите PyView), но его операция Quit завершает
    программу; метод onQuit вызывается операцией Quit, выполняемой щелчком на
    кнопке в панели инструментов, выбором пункта в меню File, а также щелчком
    на кнопке X в заголовке окна;
    """

    def __init__(self, parent=None, loadFirst='', loadEncode=''):
        # редактор занимает все родительское окно
        GuiMaker.__init__(self, parent)  # использует главное меню окна
        TextEditor.__init__(self, loadFirst, loadEncode)  # фрейм GuiMaker прикрепляет себя сам

        self.master.title('PyEdit ' + Version)  # заголовок, кнопка X, если
        self.master.iconname('PyEdit')  # выполняется как отдельная
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)  # программа
        TextEditor.editwindows.append(self)

    def onQuit(self):  # вызывается операцией Quit
        close = not self.text_edit_modified()  # проверить себя, запросить, проверить другие
        if not close:
            close = askyesno('PyEdit', 'Text changed: quit and discard changes?')
        if close:
            windows = TextEditor.editwindows
            changed = [w for w in windows if w != self and w.text_edit_modified()]
            if not changed:
                GuiMaker.quit(self)  # завершить все приложение, независимо от типа виджета
            else:
                numchange = len(changed)
                verify = '%s other edit window%s changed: '
                verify += 'quit and discard anyhow?'
                verify = verify % (numchange, 's' if numchange > 1 else '')
                if askyesno('PyEdit', verify):
                    GuiMaker.quit(self)


class TextEditorMainPopup(TextEditor, GuiMakerWindowMenu):
    # ЗАГЛУШКА!!! ДОПИСАТЬ!!!
    """
    всплывающее окно PyEdit, которое вызывает метод destroy() при выполнении
    операции Quit графического интерфейса, закрывает только себя и создает
    меню в окне; создает собственного родителя Toplevel, который является
    дочерним для окна Tk по умолчанию (если передается значение None) или для
    другого указанного окна или виджета (например, для фрейма);
    добавляется в список для проверки при закрытии любого главного окна
    PyEdit; если будет создано главное окно PyEdit, родитель данного окна
    также должен быть родителем главного окна PyEdit, чтобы оно не было
    закрыто без предупреждения; метод onQuit вызывается операцией Quit,
    выполняемой щелчком на кнопке в панели инструментов, выбором пункта в меню
    File, а также щелчком на кнопке X в заголовке окна;
    """

    def __init__(self, parent=None, loadFirst='', winTitle='', loadEncode=''):
        # создать собственное окно
        # self.popup = Toplevel(parent)
        # GuiMaker.__init__(self, self.popup)  # использует главное меню окна
        TextEditor.__init__(self, loadFirst, loadEncode)  # фрейм в новом окне
        # assert self.master == self.popup
        pass

    def onQuit(self):
        pass

    def onClone(self):
        pass


###########################################
# когда редактор встраивается в другое окно
# ДАЖЕ НЕ НАЧИНАЛ!!!
###########################################

##############################################################################
# запуск как самостоятельной программы
##############################################################################

def testPopup():
    # проверку запуска как компонента смотрите в PyView и PyMail
    root = Tk()
    TextEditorMainPopup(root)
    TextEditorMainPopup(root)
    Button(root, text='More', command=TextEditorMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()


def main():
    try:
        fname = sys.argv[1]
    except IndexError:
        fname = None

    TextEditorMain(loadFirst=fname).pack(expand=YES, fill=BOTH)
    mainloop()


if __name__ == '__main__':
    # testPopup()
    main()
