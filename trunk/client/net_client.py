import asyncore, socket

# TODO: better error handling

# state = 1 : sending command
# state = 2 : sending done, receiving
# if receiving done, send the other command (state = 1) (or close if no more commands)
class DkvNetClient(asyncore.dispatcher):
	def __init__(self, addr, commands):
		self.commands = commands
		self.responses = []
		self.current_command = 0
		self.outbuffer = self.commands[self.current_command] + "\n"
		self.inbuffer = ''
		self.state = 1
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect( addr )

	def handle_connect(self):
		pass

	def handle_close(self):
		self.close()

	def handle_read(self):
		if self.state == 2:
			self.inbuffer += self.recv(1)
			if self.inbuffer.endswith("\n"):
				# done receiving
				self.responses.append(self.inbuffer.strip())
				# start another command or close if no more commands
				self.current_command += 1
				if self.current_command < len(self.commands):
					# next command
					self.outbuffer = self.commands[self.current_command] + "\n"
					self.state = 1
				else:
					# close, no more commands
					self.close()

	def writable(self):
		return (len(self.outbuffer) > 0)

	def handle_write(self):
		if self.state == 1:
			sent = self.send(self.outbuffer)
			self.outbuffer = self.outbuffer[sent:]
			if not self.writable():
				# probably done writing, let's read
				self.state = 2

	def run(self):
		asyncore.loop()
