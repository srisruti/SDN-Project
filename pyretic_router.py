from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *


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
	
	return Router()
