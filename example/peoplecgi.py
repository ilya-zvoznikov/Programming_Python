"""
Реализует веб - интерфейс для просмотра и изменения экземпляров классов в хранилище;
хранилище находится на сервере (или на том же компьютере, если используется имя localhost)
"""
import cgi, shelve, sys, os

shelvename = 'class-shelve'
# cgi.test() выведет поля ввода
# файлы хранилища находятся
# в текущем каталоге


fieldnames = ('name', 'age', 'job', 'pay')
form = cgi.FieldStorage()
print('Content-type: text/html')
sys.path.insert(0, os.getcwd())
# парсинг данных формы заголовок + пустая строка для ответа благодаря этому модуль pickle и сам сценарий будут способны
# импортировать модуль person

# главный шаблон разметки html
replyhtml = """
<html>
<title> People Input Form </title>
<body>
<form method=POST action="peoplecgi.py">
    <table>
    <tr><th>key<td><input type=text name=key value="%(key)s">
    $ROWS$
    </table>
    <p>
    <input type=submit value="Fetch", name=action>
    <input type=submit value="Update", name=action>
</form>
</body></html>
"""

# вставить разметку html с данными в позицию $ROWS$

rowhtml = '<tr><th>%s<td><input type=text name=%s value="%%(%s)s">\n'
rowshtml = ''

for fieldname in fieldnames:
    rowshtml += (rowhtml % ((fieldname,) * 3))
replyhtml = replyhtml.replace('$ROWS$', rowshtml)


def htmlize(adict):
    new = adict.copy()
    for field in fieldnames:
        value = new[field]
        new[field] = cgi.escape(repr(value))
    return new


# значения могут содержать &, > и другие специальные символы, отображаемые особым образом; их необходимо экранировать


def fetchRecord(db, form):
    try:
        key = form['key'].value
        record = db[key]
        fields = record.__dict__
        # для заполнения строки ответа
        fields['key'] = key
        # использовать словарь атрибутов
    except:
        fields = dict.fromkeys(fieldnames, '?')
        fields['key'] = 'Missing or invalid key!'
    return fields


def updateRecord(db, form):
    if not 'key' in form:
        fields = dict.fromkeys(fieldnames, '?')
        fields['key'] = 'Missing key input!'
    else:
        key = form['key'].value
        if key in db:
            record = db[key]
            # изменить существующую запись
        else:
            from person import Person
            # создать/сохранить новую
            record = Person(name='?', age='?')  # eval: строки должны быть
        # заключены в кавычки
        for field in fieldnames:
            setattr(record, field, eval(form[field].value))
        db[key] = record
        fields = record.__dict__
        fields['key'] = key
    return fields


db = shelve.open(shelvename)
action = form['action'].value if 'action' in form else None
if action == 'Fetch':
    fields = fetchRecord(db, form)
elif action == 'Update':
    fields = updateRecord(db, form)
else:
    fields = dict.fromkeys(fieldnames, '?')
    # недопустимое значение
    fields['key'] = 'Missing or invalid action!'  # кнопки отправки формы115

db.close()
print(replyhtml % htmlize(fields))
# заполнить форму ответа
# из словаря
