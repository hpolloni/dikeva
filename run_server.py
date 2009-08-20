from server import DkvServer
from server import dkv_config
import asyncore
import getopt
import sys

VERSION = '0.1.0'

def usage():
	print 'Distributed Key Value Server v' + VERSION
	print ''
	print '-h, --help: Display this information'
	print '-c, --config config_file: Set the config file for the server to this'

# main for server
def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'hc', ['help','config=',])
	except getopt.GetoptError:
		usage()
		return -1
	config_file = 'server.ini'
	for o, a in opts:
		if o in ('-c', '--config'):
			config_file = a
		if o in ('-h', '--help'):
			usage()
			return 0
	dkv_config.read(config_file)
	port = dkv_config.get("network","port")
	if not port:
		port = 9000
	try:
		s = DkvServer(int(port))
		asyncore.loop()
	except KeyboardInterrupt:
		print 'Cleaning things up'
		s.clean()

if __name__ == '__main__':
	main()
