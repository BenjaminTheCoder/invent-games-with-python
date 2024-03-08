import pygame, sys, random
from pygame.locals import *

pygame.init()
mainClock = pygame.time.Clock()

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Collision Detection')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (60, 30, 0)

foodCounter = 0

SPREAD = 50
MOUSE_FOODS = 60
START_FOODS = 250
NEWFOOD = 1
FOODSIZE = 5
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100
player = pygame.Rect(300, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
foods = []
for i in range(START_FOODS):
    foods.append(pygame.Rect(random.randint(0, WINDOWWIDTH - FOODSIZE), random.randint(0, WINDOWHEIGHT - FOODSIZE), FOODSIZE, FOODSIZE))

moveLeft = False
moveRight = False
moveUp = False
moveDown = False

MOVESPEED = 6

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT or event.key == K_a:
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == K_d:
                moveLeft = False
                moveRight = True
            if event.key == K_UP or event.key == K_w:
                moveDown = False
                moveUp = True
            if event.key == K_DOWN or event.key == K_s:
                moveUp = False
                moveDown = True
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT or event.key == K_a:
                moveLeft = False
            if event.key == K_RIGHT or event.key == K_d:
                moveRight = False
            if event.key == K_UP or event.key == K_w:
                moveUp = False
            if event.key == K_DOWN or event.key == K_s:
                moveDown = False
            if event.key == K_x:
                player.top = random.randint(0, WINDOWHEIGHT - player.height)
                player.left = random.randint(0, WINDOWWIDTH - player.width)

        if event.type == MOUSEBUTTONUP:
            for i in range(MOUSE_FOODS):
                foods.append(pygame.Rect(event.pos[0]+random.randint(-SPREAD, SPREAD),event.pos[1]+random.randint(-SPREAD, SPREAD),FOODSIZE,FOODSIZE))
            
    foodCounter += 1
    if foodCounter >= NEWFOOD:
        foodCounter = 0
        foods.append(pygame.Rect(random.randint(0,WINDOWWIDTH-FOODSIZE),random.randint(0,WINDOWHEIGHT-FOODSIZE),FOODSIZE,FOODSIZE))

    windowSurface.fill(BROWN)

    if moveDown and player.bottom<WINDOWHEIGHT:
        player.top += MOVESPEED
    if moveUp and player.top>0:
        player.top -= MOVESPEED    
    if moveLeft and player.left>0:
        player.left -= MOVESPEED
    if moveRight and player.right<WINDOWWIDTH:
        player.right += MOVESPEED

    pygame.draw.rect(windowSurface, BLACK, player)

    for food in foods[:]:
        if player.colliderect(food):
            foods.remove(food)

    for i in range(len(foods)):
        pygame.draw.rect(windowSurface, GREEN, foods[i])
        
    pygame.display.update()
    mainClock.tick(10000000)
