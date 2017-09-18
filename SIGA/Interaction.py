
import Gene, Parameters, random, math, copy

#GAME ENGINE, SHOULD HAVE BEEN CALLED LIKE THIS, BUT OH WELL...
class Interaction:

	#game parameters, the letters represents the utility function received by playing:
	#
	#	R: reward
	#	T: temptation
	#	P: punishment
	#	S: sucker
	#
	def __init__(self, param = Parameters):
		#discount factor
		self.beta = 0.9
		self.param = param
		#batch size
		self.batch_size = int(self.param.popNum * 0.5)
		#starting payment matrix (original Dillema)
		self.R = 3
		self.T = 5
		self.S = 1
		self.P = 0
		#maximum payoff
		self.maximum_payoff = 0
		max_num = max(self.R, self.T, self.P, self.S)
		for i in range(0, param.popNum):
			for k in range(0,self.param.numRounds):
				self.maximum_payoff += math.pow(self.beta,k+1)* max_num

	#change game behavior according to chosen number (I used a number notation in order to leave an easier implementation for stochastic games)
	def change(self, type):

		#Prisoner's Dillema
		if type == 1:
			self.R = 3
			self.T = 5
			self.S = 1
			self.P = 0
		#Stag Hunt
		elif type == 2:
			self.R = 5
			self.T = 3
			self.S = 1
			self.P = 0
		#Hawk Dove
		elif type == 3:
			self.R = 3
			self.T = 5
			self.S = 0
			self.P = 1
		#Harmonic Games
		elif type == 4:
			self.R = 5
			self.T = 3
			self.S = 0
			self.P = 1
		#update payoff
		max_num = max(self.R, self.T, self.P, self.S)
		for k in range(0,self.param.numRounds):
			self.maximum_payoff += math.pow(self.beta,k+1)* max_num
	#standard game without any sthocasticity
	def socialGame(self, bestval, p1 = Gene, p2 = Gene):
		p1_socialFitness_temp = 0
		p2_socialFitness_temp = 0
		for k in range(0,self.param.numRounds):
			p1move = p1.play()
			p2move = p2.play()
			#model all possible moves (both C, both D, one D and one C)
			#both cooperate
			if(p1move == "C" and p2move == "C"):
				p1_socialFitness_temp+= math.pow(self.beta,k+1) * self.R
				p2_socialFitness_temp+= math.pow(self.beta,k+1) * self.R
			#player1 cooperate and player 2 defect
			elif(p1move == "C" and p2move == "D"):
				p1_socialFitness_temp+= math.pow(self.beta,k+1) * self.S
				p2_socialFitness_temp+= math.pow(self.beta,k+1) * self.T
			#player 1 defect and player 2 cooperate
			elif(p1move == "D" and p2move == "C"):
				p1_socialFitness_temp+= math.pow(self.beta,k+1) * self.T
				p2_socialFitness_temp+= math.pow(self.beta,k+1) * self.S
			#both defect
			elif(p1move == "D" and p2move == "D"):
				p1_socialFitness_temp+= math.pow(self.beta,k+1) * self.P
				p2_socialFitness_temp+= math.pow(self.beta,k+1) * self.P

		#calculate normalized fitness
		p1normfit = (p1_socialFitness_temp / self.maximum_payoff) * bestval

		#return fitnesses as a list
		return p1normfit

               
     #whole social interaction process
	def socialInteraction(self, bestval, population):
    	
    	#initilize random list
		index = random.sample(range(0, int(self.param.popNum)), int(self.param.popNum))

		#copy of the list 
		#index_copy = copy.copy(index)

		#EACH INDIVIDUAL INTERACTS WITH EACH OTHER IN THE POPULATION
		#iterate every member of the population with everyone else
		#for i in range(0, int(self.param.popNum)-1):
		#	tmp_ind = index_copy.pop(-1)
		#	for j in range(0, range(0, len(index_copy))):
		#		for k in range(0, self.param.numGames):
		#			#only the player who is interacting with the others will receive the payment
		#			population[index[i]].socialFitness +=self.socialGame(bestval, population[index[i]], population[tmp_ind[j]])
		#	index_copy.append(tmp_ind)


		#for i in range(0, int(self.param.popNum)-2, 2):

			#population[index[i]].socialFitness, population[index[i+1]].socialFitness =self.socialGame(bestval, population[index[i]], population[index[i+1]])
    	#EACH INDIVIDUAL INTERACTS WITH A BATCH OF THE POPULATION, TO MAKE IT INTERACT WITH EVERYONE, SET BATCH_SIZE TO NUMPOP
		for i in range(0, int(self.param.popNum)-1):
			#sort other players
			players = random.sample(list(index[:i]+index[i:]),self.batch_size)
			#iterate for the list
			for j in range(0, len(players)):
				#iterate for each game: 
				for k in range(0, self.param.numGames):
				#only the player who is interacting with the others will receive the payment
					population[index[i]].socialFitness +=self.socialGame(bestval, population[index[i]], population[players[j]])