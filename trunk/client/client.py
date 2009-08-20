import asyncore, socket
import urllib
import pickle
import md5

# need to replace this with consistent hash
def dkv_choose(key, buckets):
	m = md5.new(key)
	hash_value = long(m.hexdigest(), 16)
	return (hash_value % buckets)

def dkv_encode(data):
	return urllib.quote(pickle.dumps(data))

def dkv_decode(s):
	return pickle.loads(urllib.unquote(s))

# state = 1 : sending command
# state = 2 : sending done, receiving
# if receiving done, send the other command (state = 1) (or close if no more commands)

class DkvNetClient(asyncore.dispatcher):
	def __init__(self, addr, commands):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( addr )
		self.commands = commands
		self.responses = []
		self.current_command = 0
		self.outbuffer = self.commands[self.current_command] + "\n"
		self.inbuffer = ''
		self.state = 1

	def handle_connect(self):
		pass

	def handle_close(self):
		self.close()

	def handle_read(self):
		if self.state == 2:
			self.inbuffer += self.recv(1)
			if self.inbuffer.endswith("\n"):
				# done receiving
				self.responses.append(self.inbuffer.strip())
				# start another command or close if no more commands
				self.current_command += 1
				if self.current_command < len(self.commands):
					# next command
					self.outbuffer = self.commands[self.current_command] + "\n"
					self.state = 1
				else:
					# close, no more commands
					self.close()

	def writable(self):
		return (len(self.outbuffer) > 0)

	def handle_write(self):
		if self.state == 1:
			sent = self.send(self.outbuffer)
			self.outbuffer = self.outbuffer[sent:]
			if not self.writable():
				# probably done writing, let's read
				self.state = 2

class DkvClient:
	def __init__(self):
		self.servers = []
	def add_server(self, addr):
		self.servers.append(addr)
	def get(self, key):
		commands = []
		commands.append("GET " + key)
		commands.append("EXIT")
		dkvnet = DkvNetClient(self.choose_server(key), commands);
		asyncore.loop()
		if dkvnet.responses[0].startswith('NO'):
			return None
		return dkv_decode(dkvnet.responses[0])
	def put(self, key, data):
		commands = []
		commands.append("PUT " + key + " " + dkv_encode(data))
		commands.append("EXIT")
		dkvnet = DkvNetClient(self.choose_server(key), commands)
		asyncore.loop()
	def choose_server(self,key):
		choice = dkv_choose(key, len(self.servers))
		return self.servers[choice]
