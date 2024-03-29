import pygame, sys, time
from pygame.locals import *

pygame.init()

WINDOWWIDTH = 1500
WINDOWHEIGHT = 999
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

DOWNLEFT = 'downleft'
DOWNRIGHT = 'downright'
UPLEFT = 'upleft'
UPRIGHT = 'upright'

MOVESPEED = 8
SCREENSAVER_MODE = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

b1 = {'rect':pygame.Rect(300,80,50,100),'color':RED, 'dir':UPRIGHT}
b2 = {'rect':pygame.Rect(200,200,20,20),'color':GREEN, 'dir':UPLEFT}
b3 = {'rect':pygame.Rect(100,150,60,60),'color':BLUE, 'dir':DOWNLEFT}
b4 = {'rect':pygame.Rect(290,350,370,390),'color':BLACK, 'dir':DOWNRIGHT}
b5 = {'rect':pygame.Rect(200,200,200,200),'color':RED, 'dir':UPRIGHT}
boxes = [b4, b2, b3, b1, b5]


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not SCREENSAVER_MODE:
        windowSurface.fill(WHITE)

    for b in boxes:
        if b['dir'] == DOWNLEFT:
            b['rect'].left -= MOVESPEED
            b['rect'].top += MOVESPEED
        if b ['dir'] == DOWNRIGHT:
            b['rect'].left += MOVESPEED
            b['rect'].top += MOVESPEED
        if b ['dir'] == UPLEFT:
            b['rect'].left -= MOVESPEED
            b['rect'].top -= MOVESPEED
        if b ['dir'] == UPRIGHT:
            b['rect'].left += MOVESPEED
            b['rect'].top -= MOVESPEED

        if b['rect'].top < 0:
            if b['dir'] == UPLEFT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:  
                b['dir'] = DOWNRIGHT

        if b['rect'].bottom > WINDOWHEIGHT:
            if b['dir'] == DOWNLEFT:
                b['dir'] = UPLEFT
            if b['dir'] == DOWNRIGHT:  
                b['dir'] = UPRIGHT

        if b['rect'].left < 0:
            if b['dir'] == DOWNLEFT:
                b['dir'] = DOWNRIGHT
            if b['dir'] == UPLEFT:  
                b['dir'] = UPRIGHT

        if b['rect'].right > WINDOWWIDTH:
            if b['dir'] == DOWNRIGHT:
                b['dir'] = DOWNLEFT
            if b['dir'] == UPRIGHT:  
                b['dir'] = UPLEFT


        pygame.draw.rect(windowSurface, b['color'], b['rect'])
            
                   
    pygame.display.update()
    time.sleep(0.02)
