from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *
import csv,os
import dot_parser
from pyretic.examples.pyretic_switch import ActLikeSwitch

class Firewall(DynamicPolicy):
        def __init__(self,inputList):
                super(Firewall,self).__init__()

                self.query=packets(limit=1,group_by=['srcmac'])

                print "***query***"
		self.inputList = inputList

                self.policy= self.query 
                #self.policy=self.queryL
                print "**policy**"

                self.query.register_callback(self.checkIPAddr)


        def checkIPAddr(self,pkt):
		dropPackets= none
		for macList in self.inputList:
			dropPackets = dropPackets | (match(srcmac=MAC(macList[0]),dstmac=MAC(macList[1]))) | (match(srcmac=MAC(macList[1]),dstmac=MAC(macList[0])))
			#cond1  = ~(match(srcmac=macList[0],dstmac=macList[1]))
			#cond2 = ~(match(srcmac=macList[1],dstmac=macList[0]))
			#self.policy = self.policy +((cond1 & cond2) >> identity)
		self.policy= ~ dropPackets

def readInput(inputFile):
	
	f=open(inputFile,'r')
	macList=list()

	for line in f:
		mlist=line.strip("\n").split(",")
		macList.append(mlist)
	return macList		

def main():
	dropped = none
	policy_file = "/home/mininet/pyretic/pyretic/examples/firewallRules.csv"
	inputList=readInput(policy_file)
	print inputList
	for maclist in inputList:
		dropped = dropped | match(srcmac=MAC(maclist[0]),dstmac=MAC(maclist[1])) | match(srcmac=MAC(maclist[1]),dstmac=MAC(maclist[0]))
	allowed = ~dropped
	return Firewall(inputList)  >> ActLikeSwitch()
