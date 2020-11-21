import random
import sys
import pygame
from pygame.locals import *
import time

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
BACKGROUND2 = 'gallery/sprites/background2.png'
BACKGROUND3 = 'gallery/sprites/background3.png'
PIPE = 'gallery/sprites/pipe.png'
PIPE3 = 'gallery/sprites/pipe3.png'

def welcomescreen():

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.0013)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if the user press the cross button close the program
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user press the up key or space bar start the game
            elif event.type == KEYDOWN and (event.type == K_SPACE or event.key == K_KP_ENTER):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    color = (0, 0, 0)
    color_light = (255, 255, 255)
    color_dark = (100, 100, 100)


    smallfont = pygame.font.SysFont('Algerian', 25)
    font = pygame.font.SysFont('Ariel', 32)
    text = smallfont.render('Select the Map --', True, color)
    text1 = font.render('Country Side', True, color)
    text2 = font.render('Jungle', True, color)
    text3 = font.render('Factory', True, color)

    while True:
        # for the jungle
        mouse = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if SCREENWIDTH / 5 <= mouse[0] <= SCREENWIDTH / 5 + 140 and SCREENHEIGHT / 3 <= mouse[1] <= SCREENHEIGHT / 2 + 40:
                    level3()
                    return

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if SCREENWIDTH / 5 <= mouse[0] <= SCREENWIDTH / 5 + 140 and SCREENHEIGHT / 4 <= mouse[1] <= SCREENHEIGHT / 4 + 40:
                    level2()
                    return

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if SCREENWIDTH / 5 <= mouse[0] <= SCREENWIDTH / 5 + 140 and SCREENHEIGHT / 6 <= mouse[1] <= SCREENHEIGHT / 6 + 40:
                    level1()

        # SCREEN.fill((255, 0, 0))
        SCREEN.blit(GAME_SPRITES['backgrounda'], (0, 0))

        if SCREENWIDTH / 5 <= mouse[0] <= SCREENWIDTH / 5 + 140 and SCREENHEIGHT / 4 <= mouse[1] <= SCREENHEIGHT / 4 + 40:
            pygame.draw.rect(SCREEN, color_light, [SCREENWIDTH / 4.5, SCREENHEIGHT / 4.3, 140, 40])

        if SCREENWIDTH / 5 <= mouse[0] <= SCREENWIDTH / 5 + 140 and SCREENHEIGHT / 6 <= mouse[1] <= SCREENHEIGHT / 6 + 40:
            pygame.draw.rect(SCREEN, color_light, [SCREENWIDTH / 4.5, SCREENHEIGHT / 6.4, 140, 40])

        if SCREENWIDTH / 5 <= mouse[0] <= SCREENWIDTH / 5 + 140 and SCREENHEIGHT / 3 <= mouse[1] <= SCREENHEIGHT / 3 + 40:
            pygame.draw.rect(SCREEN, color_light, [SCREENWIDTH / 4.5, SCREENHEIGHT / 3.19, 140, 40])

        SCREEN.blit(text2, (SCREENWIDTH / 8 + 30, SCREENHEIGHT / 4))
        SCREEN.blit(text1, (SCREENWIDTH / 8 + 30, SCREENHEIGHT / 6))
        SCREEN.blit(text, (SCREENWIDTH / 10, SCREENHEIGHT / 25))
        SCREEN.blit(text3, (SCREENWIDTH / 8 + 30, SCREENHEIGHT / 3))
        pygame.display.update()


def level2():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my list of upper pipes

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},

    ]
    # my list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8     #bird speed while flapping
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            time.sleep(1)
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print (f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()

        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Adds a new pipe
        if 0<upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # removes a pipe
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background2'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base2'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def level1():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my list of upper pipes

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},

    ]
    # my list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8     #bird speed while flapping
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            time.sleep(1)
            return


        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print (f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()

        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Adds a new pipe
        if 0<upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # removes a pipe
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def level3():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my list of upper pipes

    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},

    ]
    # my list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8     #bird speed while flapping
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            time.sleep(1)
            return

        # check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe3'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print (f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()

        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Adds a new pipe
        if 0<upperPipes[0]['x']<5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # removes a pipe
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe3'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background3'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe3'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe3'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base3'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes,lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True


    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES ['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 +offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

if __name__ == '__main__':

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird By Abhinav')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        )

    GAME_SPRITES['message'] = (pygame.image.load('gallery/sprites/message.png').convert_alpha())
    GAME_SPRITES['backgrounda'] = (pygame.image.load('gallery/sprites/backgrounda.png').convert_alpha())
    GAME_SPRITES['base'] = (pygame.image.load('gallery/sprites/base.png').convert_alpha())
    GAME_SPRITES['base2'] = (pygame.image.load('gallery/sprites/jungle base.png').convert_alpha())
    GAME_SPRITES['base3'] = (pygame.image.load('gallery/sprites/base3.png').convert_alpha())
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()

    )
    GAME_SPRITES['pipe3'] = (pygame.transform.rotate(pygame.image.load(PIPE3).convert_alpha(), 180),
                            pygame.image.load(PIPE3).convert_alpha()
    )
    # game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['background2'] = pygame.image.load(BACKGROUND2).convert()
    GAME_SPRITES['background3'] = pygame.image.load(BACKGROUND3).convert()

    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:

        welcomescreen()
        mainGame()