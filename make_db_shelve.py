import shelve
from initdata import bob, sue, tom

db = shelve.open('people-shelve')
db['bob'] = bob
db['sue'] = sue
db['tom'] = tom

db.close()
