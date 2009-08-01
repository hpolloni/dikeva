from client import DkvClient

d = DkvClient()
d.add_server(('127.0.0.1', 9000))
d.put('personas', 
  [
    {'nombre' : 'Herman', 'apellido':'Polloni', 'edad':28},
    {'nombre' : 'Daniela', 'apellido':'Fuenzalida', 'edad':24}
  ]
)