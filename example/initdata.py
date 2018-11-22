from person import Person
from manager import Manager

bob = Person('Bob Smith', 42, 30000, 'software')
sue = Person('Sue Jones', 45, 40000, 'hardware')
tom = Manager('Tom', 50, 30000)

# база данных
db = {}
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom
if __name__ == '__main__':
    """если запускается, как сценарий"""
for key in db:
    print(key, '=>\n ', db[key])
