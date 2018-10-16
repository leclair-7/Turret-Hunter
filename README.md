[//]: # (Image References)
[image1]: ./image-examples/gameplay_img.png "Gameplay"


# Turret Hunter
A pygame-driven 2D game where a DQN model control a spaceship in varying environments. The game's purpose is for the spaceship to destroy the turrets. Next it will be the Agent vs. other Agents. The successive step will likely be to vary the walls and see if the Agents react in a semi-optimal manner.

#### The purpose
* To examine a DQN model's reaction to varying degrees of environmental novelty
* Replicate/examine learners outside of the common Markov assumption on which most RL-based models are made
* More purposes arise as progress is made

---

## Dependencies
* Ubuntu 16.04
* pygame >= 1.9.3

## Basic Build Instructions
1. Open up a bash terminal
2. python turret_hunter.py

#### To Do (in no particular order)
- [ ] Make a minimal ML example to see if the game environment/simulator is sufficient
- [ ] Put walls in the game for non-player ships to hide
- [ ] Randomize wall creation on successive maps
- [ ] Put a setting for autonomous or player controlled
- [x] Make the ship controllable by arrow keys
- [x] Try the Pong DQN and see if it learns spaceship commands
- [x] Write a README.md


## The Model
* To be completed * (initially this will be related to the popular pong DQN)

## What it looks like
![Bonne journée!!][image1]
