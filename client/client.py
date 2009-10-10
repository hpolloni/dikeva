import urllib
import pickle
from net_client import DkvNetClient
from hash_table import DkvHashTable

class DkvClient:
	def __init__(self, HashTable = DkvHashTable):
		self.servers = HashTable()

	def add_server(self, addr):
		# check that addr is a tuple
		self.servers.add(addr)

	def encode(self, data):
		try:
			real_data = data.__dict__
		except AttributeError:
			real_data = data
		return urllib.quote(pickle.dumps(real_data))

	def decode(self, s):
		return pickle.loads(urllib.unquote(s))

	def get(self, key):
		commands = []
		commands.append("GET " + key)
		commands.append("EXIT")
		dkvnet = DkvNetClient(self.servers.get(key), commands);
		dkvnet.run()
		if dkvnet.responses[0].startswith('NO'):
			return None
		return self.decode(dkvnet.responses[0])

	def put(self, key, data):
		commands = []
		commands.append("PUT " + key + " " + self.encode(data))
		commands.append("EXIT")
		dkvnet = DkvNetClient(self.servers.get(key), commands)
		dkvnet.run()
