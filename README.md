[//]: # (Image References)
[image1]: ./image-examples/gameplay_img.png "Gameplay"


# Turret Hunter
A pygame-driven 2D game where a Deep Q Network (DQN) model controls a spaceship in varying environments. The game's purpose is for the spaceship to destroy the turrets. Next it will be the Agent vs. other Agents. The successive step will likely be to vary the walls and NPC movements to see if the Agents react in a semi-optimal manner. Most reinforcement learning models make the markov assumption, are trained on the same game board with many game episodes, and as a result have difficulty on new game situations. A primary objective is to get the degree of novelty where the DQN based models fail. The other objective is to create/research/develop techniques to improve at this task.  

#### The purpose
* To examine a DQN model's reaction to varying degrees of environmental novelty; as in everything here, quantify if possible
* Replicate/examine learners that do not make the Markov assumption, test on this game
* Try to recreate results from one of the recent episodic memory papers
* See if it allows the NPC to adapt to varying game maps better

---

## Dependencies
Update: did a "pip freeze > requirements.txt" on 10/22/18 using the virtualenv used in testing this project which includes many extraneous libraries; the ones below are actually used in the code.
* Ubuntu 16.04
* pygame >= 1.9.3
* Keras == 2.2.0
* Keras-Applications==1.0.2
* Keras-Preprocessing==1.0.1
* numpy==1.14.5
* opencv-python==3.4.1.15
* scikit-image==0.14.1


## Basic Build Instructions
(** TO DO .. need to incorporate command line inputs/training/testing with particular and available models** )
1. Open up a bash terminal
2. python -m venv TurretHunterEnv
3. source ./TurretHunterEnv/bin/activate
4. pip install -r requirements.txt
5. python TurretHunter.py

#### To Do (in no particular order)
- [ ] Train model on current map to see if it converges (somehow make 12 hours of free GPU time)
- [ ] Command line inputs
- [ ] Edit Build Instructions in this README.md
- [x] Make a minimal ML example to see if the game environment/simulator is sufficient
- [x] Put walls in the game for non-player ships to hide
- [ ] Randomize wall creation on successive maps
- [ ] Quantify the degree of difference perhaps percentage pixel similarity on non-player/agent parts of the game screen
- [ ] Come up to date on RL research so we can do the next To Do:
- [ ] Give the ship some sort of Episodic Memory
- [x] Put a setting for autonomous or player controlled (IS_AUTONOMOUS flag)
- [x] Implement a reset mechanism
- [x] Make the ship controllable by arrow keys
- [x] Try the Pong DQN and see if it learns spaceship commands
- [x] Write a README.md


## The Model
* To be completed * (initially this will be related to the popular pong DQN from deepmind)

## What it looks like
![Bonne journée!!][image1]

## How to contribute
Email me! Part of the motivation to do this project was to have a taste of game programming via pygame, and do some reinforcement learning to make the bot beat the game!

Currently, I'm stuck on some equations on a paper. In between working on Udacity's Self Driving Car Engineering Nanodegree, I am perusing Sutton and Bartow's RL book for intuition.
