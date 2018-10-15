'''
Processing sequence

While not done:

    For each event (keypress, mouse click, etc.):
        Use a chain of if statements to run code to handle each event. 
    Run calculations to determine where objects move, what happens when objects collide, etc.
    Clear the screen
    Draw everything 
'''


import pygame
import random

#made by me, Lucas
from magic_variables import *
# Initialize the game engine
pygame.init()
#pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
#x_dim
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

background_image = pygame.image.load("./images/background_deep_ocean.jpg").convert()
player_image     = pygame.image.load("./images/space_ship.png").convert()

click_sound = pygame.mixer.Sound("./sounds/laser5.ogg")

# When blitting this Surface onto a destination, and pixels that
# have the same color as the colorkey will be transparent.
player_image.set_colorkey(BLACK)

pygame.display.set_caption("Strategizing in 2d Eventually")

done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def draw_tree():
    pygame.draw.rect(screen, BROWN, [60, 400, 30, 45])
    pygame.draw.polygon(screen, GREEN, [[150, 400], [75, 250], [0, 400]])
    pygame.draw.polygon(screen, GREEN, [[140, 350], [75, 230], [10, 350]])

def draw_snowman(screen, x, y):
    pygame.draw.ellipse(screen, WHITE, [35 + x, y, 25,  25])
    pygame.draw.ellipse(screen, WHITE, [23 + x, 20 + y, 50,  50])
    pygame.draw.ellipse(screen, WHITE, [x, 65 + y, 100,100])

def draw_stick_figure(screen, x, y):
    #head
    pygame.draw.ellipse(screen, WHITE, [1 + x, y, 10, 10],0)

    # legs    
    pygame.draw.line(screen, WHITE, [5+x, 17+y], [10+x, 27+y],2)
    pygame.draw.line(screen, WHITE, [5+x, 17+y], [1+x, 27+y],2)

    #body
    pygame.draw.line(screen, RED, [5+x, 17+y], [5+x, 7+y],2)

    # arms
    pygame.draw.line(screen, RED, [5+x, 7+y], [9+x, 17+y],2)
    pygame.draw.line(screen, RED, [5+x, 7+y], [1+x, 17+y],2)


pygame.mouse.set_visible(False)
rect_x, rect_y = 50, 50
change_x, change_y = 5, 5

# Speed in pixels per frame
x_speed = 0
y_speed = 0

# Current position
x_coord = 10
y_coord = 10

snowflake_coords = []
for i in range(50):
	x = random.randrange(0,WIDTH)
	y = random.randrange(0,400)
	snowflake_coords.append([x,y]) 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
        	print("pressed quit, the x button on the ui apparently")
        	done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3
        	
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()
            print("user pressed a mouse button")
    
    x_coord += x_speed
    y_coord += y_speed

    if x_coord < 0:
        x_coord = 0
    if x_coord > WIDTH:
        x_coord = WIDTH
    if y_coord < 0:
        y_coord = 0
    if y_coord > HEIGHT-27:
        y_coord = HEIGHT - 27

    pos = pygame.mouse.get_pos()
    # --- Game logic should go here
 
    # --- Drawing code should go here
 
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    #screen.fill(BLUE)
    screen.blit(background_image,[0,0])
    screen.blit(player_image, [pos[0], pos[1]])
    '''
 	#55 is horiz, 50 is vertical, origin = top left
    pygame.draw.rect(screen, RED, [55, 50, 20, 25])
    pygame.draw.line(screen, GREEN, [100, 100], [200, 200], 15)

    y_offset = 10
    while y_offset < 200:
    	#pygame.draw.line(screen, RED, [0,10+y_offset], [100, 110 + y_offset], 5)
    	pygame.draw.line(screen, RED, [0,100+y_offset], [100, 100 + y_offset], 5)
    	
    	y_offset += 10
	'''
    '''
    pygame.draw.arc(screen, GREEN, [100,100,250,200],  PI/2,     PI, 2)
    pygame.draw.arc(screen, BLACK, [100,100,250,200],     0,   PI/2, 2)
    pygame.draw.arc(screen, RED,   [100,100,250,200],3*PI/2,   2*PI, 2)
    pygame.draw.arc(screen, BLUE,  [100,100,250,200],    PI, 3*PI/2, 2)

    pygame.draw.rect(screen, BLACK, [100,100,250,200],2)
    #pygame.draw.polygon(screen, BLACK, [[100,100], [0,200], [200,200]], 5)
    '''
    font = pygame.font.SysFont("Calibri", 25, True, False)

    #second parameter means anti-aliased
    text = font.render('The multirole-sim {}'.format(PI), True, RED)

    screen.blit(text, [10, 10] )
    
    if rect_y > 450 or rect_y < 0:
    	change_y *= -1
    if rect_x > 650 or rect_x < 0:
    	change_x *= -1



    pygame.draw.rect(screen, WHITE, [rect_x, rect_y, 50, 50])
    pygame.draw.rect(screen, RED,   [rect_x + 10, rect_y + 10 ,30, 30])

    rect_x += change_x
    rect_y += change_y
    
    for i in snowflake_coords:
        pygame.draw.circle(screen, WHITE, i, CIRCLE_RADIUS)
    
    '''
    for i in range(len(snowflake_coords)):
        
        snowflake_coords[i][1] += 1
        if snowflake_coords[i][1] > HEIGHT - CIRCLE_RADIUS:
            snowflake_coords[i][1] = CIRCLE_RADIUS
	'''
    draw_tree() 
    draw_snowman(screen, 110,110)
    draw_stick_figure(screen, x_coord, y_coord)
    
    for i in range(len(snowflake_coords)):
        snowflake_coords[i][1] += 1
        if snowflake_coords[i][1] > HEIGHT - CIRCLE_RADIUS:
            x = random.randrange(  CIRCLE_RADIUS, WIDTH - CIRCLE_RADIUS )
            y = random.randrange(-40, 0)
            snowflake_coords[i] = [x,y]
    

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(FPS)
print('The multirole-sim {PI:.3f}')
pygame.quit()