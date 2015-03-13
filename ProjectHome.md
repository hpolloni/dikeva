# Introduction #
Dikeva is a distributed data store aiming to be as simple and easy to deploy as possible. Using  Berkeley DB as data storage and written in Python for easy deployment.

# What are the requirements for dikeva? #
The only requirement at the moment is a correct Python 2.X installation.

# How does it work? #
  1. Start the server on the nodes you want to use as data storage. So, for each server do:
```
   $ python run_server.py --config config-sample.cfg
```
  1. Use the easy to use python API to save or fetch objects on the data storage.
```
   from dikeva.client import DkvClient
   
   d = DkvClient()
   # do this for each node
   d.add_server((addr, port))
   d.put(key, data)
   d.get(key)
```

# Philosophies #
  1. Cross platform
  1. Keep things simple for the user
  1. Concurrency over Consistency

# Roadmap #
  * Object storage interface on client (data only)
  * multiget/multiput (on client: get/put queue)
  * Consistent hashing scheme
  * Replication (on nodes)
  * Python 3 support