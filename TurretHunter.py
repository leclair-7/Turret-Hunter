# Pygame template - skeleton for a new pygame project
import pygame
import random
import math
import time
from collections import deque, namedtuple

import cv2
import skimage
from skimage import color

from os import path

from Agent import Agent
from GameCharacters import *

WITH_ASTEROIDS = False
IS_AUTONOMOUS = True

FPS    = 60

'''
Action set:
0-up
1-down
2-left
3-right
4-fire
'''

# initialize pygame and create window

Experience = namedtuple('Experience', field_names=['state', 'action', 'reward', 'done', 'new_state'])


class TurretHunterGame:
    
    def __init__(self):
        
        pygame.init()
        #pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Turret Hunter")
        self.clock = pygame.time.Clock()

        #self.agent = Agent()

        self.score = 0
        self.meteor_filename = "meteorBrown_big2.png"
        self.meteor_img = pygame.image.load(path.join(img_dir, self.meteor_filename)).convert()

        self.player = Player((WIDTH//2, HEIGHT), IS_AUTONOMOUS)

        self.turret_list = [ (20, 60 ,180), # shoots down right
                             (240,100,225) # shoots down                
                             
                           ]
        wall = Wall(90,300,225)

        walls.add(wall)
        all_sprites.add(wall)

        self.num_turrets = len(self.turret_list)

        for t in self.turret_list:
            new_turret = Turret(t[0], t[1], t[2])
            all_sprites.add( new_turret )
            turrets.add(new_turret)

        self.funTurret = Turret(420, 20, 145, 0, 2) # shoots down left
        all_sprites.add(self.funTurret)
        turrets.add(self.funTurret)

        if WITH_ASTEROIDS:
            for i in range(8):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)

        self.running = True
        self.numGamesPlayed = 0
        
    def CollisionDetectionCalculations(self):

        hits = pygame.sprite.groupcollide(mobs, player_bullets, True, True)

        for hit in hits:
            self.score += 1
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        
        # Player bullets cancel out turret bullets 
        #pygame.sprite.groupcollide(player_bullets, turret_bullets, True, True)

        # See if turret bullets hit a player 
        hit_player = pygame.sprite.spritecollide(self.player, turret_bullets, True, pygame.sprite.collide_circle)
        for ship_impact in hit_player:
            self.score -= 1
            #print("Got hit by a turret", self.score)
            #self.player.shield -= 1
            #self.player.health -= 1
        
        #see if mobs(asteroids) hit a player 
        hit_player = pygame.sprite.spritecollide(self.player, mobs, True, pygame.sprite.collide_circle)
        for ship_impact in hit_player:
            self.player.shield -= 1
            self.score -= 1    

        #see if turret bullets hit a player 
        hits = pygame.sprite.groupcollide(player_bullets, turrets,True,True)
        for ship_impact in hits:
            #print("hit a turret", self.num_turrets -1)
            self.score += 1
            self.num_turrets -= 1
        
        pygame.sprite.groupcollide(player_bullets, walls, True, False)
        pygame.sprite.groupcollide(turret_bullets, walls, True, False)        

    def InitialDisplay(self):
        #for each frame, calls the event queue, like if the main window needs to be repainted
        pygame.event.pump()
        #make the background black
        self.screen.fill(BLACK)

        all_sprites.draw(self.screen)
        self.player.draw(self.screen)

        pygame.display.flip()

    def EmptySpriteGroups(self):
        all_sprites.empty()
        mobs.empty()
        player_bullets.empty()
        turret_bullets.empty()
        turrets.empty()
        walls.empty()

    #  Game Update Inlcuding Display
    def PlayNextMove(self, action):
        # Calculate DeltaFrameTime
        DeltaFrameTime = self.clock.tick(FPS)

        self.screen.fill(BLACK)

        #action is in range(5)
        self.player.get_event(None, action)

        # Update Sprites
        all_sprites.update()
        self.player.update()

        #all_sprites.draw(self.screen)
        #self.player.draw(self.screen)

        self.CollisionDetectionCalculations()

        if self.num_turrets == 0 or self.score < -25:
            self.EmptySpriteGroups()
            self.__init__()
            self.numGamesPlayed += 1
        #print("self.score:", self.score )
        ScreenImage = pygame.surfarray.array3d(pygame.display.get_surface())
        #pygame.display.flip()
        return [self.score, ScreenImage]
    def PlayNextMoveTest(self, action):
        # Calculate DeltaFrameTime
        DeltaFrameTime = self.clock.tick(FPS)

        self.screen.fill(BLACK)

        #action is in range(5)
        self.player.get_event(None, action)

        self.CollisionDetectionCalculations()
        
        # Update Sprites
        all_sprites.update()
        self.player.update()

        all_sprites.draw(self.screen)
        self.player.draw(self.screen)

        print("In PlayNextMoveTest score:", self.score)
        if self.num_turrets == 0 or self.score < -25:
            self.EmptySpriteGroups()
            self.__init__()
            self.numGamesPlayed += 1
        #print("self.score:", self.score )
        ScreenImage = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.flip()
        return [self.score, ScreenImage]
    def PlayGame(self):
        start = time.time()
        # Game loop        
        action = None

        autonomous_commands = [4 for i in range(25)]
        for i in range(8):
            autonomous_commands.append(3)
        for i in range(45):
            autonomous_commands.append(4)
        for i in range(16):
            autonomous_commands.append(2)
        for i in range(45):
            autonomous_commands.append(4)
        
        frameno = 0
        post_command_set_count = 0
        while self.running:
            pygame.event.pump()
            frameno += 1
            # keep loop running at the right speed
            self.clock.tick(FPS)
            # Process input (events)- Shooting and closing the game handled here
            event = None
            #print(self.score)
            now = time.time()
            if not IS_AUTONOMOUS:
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.shoot()
                        if event.key == pygame.K_ESCAPE:
                                self.running = False
                    if event.type == pygame.QUIT:
                        self.running = False
                    self.player.get_event(event, action)
            else:
                if frameno < len(autonomous_commands):
                    self.player.get_event(event, autonomous_commands[frameno])
                else:
                    post_command_set_count += 1
                    if post_command_set_count == 200:

                        return [self.score, (now - start), frameno ]
            # Update
            all_sprites.update()
            self.player.update()
            # True true means if a mobs collides, it's killed, it bullet collides it gets killed too
            
            self.CollisionDetectionCalculations()

            if self.player.health <1:
                return [ self.score, "Game time:", round((now - start),4), "Frame number: ",frameno ]

            # Draw / render
            self.screen.fill(BLACK)
            #screen.blit(background,background_rect)
            all_sprites.draw(self.screen)
            self.player.draw(self.screen)

            if not IS_AUTONOMOUS:
                font = pygame.font.SysFont("Calibri", 25, True, False)
                
                if self.score > 0:
                    text = font.render('Score: {}'.format(self.score), True, GREEN)
                else:
                    text = font.render('Score: {}'.format(self.score), True, RED)
                
                text_player_shield = font.render('Shield: {}'.format(self.player.shield), True, GREEN)
                TurretsLeft = font.render('Turrets left: {}'.format(self.num_turrets), True, GREEN)
                
                self.screen.blit(text, [10, 10] )
                self.screen.blit(text_player_shield, [10, 38] )
                self.screen.blit(TurretsLeft, [10, 66] )
            # *after* drawing everything, flip the display
            pygame.display.flip()            
            
            if not IS_AUTONOMOUS and self.num_turrets == 0:
                self.running = False
            elif IS_AUTONOMOUS and self.num_turrets == 0:
                now = time.time() 
                '''
                print("this one")
                observ = pygame.surfarray.array3d(pygame.display.get_surface())
                print("game board before image transform", observ.shape)
                observ2 = self.agent.ProcessGameImage(observ)
                print("game board after  image transform", observ2.shape)
                
                timelist = []
                for i in range(1000):
                    start_time = time.time()
                    prediction_1 = self.agent.getActuationCommand(observ2)
                    finish_time = time.time()
                    timelist.append( (finish_time - start_time) )
                print("This is the NN prediction time:", timelist)
                print("Average inference time", sum(timelist) / len(timelist))
                print("Number of parameters",self.agent.model.count_params())
                '''
                return [ self.score, "Game time:", round((now - start),4), "Frame number: ",frameno ]
        now = time.time()
                        
        return [ self.score, (now - start) ]

if __name__=='__main__':

    th = TurretHunterGame()
    th.PlayGame()

    pygame.quit()
    '''
    th.InitialDisplay()

    autonomous_commands = [4 for i in range(25)]
    for i in range(8):
        autonomous_commands.append(3)
    for i in range(45):
        autonomous_commands.append(4)
    for i in range(16):
        autonomous_commands.append(2)
    for i in range(45):
        autonomous_commands.append(4)

    for i in autonomous_commands:
        #action = int(input())
        th.PlayNextMove(i)
    for i in range(50):
        #action = int(input())
        th.PlayNextMove(2)

    a = int(input())
    print("finished the game")
    '''

    '''



    #A testing line
    num_play_games = 1
    for i in range(num_play_games):
        print("Playing the game for the", i, "th time.")
        asdf = getTest()
        print(asdf)

    '''