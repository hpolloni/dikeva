
try:
	import hashlib
	md5_new = hashlib.md5
except ImportError:
	import md5
	md5_new = md5.new

class DkvHashTable:
	def __init__(self):
		self.nodes = []

	def add(self, addr):
		self.nodes.append(addr)

	def remove(self, addr):
		self.nodes.remove(addr)

	def get(self, key):
		m = md5_new(key)
		hash_value = long(m.hexdigest(), 16)
		return self.nodes[hash_value % len(self.nodes)]
