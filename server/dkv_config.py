import ConfigParser

config = ConfigParser.ConfigParser()

def read(filename):
	global config
	config.read(filename)

def get(section, variable):
	global config
	try:
		value = config.get(section, variable)
		return value
	except ConfigParser.NoSectionError:
		return False
	except ConfigParser.NoOptionError:
		return False
