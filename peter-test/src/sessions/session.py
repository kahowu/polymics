from . import basicsession

class Session:
	def __init__(self,
	             userid    = None, # not a user
	             expire    = None,
	             auth      = None,
	             prefix    = None,
	             config    = None,
	             node      = None,
	             ):
		self.sessionid = None
		self.userid    = userid
		self.expire    = expire
		self.auth      = auth
		self.prefix    = prefix
		self.config    = config
		self.node      = node
		
		if self.prefix == None:
			self.prefix = tuple()
	
	# no one should use this function outside this file
	def set_sessionid(self, k):
		self.sessionid = k
	
	def get_sessionid(self):
		return self.sessionid
	
	def authenticate(self, packet):
		if self.auth:
			return self.auth(packet)
		else:
			return True
	
	def process(self, packet, hub):
		if not self.authenticate(packet):
			return hub.log("session authentication fail")
		
		packet.session = self
		
		node = self.node
		for i in packet.path:
			if node != None:
				node = node.child_node(i)
		
		if node == None:
			return hub.log("path finding fail")
		
		node.process(packet, hub)