# Pygame template - skeleton for a new pygame project
import pygame
import random


from os import path
img_dir = path.join(path.dirname(__file__), 'img')
WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schmup")
clock = pygame.time.Clock()



class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (50,40) )
        #self.image.fill(GREEN)
        self.image = pygame.transform.scale(player_img, (50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        
        self.radius = 20
        # circle for collision detect debug line
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        
        self.rect.centerx = WIDTH//2
        self.rect.bottom = HEIGHT - 42

        self.speedx = 0
        self.speedy = 0

    def update(self ):
        self.speedx = 0
        self.speedy = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5
        elif keystate[pygame.K_UP]:
            self.speedy = -5
        elif keystate[pygame.K_DOWN]:
            self.speedy = 5
        
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0


        if self.rect.top < HEIGHT - HEIGHT // 2:
            self.rect.top = HEIGHT - HEIGHT // 2
        elif self.rect.bottom > HEIGHT - self.rect.height:
            self.rect.bottom = HEIGHT - self.rect.height
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface( (10, 20) )
        #self.image.fill(YELLOW)
        self.image = laser_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -20
    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom == 0:
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


ship_filename = "playerShip2_blue.png"
laser_filename = "laserBlue16.png"
meteor_filename = "meteorBrown_big2.png"

player_img = pygame.image.load(path.join(img_dir, ship_filename)).convert()
laser_img = pygame.image.load(path.join(img_dir, laser_filename)).convert()
meteor_img = pygame.image.load(path.join(img_dir, meteor_filename)).convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

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


    # Update
    all_sprites.update()

    
    #true true means if a mobs collides, it's killed, it bullet collides it gets killed too
    hits = pygame.sprite.groupcollide(mobs, bullets,True,True)
    for hit in hits:
        score += 1
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    #see if mob hit a player 
    hit_player = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)

    
    if hit_player:
        pass
        #running = False

    # Draw / render
    screen.fill(BLACK)
    #screen.blit(background,background_rect)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
