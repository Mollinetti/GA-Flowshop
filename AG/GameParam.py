
class GameParam:

	#game parameters, with the letter being the utility function received by:
	#
	#	R: reward
	#	T: temptation
	#	P: punishment
	#	S: sucker
	#
	def __init__(self, type):
		if type == 'PD':
			self.R = 3
			self.T = 5
			self.S = 1
			self.P = 0
		elif type == 'SH':
			self.R = 5
			self.T = 3
			self.S = 1
			self.P = 0
		elif type == 'HD':
			self.R = 3
			self.T = 5
			self.S = 0
			self.P = 1
		elif type == 'Harmonic':
			self.R = 5
			self.T = 3
			self.S = 0
			self.P = 1