import Queue



def init():
# Outgoing message queues (socket:Queue)
	global message_que
	message_queue = Queue.Queue()
