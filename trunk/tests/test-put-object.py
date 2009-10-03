import fix_path
from client import DkvClient
from person import Person

d = DkvClient()
d.add_server(('127.0.0.1', 9000))

p = Persona('Herman', 'Polloni', 28)
d.put('person', p)
