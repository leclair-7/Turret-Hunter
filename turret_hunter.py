# Pygame template - skeleton for a new pygame project
import pygame
import random
import math
import time
from collections import deque

import cv2
from os import path

from keras.models import Sequential
from keras.layers import *
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import *


img_dir = path.join(path.dirname(__file__), 'img')

'''
Action set:
0-up
1-down
2-left
3-right
4-fire
'''

NUM_ACTIONS = 5

#Resizing for model training
IMGHEIGHT = 50
IMGWIDTH = 50
IMGHISTORY = 4

WIDTH  = 480
HEIGHT = 600
FPS    = 60

WITH_ASTEROIDS = False
IS_AUTONOMOUS = True

# define colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREY   = (122, 122, 82)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN  = ( 165,  42,  42)
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Turret Hunter")
clock = pygame.time.Clock()

SPIN_DICT = {pygame.K_LEFT  :  1,
             pygame.K_RIGHT : -1}

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
turret_bullets = pygame.sprite.Group()
turrets = pygame.sprite.Group()      


class Player(pygame.sprite.Sprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        ship_filename = "playerShip2_blue.png"
        self.original_barrel  = pygame.image.load(path.join(img_dir, ship_filename)).convert()
        self.original_barrel = pygame.transform.scale(self.original_barrel, (50,38))
        self.original_barrel.set_colorkey(BLACK)
        #= pygame.Surface( (50,40) )
        self.barrel = self.original_barrel.copy()

        self.rect = self.barrel.get_rect(center=location)
        #self.image.fill(GREEN)
        
        self.radius = 20
        # circle for collision detect debug line
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT - 42

        self.speedx = 0
        self.speedy = 0
        
        self.angle = 0
        self.spin = 0
        self.rotate_speed = 3
        self.rotate(True)

        self.shield = 50

    def rotate(self, force=False):
        """
        Rotate our ship image and set the new rect's center to the
        old rect's center to ensure our image doesn't shift.
        """
        if self.spin or force:
            self.angle += self.rotate_speed*self.spin
            self.barrel = pygame.transform.rotate(self.original_barrel, self.angle)
            self.rect = self.barrel.get_rect(center=self.rect.center)

    def get_event(self, event, action):
        """ Our spaceship event handler !! """

        if IS_AUTONOMOUS:
            
            self.speedx = 0
            self.speedy = 0

            self.velocity = 0
            self.move_angle = math.radians(self.angle - 90)
            
            if   action == 0:
                #up
                self.velocity = 4
                self.speedx = round(-1 * self.velocity * math.cos(self.move_angle)  )
                self.speedy = round(     self.velocity * math.sin(self.move_angle)  )
            elif action == 1:
                #down
                self.velocity = 4
                self.speedx = -1 * round(-1 * self.velocity * math.cos(self.move_angle)  )
                self.speedy = -1 * round(     self.velocity * math.sin(self.move_angle)  )       
            elif action == 2 or action == 3:
                #left or right rotation
                self.spin = 0
                if action == 2:
                    self.spin += 1
                elif action == 3:
                    self.spin -= 1
                self.rotate()
            elif action == 4:
                #fire
                self.shoot()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot()
                    #objects.add(Laser(self.rect.center, self.angle))

    def update(self):

        if not IS_AUTONOMOUS:
            
            keystate = pygame.key.get_pressed()
            self.spin = 0
            for key in SPIN_DICT:
                if keystate[key]:
                    self.spin += SPIN_DICT[key]
            self.rotate()

            self.speedx = 0
            self.speedy = 0

            self.velocity = 0
            self.move_angle = math.radians(self.angle - 90)
            
            if keystate[pygame.K_UP]:
                self.velocity = 4
                self.speedx = round(-1 * self.velocity * math.cos(self.move_angle)  )
                self.speedy = round(     self.velocity * math.sin(self.move_angle)  )
            elif keystate[pygame.K_DOWN]:
                self.velocity = 4
                self.speedx = -1 * round(-1 * self.velocity * math.cos(self.move_angle)  )
                self.speedy = -1 * round(     self.velocity * math.sin(self.move_angle)  )       

            self.rect.x += self.speedx
            self.rect.y += self.speedy

            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            elif self.rect.left < 0:
                self.rect.left = 0

            if self.rect.top < HEIGHT - HEIGHT:
                self.rect.top = HEIGHT - HEIGHT
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
        else:
            pass

    def draw(self, surface):
        """Draw base and barrel to the target surface."""
        surface.blit(self.barrel, self.rect)
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, "player")
        all_sprites.add(bullet)
        player_bullets.add(bullet)

class Turret(pygame.sprite.Sprite):

    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface( (50,50) )
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.radius = int(self.rect.width )
        # circle for collision detect debug line
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.health = 5
        self.angle = angle
        self.next_fire = pygame.time.get_ticks() + 400
        
    def shoot(self):

        if pygame.time.get_ticks() > self.next_fire:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, "turret")
            all_sprites.add(bullet)
            turret_bullets.add(bullet)

            self.next_fire = pygame.time.get_ticks() + 400  
        
    def draw(self, surface):
        surface.blit(self.rect)
    
    def update(self):
        self.shoot()

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, angle, shooter_type):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface( (10, 20) )
        #self.image.fill(YELLOW)
        if shooter_type == "player":
            laser_filename = "laserBlue16.png"
        elif shooter_type == "turret":
            laser_filename = "laserRed16.png"
        else:
            laser_filename = "laserGreen10.png"
        self.original_laser = pygame.image.load(path.join(img_dir, laser_filename)).convert()
        self.original_laser.set_colorkey(BLACK)

        self.angle = math.radians(angle - 90)
        self.image = pygame.transform.rotate(self.original_laser, angle)
        self.rect = self.image.get_rect(center=(x, y))
        
        self.move = [self.rect.x, self.rect.y]
        self.speed_magnitude = 5
        self.speed = (-1 * self.speed_magnitude*math.cos(self.angle),
                      self.speed_magnitude*math.sin(self.angle))

    def update(self):
        '''
        Off the screen positions handled in this class definition
        collisions between this and other sprites are handled in main
        '''

        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move

        if self.rect.bottom == 0 or self.rect.left == 0 or self.rect.right == WIDTH:
            self.kill()

class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        #self.image.fill(RED)
        self.image = pygame.transform.scale(meteor_img, ( 50,40 ) )
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * .80 / 2 )
        # circle for collision detect debug line
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

        self.rect.x = random.randrange(0, WIDTH - self.rect.width )
        self.rect.y = random.randrange(0, WIDTH - self.rect.height )

        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3, 3)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > HEIGHT + 10 or self.rect.x < 0 or self.rect.x > WIDTH + 20:
            # if we go through bottom of the screen, respawn
            self.rect.x = random.randrange(0, WIDTH - self.rect.width )
            self.rect.y = random.randrange(0, WIDTH - self.rect.height )
            self.speedy = random.randrange(1,8)

class TurretHunterGame:
    
    def __init__(self):
        '''
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        turret_bullets = pygame.sprite.Group()
        turrets = pygame.sprite.Group()      
        '''
        self.score = 0
        self.meteor_filename = "meteorBrown_big2.png"
        self.meteor_img = pygame.image.load(path.join(img_dir, self.meteor_filename)).convert()

        self.player = Player((WIDTH//2, HEIGHT))

        self.turret_list = [ (20, 60 ,180),
                        (420, 20,145),
                        (240,100,135),                
                       ]
        self.num_turrets = len(self.turret_list)

        for t in self.turret_list:
            new_turret = Turret(t[0], t[1], t[2])
            all_sprites.add( new_turret )
            turrets.add(new_turret)
        
        if WITH_ASTEROIDS:
            for i in range(8):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)

        self.running = True

    def playGame(self):
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
            frameno += 1
            # keep loop running at the right speed
            clock.tick(FPS)
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
                        return [self.score, (now - start) ]
            # Update
            all_sprites.update()
            self.player.update()
            # True true means if a mobs collides, it's killed, it bullet collides it gets killed too
            
            hits = pygame.sprite.groupcollide(mobs, player_bullets, True, True)
            for hit in hits:
                self.score += 1
                m = Mob()
                all_sprites.add(m)
                mobs.add(m)
            
            # Player bullets cancel out turret bullets 
            pygame.sprite.groupcollide(player_bullets, turret_bullets, True, True)

            # See if turret bullets hit a player 
            hit_player = pygame.sprite.spritecollide(self.player, turret_bullets, True, pygame.sprite.collide_circle)
            for ship_impact in hit_player:
                self.player.shield -= 1
                self.score -= 1
            
            #see if mobs(asteroids) hit a player 
            hit_player = pygame.sprite.spritecollide(self.player, mobs, True, pygame.sprite.collide_circle)
            for ship_impact in hit_player:
                self.player.shield -= 1
                self.score -= 1
            
            #see if turret bullets hit a player 
            hits = pygame.sprite.groupcollide(player_bullets, turrets,True,True)
            for ship_impact in hits:
                self.score += 1
                self.num_turrets -= 1

            # Draw / render
            screen.fill(BLACK)
            #screen.blit(background,background_rect)
            all_sprites.draw(screen)
            self.player.draw(screen)

            if not IS_AUTONOMOUS:
                font = pygame.font.SysFont("Calibri", 25, True, False)
                
                if self.score > 0:
                    text = font.render('Score: {}'.format(self.score), True, GREEN)
                else:
                    text = font.render('Score: {}'.format(self.score), True, RED)
                
                text_player_shield = font.render('Shield: {}'.format(self.player.shield), True, GREEN)
                TurretsLeft = font.render('Turrets left: {}'.format(self.num_turrets), True, GREEN)
                
                screen.blit(text, [10, 10] )
                screen.blit(text_player_shield, [10, 38] )
                screen.blit(TurretsLeft, [10, 66] )
            # *after* drawing everything, flip the display

            pygame.display.flip()            
            pygame.event.pump()

            if not IS_AUTONOMOUS and self.num_turrets == 0:
                self.running = False
            elif IS_AUTONOMOUS and self.num_turrets == 0:
                now = time.time() 
                
                return [ self.score, round((now - start),4) ]
        now = time.time()
                        
        return [ self.score, (now - start) ]
        #pygame.quit()
class Agent:
    def __init__(self):

        self.domination = True
        self.model = self.createModel()

    def createModel(self):
        print("Creating Convolutional Keras Model")
        
        model = Sequential()
        model.add(Conv2D(16, kernel_size=8, strides=(4, 4), input_shape=(IMGHEIGHT, IMGWIDTH, IMGHISTORY), padding='same'))
        model.add(Activation('relu'))
        model.add(Conv2D(32, kernel_size=4, strides=(2, 2), padding='same'))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(256))
        model.add(Activation('relu'))
        model.add(Dense(units=NUM_ACTIONS, activation='linear'))
        model.compile(loss='mse', optimizer='rmsprop')
        print("Done Creating Model")
        return model

    def getActuationCommand(observation):
        q_value = self.model.predict(observation)
        return np.argmax(q_value)

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
turret_bullets = pygame.sprite.Group()
turrets = pygame.sprite.Group()
#if __name__=='__main__':
th = TurretHunterGame()

def getTest():          
    th.__init__()
    score_and_time = th.playGame() 

    all_sprites.empty()
    mobs.empty()
    player_bullets.empty()
    turret_bullets.empty()
    turrets.empty()

    return score_and_time

print("we'll play the game once")
asdf = getTest()
print(  "asdf", asdf )
print("we'll play the game Again")
print( getTest() )
#print("And again")
#getTest()

times_game = []
for i in range(15):
    game_results = getTest()
    times_game.append(game_results[1])
print(times_game)
