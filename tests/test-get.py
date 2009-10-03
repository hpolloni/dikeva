import fix_path
from client import DkvClient


d = DkvClient()
d.add_server(('127.0.0.1', 9000))
p = d.get('person')
print p['name'] + " " + p['last_name'] + " is " + str(p['age']) + " years old"
