import bsddb
from functions import dkv_filename_for_key

class DkvDataStore:
  CACHE = {}
  def __init__(self):
    pass
  def get(self, key):
    if key in DkvDataStore.CACHE:
      return DkvDataStore.CACHE[key]
    db = bsddb.btopen(dkv_filename_for_key(key))
    if key in db:
      return db[key]
    return None
  def put(self, key, data):
    DkvDataStore.CACHE[key] = data # HOW MUCH SHOULD BE OPTIONAL
    db = bsddb.btopen(dkv_filename_for_key(key))
    db[key] = data
    db.sync()

