'''
This module was done with the help of the following references:

https://github.com/JulesVerny/PongConvolutionalDQN
https://www.amazon.com/Deep-Reinforcement-Learning-Hands-Q-networks/dp/1788834240
https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/

'''

from keras.models import Sequential
from keras.layers import *
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import *

import cv2
import skimage
from skimage import color

import random
import numpy as np
from collections import deque


#Resizing for model training
IMGHEIGHT = 50
IMGWIDTH = 50
IMGHISTORY = 4

EPSILON_DECAY_LAST_FRAME = 10**5
EPSILON_START = 1.0
EPSILON_FINAL = 0.02

#number of actions the agent can do
NUM_ACTIONS   = 5
OBSERVEPERIOD = 2500

EXPERIENCE_REPLAY_CAPACITY = 10000

BATCH_SIZE = 32
GAMMA = 0.975

class Agent:
    def __init__(self):

        self.domination = True
        self.model = self.createModel(NUM_ACTIONS)

        self.ExperienceReplay = deque(maxlen=EXPERIENCE_REPLAY_CAPACITY)
        
        self.steps = 0
        self.epsilon = 1.0

        self.frame_idx = 0

    def LoadTrainedModel(self):
        self.model.load_weights("TurretHunterModelWeights10000.h5")
        self.model.compile(loss='mse',optimizer='rmsprop')
        self.epsilon = 0.0
        
    def ProcessGameImage(self, RawImage):
        base = np.copy(RawImage)
        img = color.rgb2gray(base)
        #ReducedImage = cv2.cvtColor(base, COLOR_RGB2GREY)
        GameImage = cv2.resize(img, (50, 50),interpolation=cv2.INTER_AREA )
               
        #Initial gamestate for 
        #GameState = np.stack((InitialGameImage, InitialGameImage, InitialGameImage, InitialGameImage), axis=2)
        # Keras expects shape 1x40x40x4
        #GameState = GameState.reshape(1, GameState.shape[0], GameState.shape[1], GameState.shape[2])
        return GameImage

    def createModel(self, NUM_ACTIONS):
        print("Creating Model")
        model = Sequential()
        model.add(Conv2D(32, kernel_size=8, strides=(4, 4), input_shape=(IMGHEIGHT, IMGWIDTH, IMGHISTORY), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, kernel_size=4, strides=(2, 2), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(64, kernel_size=3, strides=(1, 1), padding='same'))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(512))
        model.add(Activation('relu'))
        model.add(Dense(units=NUM_ACTIONS, activation='linear'))
        model.compile(loss='mse', optimizer='rmsprop')
        print("Done Creating Model")
        return model

    def getActuationCommand(self, observation):
        #observation = np.array(self.ProcessGameImage(observation) )
        #print("observation.shape", observation.shape)
        q_value = self.model.predict(observation)
        return np.argmax(q_value)

    def play_train_step(self, epsilon):
        '''
        plays a step in the training step, outputs an
        Experience()

        Input: epsilon is the exploration/exploitation parameter 
        '''

        pass
    def FindBestActionTrain(self,state):
            
        if np.random.random() < self.epsilon:
            # pick a random action
            action = random.randint(0,NUM_ACTIONS - 1)
        else:
            action = np.argmax(self.model.predict(state))
        return action
    
    def FindBestActionTest(self, state):
        q_val = self.model.predict(state)
        return np.argmax(q_val)

    def AbsorbSample(self, sample):
        '''
        Input: A sample, (s, a, r, s') 
        '''
        self.ExperienceReplay.append(sample)

        self.steps += 1

        if self.steps > OBSERVEPERIOD:
            # Epsilon-greedy decay
            self.epsilon = max(EPSILON_FINAL, EPSILON_START - (self.steps - OBSERVEPERIOD) / EPSILON_DECAY_LAST_FRAME)

    def Process(self):
        '''
        Train on a BATCH_SIZE sample, of experiences of the form: (s, a, r, s') 
        '''
        #do a training run only if we've sampled enough steps from the game
        if self.steps > OBSERVEPERIOD:
            #sample BATCH_SIZE experiences
            minibatch = random.sample(self.ExperienceReplay,BATCH_SIZE)

            inputs = np.zeros((BATCH_SIZE, IMGHEIGHT,IMGWIDTH ,IMGHISTORY))   #BatchSize, 40, 40, 4
            targets = np.zeros((inputs.shape[0], NUM_ACTIONS)) 
        
            Q_sa =0

            for i in (BATCH_SIZE):
                state_t  = minibatch[i][0]
                action_t = minibatch[i][1]   #This is action index
                reward_t = minibatch[i][2]
                state_t1 = minibatch[i][3]


                # Fill out inputs
                inputs[i:i + 1] = state_t

                # Fill Out Targets
                targets[i] = self.model.predict(state_t)  # Fill out All Q. Sstya,Action values
                Q_sa = self.model.predict(state_t1)

                # Review next state Q Function Update
                if(state_t1 is None):
                    targets[i, action_t] = reward_t
                else:
                    # Prediction Q Value at next States
                    targets[i, action_t] = reward_t + GAMMA * np.max(Q_sa)
            self.model.fit(inputs, targets, batch_size=BATCH_SIZE, epochs=1, verbose=0)
    
    def SaveBestWeights(self, number):
        print("Saving Best Model")
        self.model.save_weights("./ModelWeights/TurretHunterModelWeights" + str(number) +".h5",overwrite=True)
