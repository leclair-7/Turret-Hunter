# Pygame template - skeleton for a new pygame project
import pygame
import random
import math

from os import path
img_dir = path.join(path.dirname(__file__), 'img')
WIDTH  = 480
HEIGHT = 600
FPS    = 60

# define colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
BROWN  = ( 165,  42,  42)
# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schmup")
clock = pygame.time.Clock()

SPIN_DICT = {pygame.K_LEFT  :  1,
             pygame.K_RIGHT : -1}

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

    def rotate(self, force=False):
        """
        Rotate our ship image and set the new rect's center to the
        old rect's center to ensure our image doesn't shift.
        """
        if self.spin or force:
            self.angle += self.rotate_speed*self.spin
            self.barrel = pygame.transform.rotate(self.original_barrel, self.angle)
            self.rect = self.barrel.get_rect(center=self.rect.center)

    def get_event(self, event):
        """ Our spaceship event handler !! """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shoot()
                #objects.add(Laser(self.rect.center, self.angle))

    def update(self):

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
        #print(keystate )
        if keystate[pygame.K_UP]:
            self.velocity = 2
            self.speedx = round(-1 * self.velocity * math.cos(self.move_angle)  )
            self.speedy = round(     self.velocity * math.sin(self.move_angle)  )
        elif keystate[pygame.K_DOWN]:
            self.velocity = 0
            self.speedx = -1 * self.velocity * math.cos(self.move_angle)
            self.speedy =      self.velocity * math.sin(self.move_angle)        

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < HEIGHT - HEIGHT // 2:
            self.rect.top = HEIGHT - HEIGHT // 2
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
    def draw(self, surface):
        """Draw base and barrel to the target surface."""
        surface.blit(self.barrel, self.rect)
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface( (10, 20) )
        #self.image.fill(YELLOW)
        laser_filename = "laserBlue16.png"
        self.original_laser = pygame.image.load(path.join(img_dir, laser_filename)).convert()
        self.original_laser.set_colorkey(BLACK)

        self.angle = math.radians(angle - 90)
        self.image = pygame.transform.rotate(self.original_laser, angle)
        self.rect = self.image.get_rect(center=(x, y))
        
        self.move = [self.rect.x, self.rect.y]
        self.speed_magnitude = 5
        self.speed = (-1 * self.speed_magnitude*math.cos(self.angle),
                      self.speed_magnitude*math.sin(self.angle))

        #self.rect.bottom = y
        #self.rect.centerx = x

        #self.projectile_velicity = 10
        #self.speedy = -10
        #self.speedx = 0
        #self.angle = angle

    def update(self):
        '''
        Off the screen positions handled in this class definition
        collisions between this and other sprites are handled in main
        '''

        #self.rect.y += self.speedy
        #self.rect.x += self.speedx
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


meteor_filename = "meteorBrown_big2.png"

meteor_img = pygame.image.load(path.join(img_dir, meteor_filename)).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player((WIDTH//2, HEIGHT))
#all_sprites.add(player)

for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

running = True
score = 0
# Game loop
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

            if event.key == pygame.K_ESCAPE:
                    running = False
        if event.type == pygame.QUIT:
            running = False
        player.get_event(event)


    # Update
    all_sprites.update()
    player.update()
    #true true means if a mobs collides, it's killed, it bullet collides it gets killed too
    hits = pygame.sprite.groupcollide(mobs, bullets,True,True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    #see if mob hit a player 
    hit_player = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    
    for ship_impact in hit_player:
        score -= 1
        #running = False

    # Draw / render
    screen.fill(BLACK)
    #screen.blit(background,background_rect)
    all_sprites.draw(screen)
    player.draw(screen)

    font = pygame.font.SysFont("Calibri", 25, True, False)
    if score > 0:
        text = font.render('Score: {}'.format(score), True, GREEN)
    else:
        text = font.render('Score: {}'.format(score), True, RED)
    screen.blit(text, [10, 10] )
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
