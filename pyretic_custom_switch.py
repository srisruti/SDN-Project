from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *

class LoadBalancerSwitch(DynamicPolicy):
    def __init__(self):
        super(LoadBalancerSwitch, self).__init__()
        # Set up the initial forwarding behavior for your mac learning switch to flood 
        # all packets
        print "In ActLikeSwitch function.."
        print "Forwarding......"

        self.forward = flood()
        print "Forward:",self.forward
#       print "Source MAC:",srcmac
#       print "Switch:",switch

        # Set up a query that will receive new incoming packets
	q=packets(limit=1,group_by=['dstip'])
        self.query = packets(limit=1,group_by=['srcmac','switch'])
        print "Flood Query:",self.query
        # Set the initial internal policy value (each dynamic policy has a member 'policy'
        # when this member is assigned, the dynamic policy updates itself)
        self.policy = self.forward + self.query

        print "Policy:",self.policy
	q.register_callback(self.modify_dest_IP)
        self.query.register_callback(self.learn_from_a_packet)

    def modify_dest_IP(self,pkt):
	
	if_(match(dstip=IPAddr('10.0.0.3')),modify(dstip=IPAddr('10.0.0.2')),modify(dstip=pkt['dstip']))

    def learn_from_a_packet(self, pkt):
        # Set the forwarding policy
        print "In Learn_From_A_Packet function.."
        print "Source MAC:",pkt['srcmac']
        print "Switch:",pkt['switch']
        print "Inport:",pkt['inport']
        #print "DestMac:",dstmac
        #print "Switch:",switch
        self.forward = if_(match(dstmac=pkt['srcmac'],
                                 switch=pkt['switch']), fwd(pkt['inport']),
                           self.forward)  # hint use 'match', '&', 'if_', and 'fwd' 
	
        # Update the policy
        self.policy = self.forward + self.query # hint you've already written this
        print self.policy

def main():
	return LoadBalancerSwitch()


