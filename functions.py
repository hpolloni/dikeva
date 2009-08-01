import urllib
import pickle
import md5
import os

def dkv_encode(data):
  return urllib.quote(pickle.dumps(data))

def dkv_decode(s):
  return pickle.loads(urllib.unquote(s))

def dkv_choose(key, buckets):
  m = md5.new(key)
  hash_value = long(m.hexdigest(), 16)
  return (hash_value % buckets)

def dkv_filename_for_key(key):
  # OPTIONS!!
  return os.path.join('data', 'bucket' + str(dkv_choose(key, 100)))