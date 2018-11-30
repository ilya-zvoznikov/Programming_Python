"""##############################################################################
Создает страницы со ссылками переадресации на перемещенный веб-сайт.
Генерирует по одной странице для каждого существующего на сайте файла html;
сгенерированные файлы нужно выгрузить на ваш старый веб-сайт. Смотрите описание
ftplib далее в книге, где представлены приемы реализации выгрузки файлов
в сценариях после или в процессе создания файлов страниц.
##############################################################################"""

import os

servername = 'learning-python.com'  # новый адрес сайта
homedir = 'books'  # корневой каталог сайта
sitefilesdir = r'C:\temp\public_html'  # локальный каталог с файлами сайта
uploaddir = r'C:\temp\isp-forward'  # где сохранять сгенерированные файлы
templatename = 'template.html'  # шаблон для генерируемых страниц

try:
    os.mkdir(uploaddir)
except OSError:
    pass

template = open(templatename).read()
sitefiles = os.listdir(sitefilesdir)

count = 0

for filename in sitefiles:
    if filename.endswith('.html') or filename.endswith('.htm'):
        fwdname = os.path.join(uploaddir, filename)
        print('Creating', filename, 'as', fwdname)
        filetext = template.replace('$server$', servername)
        filetext = filetext.replace('$home$', homedir)
        filetext = filetext.replace('$file$', filename)
        open(fwdname, 'w').write(filetext)
        count += 1

print('Last file =>\n', filetext, sep='')
print('Done:', count, 'forward files created.')
