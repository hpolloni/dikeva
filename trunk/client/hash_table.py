
try:
	import hashlib
	md5_new = hashlib.md5
except ImportError:
	import md5
	md5_new = md5.new

class DkvHashTable:
	def __init__(self):
		self.nodes = []
	def add(self, key):
		self.nodes.append(key)
	def get(self, key):
		m = md5_new(key)
		hash_value = long(m.hexdigest(), 16)
		return self.nodes[hash_value % len(self.nodes)]
