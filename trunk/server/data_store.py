import bsddb
import os
import dkv_config
from dkv_functions import dkv_debug

try:
	import hashlib
	md5_new = hashlib.md5
except ImportError:
	import md5
	md5_new = md5.new

def naive_choose(key, buckets):
	m5 = md5_new(key)
	hash_value = long(m5.hexdigest(), 16)
	return (hash_value % buckets)

# TODO: delete least "getted"
class DkvCache:
	CACHE = {}
	def __init__(self, cache_max, use_cache):
		self.useit = use_cache
		self.cache_max = cache_max
		self.mbytes_used = 0

	def key_exists(self,key):
		if not self.useit:
			return False
		return key in self.__class__.CACHE

	def get(self,key):
		if not self.useit:
			return None
		return self.__class__.CACHE[key]

	def put(self, key, data):
		if self.useit:
			self.mbytes_used += float(len(data)) / 1000000.0
			if self.mbytes_used < self.cache_max:
				self.__class__.CACHE[key] = data
			else:
				dkv_debug('DATA_CACHE: Cache is full')

class DkvDataStore:
	def __init__(self, datadir, max_buckets):
		self.dbs = []
		dkv_debug('DATA_STORE: using datadir ' + datadir)
		for i in xrange(max_buckets):
			dbname = os.path.join(datadir, 'bucket' + str(i))
			dkv_debug('DATA_STORE: loading local db ' + dbname + ' ...', False)
			db = bsddb.btopen(dbname, 'c')
			self.dbs.append(db)
			dkv_debug(' done')
		dkv_debug('DATA_STORE: all buckets loaded')
		cache_max = dkv_config.get('cache', 'max_mbytes')
		use_cache = dkv_config.get('cache', 'use_cache')
		self.cache = DkvCache(int(cache_max), use_cache)

	def get(self, key):
		dkv_debug('DATA_STORE: fetching key ' + key) 
		if self.cache.key_exists(key):
			dkv_debug('DATA_STORE: cache hit for key ' + key)
			return self.cache.get(key)
		choose = naive_choose(key, len(self.dbs))
		dkv_debug('DATA_STORE: cache miss for key ' + key + ', fetching from bucket'+str(choose))
		db = self.dbs[choose]
		if key in db:
			data = db[key]
			dkv_debug('DATA_STORE: key '+key+' found on db, making it available on cache')
			self.cache.put(key, data)
			return data
		dkv_debug('DATA_STORE: key ' + key + ' not found on db')
		return None

	def put(self, key, data):
		dkv_debug('DATA_STORE: storing key ' + key + ' on cache')
		self.cache.put(key, data)
		choose = naive_choose(key, len(self.dbs))
		dkv_debug('DATA_STORE: storing key ' + key + ' on bucket'+str(choose)+'...', False)
		db = self.dbs[choose]
		db[key] = data
		db.sync()
		dkv_debug('done')

	def close_all(self):
		dkv_debug('DATA_STORE: closing all buckets...',False)
		for db in self.dbs:
			db.close()
		dkv_debug('done')

