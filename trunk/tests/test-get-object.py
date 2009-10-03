import fix_path
from client import DkvClient
from person import Person

d = DkvClient()
d.add_server(('127.0.0.1', 9000))

pdata = d.get('person')

p = Person()
p.unserialize(pdata)
print p.name + " " + p.last_name + " is " + str(p.age) + " years old"

