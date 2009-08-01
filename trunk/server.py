import asyncore
import socket, time
from data_store import DkvDataStore

class DkvNetHandler(asyncore.dispatcher):
  def create_buffers(self):
    if not 'inbuffer' in self.__dict__:
      self.inbuffer = ''
    if not 'outbuffer' in self.__dict__:
      self.outbuffer = ''

  def handle_read(self):
    self.create_buffers()
    self.inbuffer += self.recv(1)
    if self.inbuffer.endswith("\n"):
      self.inbuffer = self.inbuffer.strip() # remove trailing linebreak
      self.handle_command()

  def handle_command(self):
    print 'Command', self.inbuffer
    args = self.inbuffer.split(" ")
    if args[0] == 'GET':
      self.handle_get(args)
    elif args[0] == 'PUT':
      self.handle_put(args)
    elif args[0] == 'EXIT':
      self.close()
    self.inbuffer = '' # empty inbuffer

  def handle_get(self, args):
    ds = DkvDataStore()
    data = ds.get(args[1])
    if data is None:
      self.outbuffer = "NO\n"
    else:
      self.outbuffer = data + "\n"

  def handle_put(self, args):
    ds = DkvDataStore()
    ds.put(args[1], args[2])
    self.outbuffer = "OK\n"

  def handle_close(self):
    print 'Disconnected from', self.getpeername()
    self.close()

  def writable(self):
    self.create_buffers()
    return (len(self.outbuffer) > 0)

  def handle_write(self):
    self.create_buffers()
    sent = self.send(self.outbuffer)
    self.outbuffer = self.outbuffer[sent:]

class DkvServer(asyncore.dispatcher):
  def __init__(self, port=9000):
    asyncore.dispatcher.__init__(self)
    self.port = port # OPTIONAL
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.bind(("", port))
    self.listen(5)
    print 'Receiving incoming connections on port %d' % port
  def handle_accept(self):
    channel, addr = self.accept()
    print 'Incoming connection from', addr
    DkvNetHandler(channel)

s=DkvServer()
asyncore.loop(timeout=2)