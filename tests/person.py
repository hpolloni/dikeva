
class Person:
	def __init__(self, name='', last_name='', age=0):
		self.name = name
		self.last_name = last_name
		self.age = age
	def unserialize(self, data):
		self.name = data['name']
		self.last_name = data['last_name']
		self.age = data['age']
