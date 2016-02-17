#coding: utf-8

# DSP16 EX1
# Jenny Tyrväinen
# 013483708

import lnode
import random
import socket
import sys
import time
import eventcounter

""" Program to simulate, how Lamport Clocks work. This file contains the main and uses classes EventCounter and LNode."""

if len(sys.argv) < 2:
	print "Usage: program congfiguration_file line"
	sys.exit()

conf_file = sys.argv[1]

hosts = open(conf_file)
nodes = {}

events = eventcounter.EventCounter()

for idx, line in enumerate(hosts):
	l = line.split()
	if not l:
		continue

	# Take correct row for this node from the conf file.
	if idx == int(sys.argv[2]):
		thisnode = lnode.LNode(events, int(l[0]), l[1], int(l[2]))
		continue

	nodes[int(l[0])] = lnode.LNode(events, int(l[0]), l[1], int(l[2]))

# Time to start all the nodes needed, hopefully.
time.sleep(10)
thisnode.listen()

while events.getValue() <= 100:
	# Choose randomly if a local event happens or a message is sent
	if random.randint(0,1):
		thisnode.localEvent()

	else:
		# Choose randomly, where to send
		target = nodes[random.choice(nodes.keys())]
		try:
			thisnode.send(target.getID(), target.getHost(), target.getPort())
		except socket.error as e:
			pass

