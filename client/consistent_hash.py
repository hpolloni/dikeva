# --------------- UNIMPLEMENTED -------------


import md5

class ConsistentHash:
	def __init__(self, number_of_replicas, nodes):
		self.circle = {}
		self.number_of_replicas = number_of_replicas
		for node in nodes:
			self.add(node)

	def add(self, node):
		for i in xrange(0, self.number_of_replicas):
			m5 = md5.new(node + i)

	public void add(T node) {
		for (int i = 0; i < numberOfReplicas; i++) {
			circle.put(hashFunction.hash(node.toString() + i),
				node);
		}
	}

	public void remove(T node) {
		for (int i = 0; i < numberOfReplicas; i++) {
			circle.remove(hashFunction.hash(node.toString() + i));
		}
	}

	public T get(Object key) {
		if (circle.isEmpty()) {
			return null;
		}
		int hash = hashFunction.hash(key);
		if (!circle.containsKey(hash)) {
			SortedMap<Integer, T> tailMap =
				circle.tailMap(hash);
			hash = tailMap.isEmpty() ?
						 circle.firstKey() : tailMap.firstKey();
		}
		return circle.get(hash);
	}

}
