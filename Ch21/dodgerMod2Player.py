import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000
TEXTCOLOR = (0,0,0)
BACKGROUNDCOLOR = (255,255,255)
FPS = 60
BADDIEMINSIZE = 20
BADDIEMAXSIZE = 70
BADDIEMINSPEED = 2
BADDIEMAXSPEED = 4
ADDNEWBADDIERATE = 35
PLAYERMOVERATE = 5
PLAYERSIZE = 60
INCREASEBADDIERSPEEDEVERYNPOINTS = 1000
INCREASEBADDIESPEEDBY = 1
TITLE = 'The Legend of Zelda: Mountain Chaos'

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            return

def playerHasHitBaddie(playerRect, player2Rect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']) or player2Rect.colliderect(b['rect']):
            return True
    return False

def playersCollided(playerRect, player2Rect):
    if playerRect.colliderect(player2Rect):
        return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)

font = pygame.font.SysFont(None, 48)

gameOverSound = pygame.mixer.Sound('lttp_link_dying.mp3')
playerCollideSound = pygame.mixer.Sound('sword-shine-2.mp3')
pygame.mixer.music.load('death-mountain-2.mid')

playerImage = pygame.image.load('link.png')
playerStretchedImage = pygame.transform.scale(playerImage, (PLAYERSIZE, PLAYERSIZE))
playerRect = playerStretchedImage.get_rect()

player2Image = pygame.image.load('link2.png')
player2StretchedImage = pygame.transform.scale(player2Image, (PLAYERSIZE, PLAYERSIZE))
player2Rect = player2StretchedImage.get_rect()

baddieImage = pygame.image.load('boulder2.png')
bgImage = pygame.image.load("Death-Mountain.png")

windowSurface.fill(BACKGROUNDCOLOR)
drawText(TITLE, font, windowSurface, (WINDOWWIDTH / 6), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

# New game.
topScore = 0
while True:
    baddies = []
    score = 0
    baddieSpeedRate = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 100)
    player2Rect.topleft = (WINDOWWIDTH / 4, WINDOWHEIGHT - 100)
    moveLeft = moveRight = moveUp = moveDown = False
    moveLeft2 = moveRight2 = moveUp2 = moveDown2 = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    # Game loop.
    while True:
        score += 1
        

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True      

                # Player one - arrow keys
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN:
                    moveUp = False
                    moveDown = True

                # Player 2 - WASD
                if event.key == K_a:
                    moveRight2 = False
                    moveLeft2 = True
                if event.key == K_d:
                    moveLeft2 = False
                    moveRight2 = True
                if event.key == K_w:
                    moveDown2 = False
                    moveUp2 = True
                if event.key == K_s:
                    moveUp2 = False
                    moveDown2 = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat =  False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                # Player one -- arrow keys    
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False

                # Player two - WASD
                if event.key == K_a:
                    moveLeft2 = False
                if event.key == K_d:
                    moveRight2 = False
                if event.key == K_w:
                    moveUp2 = False
                if event.key == K_s:
                    moveDown2 = False
                    

##            if event.type == MOUSEMOTION:
##                playerRect.centerx = event.pos[0]
##                playerRect.centery = event.pos[1]
                          
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1

        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize), 
                         'speed': random.randint(BADDIEMINSPEED+baddieSpeedRate, BADDIEMAXSPEED+baddieSpeedRate),
                         'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            if score % INCREASEBADDIERSPEEDEVERYNPOINTS == 0:
                baddieSpeedRate += INCREASEBADDIESPEEDBY
                
            baddies.append(newBaddie)

        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE,0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE,0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)    
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        if moveLeft2 and player2Rect.left > 0:
            player2Rect.move_ip(-1 * PLAYERMOVERATE,0)
        if moveRight2 and player2Rect.right < WINDOWWIDTH:
            player2Rect.move_ip(PLAYERMOVERATE,0)
        if moveUp2 and player2Rect.top > 0:
            player2Rect.move_ip(0, -1 * PLAYERMOVERATE)    
        if moveDown2 and player2Rect.bottom < WINDOWHEIGHT:
            player2Rect.move_ip(0, PLAYERMOVERATE)

        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # windowSurface.fill(BACKGROUNDCOLOR)
        windowSurface.blit(bgImage, (0, 0))
            
            
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        windowSurface.blit(playerStretchedImage, playerRect)
        windowSurface.blit(player2StretchedImage, player2Rect)

        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if playerHasHitBaddie(playerRect, player2Rect, baddies):
            if score > topScore:
                topScore = score
            break

        if playersCollided(playerRect, player2Rect):
            playerCollideSound.play()

        mainClock.tick(FPS)

    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) -80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()



    
                                                        
            
































    













