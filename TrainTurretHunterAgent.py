
from TurretHunter import *

from Agent import *

import time

TOTAL_TrainTime = 10**5

def TrainExperiment():
	TrainTime = 0
    
	TrainHistory = []
	
	ScoreCheck = deque()
	NotQuit = True
	
	#Create our PongGame instance
	TheGame = TurretHunterGame()
    # Initialise Game
	TheGame.InitialDisplay()
	#
	#  Create our Agent (including DQN based Brain)
	TheAgent = Agent()

	BestAction = 0
	
	# Get an Initial State
	[InitialScore,InitialScreenImage]= TheGame.PlayNextMove(BestAction)

	InitialGameImage = TheAgent.ProcessGameImage(InitialScreenImage)

	GameState = np.stack((InitialGameImage, InitialGameImage, InitialGameImage, InitialGameImage), axis=2)
	# Keras expects shape 1x40x40x4
	GameState = GameState.reshape(1, GameState.shape[0], GameState.shape[1], GameState.shape[2])
	#Main Experiment Loop 
	while ((TrainTime < TOTAL_TrainTime) and NotQuit):    
	
		# First just Update the Game Display
		#if TrainTime % 100 == 0:
		#	TheGame.UpdateGameDisplay(TrainTime,TheAgent.epsilon)

		# Determine Next Action From the Agent
		BestAction = 0

		# 1 Random via epsilon decay -- OR -- numpy.argmax(model.predict(S))
		BestAction = TheAgent.FindBestActionTrain(GameState)
		
		#  Now Apply the Recommended Action into the Game 	
		[ReturnScore,NewScreenImage]= TheGame.PlayNextMove(BestAction)
		
		# Need to process the returned Screen Image, 
		NewGameImage = TheAgent.ProcessGameImage(NewScreenImage);
		
		# Now reshape Keras expects shape 1x40x40x1
		NewGameImage = NewGameImage.reshape(1, NewGameImage.shape[0], NewGameImage.shape[1], 1)
		
		#Now Add the new Image into the Next GameState stack, using 3 previous capture game images 
		NextState = np.append(NewGameImage, GameState[:, :, :, :3], axis=3)
		
		# Capture the Sample [S, A, R, S"] in Agent Experience Replay Memory 
		TheAgent.AbsorbSample((GameState,BestAction,ReturnScore,NextState))
		
		#  Now Request Agent to DQN Train process  Against Experience
		TheAgent.Process()
		
		# Move State On
		GameState = NextState
		
		# Move TrainTime Click
		TrainTime = TrainTime+1        

		if TrainTime % 500 == 0:
			print("Saving weights at: ", TrainTime)
			TheAgent.SaveBestWeights(TrainTime)
			# Complete the Game Loop
			#NotQuit = False

def main():
    #
	# Main Method Just Play our Experiment
	a = time.time()
	TrainExperiment()
	b = time.time()
	print("It took {}".format((b-a), "seconds to train") )

	# =======================================================================
if __name__ == "__main__":
    main()