import pygame, math
from os import path

img_dir = path.join(path.dirname(__file__), 'img')


WIDTH  = 480
HEIGHT = 600

# define some colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
GREY   = (122, 122, 82)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN  = ( 165,  42,  42)

TURRET_FIRE_DELAY = 800

VELOCITY_SCALER = 6

SPIN_DICT = {pygame.K_LEFT  :  1,
             pygame.K_RIGHT : -1}

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
turret_bullets = pygame.sprite.Group()
turrets = pygame.sprite.Group()
walls = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):

    def __init__(self, location, IS_AUTONOMOUS):
        pygame.sprite.Sprite.__init__(self)

        self.IS_AUTONOMOUS = IS_AUTONOMOUS
        ship_filename = "playerShip2_blue.png"
        self.original_barrel  = pygame.image.load(path.join(img_dir, ship_filename)).convert()
        self.original_barrel = pygame.transform.scale(self.original_barrel, (50,38))
        self.original_barrel.set_colorkey(BLACK)
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

        self.health = 1

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

        if self.IS_AUTONOMOUS:

            #assert action in [i for i in range(5)]

            self.speedx = 0
            self.speedy = 0

            self.velocity = 0
            self.move_angle = math.radians(self.angle - 90)
            
            if   action == 0:
                #up
                self.velocity = VELOCITY_SCALER
                self.speedx = round(-1 * self.velocity * math.cos(self.move_angle)  )
                self.speedy = round(     self.velocity * math.sin(self.move_angle)  )
            elif action == 1:
                #down
                self.velocity = VELOCITY_SCALER
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

        if not self.IS_AUTONOMOUS:
            
            keystate = pygame.key.get_pressed()
            self.spin = 0
            for key in SPIN_DICT:
                if keystate[key]:
                    self.spin += SPIN_DICT[key]
            #print("angle:", self.angle, "self.spin", self.spin)
            self.rotate()

            self.speedx = 0
            self.speedy = 0

            self.velocity = 0
            self.move_angle = math.radians(self.angle - 90)
            
            if keystate[pygame.K_UP]:
                self.velocity = VELOCITY_SCALER
                self.speedx = round(-1 * self.velocity * math.cos(self.move_angle)  )
                self.speedy = round(     self.velocity * math.sin(self.move_angle)  )
            elif keystate[pygame.K_DOWN]:
                self.velocity = VELOCITY_SCALER
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

    def __init__(self, x, y, angle, speedx=0, speedy=0):
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
        self.next_fire = pygame.time.get_ticks() + TURRET_FIRE_DELAY

        self.speedx = speedx
        self.speedy = speedy
        
    def shoot(self):

        if pygame.time.get_ticks() > self.next_fire:
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle, "turret")
            all_sprites.add(bullet)
            turret_bullets.add(bullet)

            self.next_fire = pygame.time.get_ticks() + TURRET_FIRE_DELAY  
        
    def draw(self, surface):
        surface.blit(self.rect)
    
    def update(self):
        self.shoot()

        if self.speedx != 0 or self.speedy != 0:
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            #print(self.rect.top)
            #Want the fun turret to go up/down
            if self.rect.top > 495:
                self.speedy = -1 * self.speedy
                self.rect.y += self.speedy
            
            if self.rect.top < 0:
                self.speedy *= -1
                self.rect.y += self.speedy
            '''
            #Code to see if it hit a screen boundary
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            elif self.rect.left < 0:
                self.rect.left = 0

            if self.rect.top < HEIGHT - HEIGHT:
                self.rect.top = HEIGHT - HEIGHT
            elif self.rect.bottom > HEIGHT:
                self.rect.bottom = height
            '''

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface( (250,30) )
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.radius = int(self.rect.width )
        # circle for collision detect debug line
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        
        self.speedx = 0
        self.speedy = 2

    def draw(self, surface):
        surface.blit(self.rect)
    
    def update(self):
        pass
        
    

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
