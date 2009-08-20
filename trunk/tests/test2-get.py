import fix_path
from client import DkvClient


d = DkvClient()
d.add_server(('127.0.0.1', 9000))
personas = d.get('personas')

for p in personas:
	print p['nombre'] + " " + p['apellido'] + " is " + str(p['edad']) + " years old"
