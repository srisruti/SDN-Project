from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *

class LoadBalancer(DynamicPolicy):
	def __init__(self):
		super(LoadBalancer,self).__init__()
		self.queryL=packets(limit=1,group_by=['srcip'])
		
		print "***query***"

		self.policy= if_( (match(srcip=IPAddr('10.0.0.100')) | match(dstip=IPAddr('10.0.0.100'))) , self.queryL, identity)
		#self.policy=self.queryL
		print "**policy**"

		self.queryL.register_callback(self.modifyDestIP)
		

	def modifyDestIP(self,pkt):
		print "********Modify destIP*******"
		self.policy= (match(srcip=IPAddr('10.0.0.1'), dstip=IPAddr('10.0.0.100')) >> modify(dstip=IPAddr('10.0.0.3'))) + (match(srcip=IPAddr('10.0.0.2'),dstIP=IPAddr('10.0.0.100')) >>  modify(dstip=IPAddr('10.0.0.4'))) + (match(srcip=IPAddr('10.0.0.3'),dstip=IPAddr('10.0.0.1')) >> modify(srcip=IPAddr('10.0.0.100'))) + (match(dstip=IPAddr('10.0.0.2'), srcip=IPAddr('10.0.0.4')) >> modify(srcip=IPAddr('10.0.0.100'))) 
		
class Router(DynamicPolicy):
	def __init__(self):
		print "===== routing started ======"
		super(Router,self).__init__()

		self.forward=flood()
		
		self.query= packets(limit=1,group_by=['srcip'])

		self.policy= self.forward + self.query

		self.query.register_callback(self.route)

	def route(self,pkt):
		self.forward= (match(dstip=IPAddr('10.0.0.1')) >> fwd(1)) + (match(dstip=IPAddr('10.0.0.2')) >> fwd(2)) + (match(dstip=IPAddr('10.0.0.3')) >> fwd(3)) + (match(dstip=IPAddr('10.0.0.4')) >> fwd(4))
		#self.forward=if_(match(dstip=pkt['srcip']),fwd(pkt['inport']),self.forward)

		self.policy= self.forward + self.query

		
		

def main():
	return LoadBalancer() >> Router()
