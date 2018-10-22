
from TurretHunter import *
from Agent import *


TOTAL_GAMETIME = 5000 

def PlayGame():
    GameTime = 0
    
    GameHistory = []
    
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
    
    #
    while (GameTime < TOTAL_GAMETIME):
    
        # First just Update the Game Display
        #if TrainTime % 100 == 0:
        #   TheGame.UpdateGameDisplay(TrainTime,TheAgent.epsilon)

        # Determine Next Action From the Agent
        BestAction = 0

        # 1 Random via epsilon decay -- OR -- numpy.argmax(model.predict(S))
        BestAction = TheAgent.FindBestActionTrain(GameState)
        
        #  Now Apply the Recommended Action into the Game   
        [ReturnScore,NewScreenImage]= TheGame.PlayNextMoveTest(BestAction)
        
        # Need to process the returned Screen Image, 
        NewGameImage = TheAgent.ProcessGameImage(NewScreenImage);
        
        # Now reshape Keras expects shape 1x40x40x1
        NewGameImage = NewGameImage.reshape(1, NewGameImage.shape[0], NewGameImage.shape[1], 1)
        
        #Now Add the new Image into the Next GameState stack, using 3 previous capture game images 
        NextState = np.append(NewGameImage, GameState[:, :, :, :3], axis=3)
        
        GameState = NextState

        # Move GameTime Click
        GameTime = GameTime+1
def main():
    #
    # Main Method Just Play our Game
    PlayGame()

    # =======================================================================
if __name__ == "__main__":
    main()