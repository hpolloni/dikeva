import asyncore
import socket, time
from data_store import DkvDataStore
import dkv_config
from dkv_functions import dkv_debug

DATA_STORE = None
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
		dkv_debug('%s : %s' % (self.getpeername() , self.inbuffer))
		args = self.inbuffer.split(" ")
		if len(args) > 0:
			if args[0] == 'GET':
				self.handle_get(args)
			elif args[0] == 'PUT':
				self.handle_put(args)
			elif args[0] == 'EXIT':
				self.close()
		self.inbuffer = '' # empty inbuffer

	def handle_get(self, args):
		data = DATA_STORE.get(args[1])
		if data is None:
			self.outbuffer = "NO\n"
		else:
			self.outbuffer = data + "\n"

	def handle_put(self, args):
		DATA_STORE.put(args[1], args[2])
		self.outbuffer = "OK\n"

	def handle_close(self):
		dkv_debug('Disconnected from %s' % (str(self.getpeername())))
		self.close()

	def writable(self):
		self.create_buffers()
		return (len(self.outbuffer) > 0)

	def handle_write(self):
		self.create_buffers()
		sent = self.send(self.outbuffer)
		self.outbuffer = self.outbuffer[sent:]


class DkvServer(asyncore.dispatcher):
	def __init__(self, port = 9000):
		asyncore.dispatcher.__init__(self)
		self.port = port
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.bind(("", port))
		self.listen(5)
		dkv_debug('Receiving incoming connections on port %d' % port)
		datadir = dkv_config.get('server','datadir')
		if not datadir:
			datadir = 'data'
		max_buckets = dkv_config.get('server', 'buckets')
		if not max_buckets:
			max_buckets = 10
		global DATA_STORE
		DATA_STORE = DkvDataStore(datadir, int(max_buckets))

	def handle_accept(self):
		channel, addr = self.accept()
		dkv_debug('Incoming connection from %s' % str(addr))
		DkvNetHandler(channel)

	def clean(self):
		self.close()
		global DATA_STORE
		DATA_STORE.close_all()
