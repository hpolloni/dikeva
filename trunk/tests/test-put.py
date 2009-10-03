import fix_path
from client import DkvClient

d = DkvClient()
d.add_server(('127.0.0.1', 9000))
d.put('person', {'name' : 'Herman', 'last_name':'Polloni', 'age':28})
