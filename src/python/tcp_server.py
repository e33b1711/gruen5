#!/usr/bin/env python

import select
import socket
import sys
import Queue


def init():

	global server
	global inputs
	global outputs
	global message_queue_out
	global message_queue_in

	# Create a TCP/IP socket
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setblocking(0)

	# Bind the socket to the port
	server_address = ('192.168.178.54', 1000)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	server.bind(server_address)

	# Listen for incoming connections
	server.listen(5)


	# Sockets from which we expect to read
	inputs = [ server ]

	# Sockets to which we expect to write
	outputs = [ ]

	message_queue_in=Queue.Queue()
	message_queue_out=Queue.Queue()


	

def step():

	global server
	global inputs
	global outputs
	global message_queue_out
	global message_queue_in


	if inputs:

		# Wait for at least one of the sockets to be ready for processing
		readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.0001)


	# Handle inputs
	for s in readable:

		if s is server:
			# A "readable" server socket is ready to accept a connection
			connection, client_address = s.accept()
			print >>sys.stderr, 'new connection from', client_address
			connection.setblocking(0)
			inputs.append(connection)
			outputs.append(connection)
			


		else:
			try:
				data = s.recv(1024)

				if data:
				# A readable client socket has data
				#print >>sys.stderr, 'received "%s" from %s' % (data, s.getpeername())
				# Add output channel for response
				#if s not in outputs:
				#	outputs.append(s)
					message_queue_in.put(data)

				else:
				# Interpret empty result as closed connection
				#print >>sys.stderr, 'closing', client_address, 'after reading no data'
				# Stop listening for input on the connection
					if s in outputs:
						outputs.remove(s)
						inputs.remove(s)
						s.close()
			except socket.error, (value,message): 
                    		print('Scoket error.')
				if s in outputs:
					outputs.remove(s)
					inputs.remove(s)
					s.close()


			


    # Handle outputs
	for s in writable:
		try:
			next_msg = message_queue_out.get_nowait()
		except Queue.Empty:
			# No messages waiting so stop checking for writability.
			#print >>sys.stderr, 'output queue for', s.getpeername(), 'is empty'
            		#outputs.remove(s)
			pass
		else:
			#print >>sys.stderr, 'sending "%s" to %s' % (next_msg, s.getpeername())
			try:			
				s.send(next_msg)
			except socket.error:
				print('No connection to client.')



    # Handle "exceptional conditions"
	for s in exceptional:
		print >>sys.stderr, 'handling exceptional condition for', s.getpeername()
		# Stop listening for input on the connection
		inputs.remove(s)
		if s in outputs:
			outputs.remove(s)
		s.close()






