import fix_path
from client import DkvClient

d = DkvClient()
d.add_server(('127.0.0.1', 9000))

for i in xrange(0,1000):
	key = 'person' + str(i)
	name = 'name' + str(i)
	last_name = 'last_name'+str(i)
	age = i
	d.put(key, {'name':name, 'last_name':last_name, 'age':age})
