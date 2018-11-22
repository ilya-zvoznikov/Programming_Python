"""
Реализация веб-сервера на языке Python, способная запускать серверные
CGI-сценарии на языке Python; обслуживает файлы и сценарии в текущем
рабочем каталоге; сценарии на языке Python должны находиться в каталоге
webdir\cgi-bin или webdir\htbin;
"""
import os, sys
from http.server import HTTPServer, CGIHTTPRequestHandler

webdir = '.'
port = 8888
# место, где находятся файлы html и подкаталог cgi-bin
# по умолчанию http://localhost/, иначе используйте
# http://localhost:xxxx/
os.chdir(webdir)
# перейти в корневой каталог HTML
srvraddr = ("", port)
# имя хоста и номер порта
srvrobj = HTTPServer(srvraddr, CGIHTTPRequestHandler)
srvrobj.serve_forever()
# запустить как бесконечный фоновый процесс
