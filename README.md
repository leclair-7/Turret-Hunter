[//]: # (Image References)
[image1]: ./image-examples/gameplay_img.png "Gameplay"


# Turret Hunter
A pygame-driven 2D game where a Deep Q Network (DQN) model controls a spaceship in varying environments. The game's purpose is for the spaceship to destroy the turrets. Next it will be the Agent vs. other Agents. The successive step will likely be to vary the walls and NPC movements to see if the Agents react in a semi-optimal manner. Most reinforcement learning models make the markov assumption, are trained on the same game board with many game episodes, and as a result have difficulty on new game situations. A primary objective is to get the degree of novelty where the DQN based models fail. The other objective is to create/research/develop techniques to improve at this task.  

#### The purpose
* To examine a DQN model's reaction to varying degrees of environmental novelty
* Replicate/examine learners that do not make the Markov assumption
* More purposes arise as progress is made

---

## Dependencies
Update: did a "pip freeze > requirements.txt" on 10/22/18 using the virtualenv used in testing this project.
* Ubuntu 16.04
* pygame >= 1.9.3
* Keras == 2.2.0
* Keras-Applications==1.0.2
* Keras-Preprocessing==1.0.1
* numpy==1.14.5
* opencv-python==3.4.1.15
* scikit-image==0.14.1


## Basic Build Instructions
(** TO DO ** )
1. Open up a bash terminal
2. python -m venv TurretHunterEnv
3. pip install -r requirements.txt
4. source ./TurretHunterEnv/bin/activate
5. python TurretHunter.py

#### To Do (in no particular order)
- [ ] Edit Build Instructions in this README.md
- [ ] Make a minimal ML example to see if the game environment/simulator is sufficient
- [ ] Put walls in the game for non-player ships to hide
- [ ] Randomize wall creation on successive maps
- [ ] Quantify the degree of difference perhaps percentage pixel similarity
- [ ] Give the ship some sort of Episodic Memory
- [x] Put a setting for autonomous or player controlled (IS_AUTONOMOUS flag)
- [x] Implement a reset mechanism
- [x] Make the ship controllable by arrow keys
- [x] Try the Pong DQN and see if it learns spaceship commands
- [x] Write a README.md


## The Model
* To be completed * (initially this will be related to the popular pong DQN)

## What it looks like
![Bonne journée!!][image1]
