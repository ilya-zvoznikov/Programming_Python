import requests

r = requests.get('http://translate.google.ru/translate_a/t?client=x&text="fetch"&hl=en&sl=en&tl=ru')
print(r.url)

"""
https://pypi.org/project/py-translate/
https://multillect.com/apidoc
https://tech.yandex.com/translate/doc/dg/reference/translate-docpage/
"""