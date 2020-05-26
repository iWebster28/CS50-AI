#Exceptions

class Error(Exception):
	"""Base class"""
	pass

#class InputError(Error):
	"""Input errors"""

class TransitionError(Error):
	"""Invalid state transition"""

	def __init__(self, previous, next, message):
		self.previous = previous
		self.next = next
		self.message = message