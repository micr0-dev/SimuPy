import math
import pygame
from pygame import gfxdraw
import sys
import physics
from time import sleep


def run(body_log: list, simStep):
    pygame.init()

    maxX = 0
    minX = 0
    maxY = 0
    minY = 0

    maxThrust = 0

    for body in body_log:
        if body.position.x > maxX:
            maxX = body.position.x
        if body.position.y > maxY:
            maxY = body.position.y
        if body.position.x < minX:
            minX = body.position.x
        if body.position.y < minY:
            minY = body.position.y
        if body.thrust.y > maxThrust:
            maxThrust = body.thrust.y

    difX = abs(maxX)
    if abs(minX) > difX:
        difX = abs(minX)

    difY = abs(maxY)
    if abs(minY) > difY:
        difY = abs(minY)

    font = pygame.font.Font('freesansbold.ttf', 20)

    screensize = physics.Vector2(500, 1000)

    paddedSpace = screensize*0.85

    offset = screensize/2

    offset.y = screensize.y-(screensize.y-paddedSpace.y)/2

    scaleX = (paddedSpace.x/2) / difX
    scaleY = paddedSpace.y / difY

    scale = scaleX
    if scaleY < scaleX:
        scale = scaleY

    display_surface = pygame.display.set_mode(screensize.tuple())

    pygame.display.set_caption('Rocket Visualizer')

    rocketSize = body_log[0].size*scale

    if (rocketSize.x < 4):
        rocketSize.x = 4
    if (rocketSize.y < 4):
        rocketSize.y = 4

    print(rocketSize)
    # define a surface (RECTANGLE)
    image_orig = pygame.Surface((rocketSize).tuple())
    # for making transparent background while rotating an image
    image_orig.set_colorkey((255, 255, 255))
    # fill the rectangle / surface with green color
    image_orig.fill((255, 0, 0))
    # creating a copy of orignal image for smooth rotation
    image = image_orig.copy()
    image.set_colorkey((255, 255, 255))
    # define rect for placing the rectangle at the desired position
    rect = image.get_rect()

    # Motor Burn image
    burnimg = pygame.image.load("./burn.png")

    num = 0
    isReversed = False
    timeScale = 1
    isPaused = True

    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    timeScale *= 2

                if event.key == pygame.K_LEFT:
                    timeScale /= 2

                if event.key == pygame.K_SPACE:
                    isPaused = not isPaused

                if event.key == pygame.K_r:
                    isReversed = not isReversed

        # Draw the environment
        display_surface.fill((69, 212, 255))
        pygame.draw.rect(display_surface, (140, 255, 100),
                         (0, offset.y, screensize.x, offset.y))

        # Draw bread crumbs
        for body in body_log[0:num][0::int(1/simStep/4)]:
            pygame.draw.rect(display_surface, (255, 0, 0), (
                             (-body.position*scale+offset).tuple(),
                             (physics.Vector2.one()*2).tuple()))

        # Draw Altitude marks

        # list of increments to use
        increments = [1, 5, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000]
        increment = increments[-1]  # default increment

        # Find the largest increment that will result in at least 2 marks on the screen
        for inc in increments[::-1]:
            increment = inc
            num_marks = paddedSpace.y/scale / increment
            if num_marks >= 3:
                break

        for i in range(increment, int(paddedSpace.y)*increment, increment):
            point = -physics.Vector2.up()*i*scale+offset
            pygame.draw.lines(display_surface, (255, 255, 255), False,
                              ((point.x-50, point.y), (point.x+50, point.y)))
            if i < 10000:
                distance = str(i)+"m"
            else:
                distance = str(int(i/1000))+"km"

            text = font.render(distance, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (point.x-50, point.y-10)
            display_surface.blit(text, textRect)

        # Draw the rocket
        new_image = pygame.transform.rotate(
            image_orig, -body_log[num].angle)
        rect = new_image.get_rect()
        # set the rotated rectangle to the old center
        rect.center = (-body_log[num].position*scale+offset).tuple()
        # drawing the rotated rectangle to the screen
        display_surface.blit(new_image, rect)

        # Draw the Motor Fire

        thrust = body_log[num].thrust.y/maxThrust

        burnimgdif = pygame.transform.scale(
            burnimg, (physics.Vector2(9, 16)*rocketSize.x*thrust*0.5).tuple())

        rect = burnimgdif.get_rect()

        rect.center = ((-body_log[num].position*scale +
                       offset) + physics.Vector2((math.sin(math.radians(-body_log[num].angle)))*(rocketSize.y/2), rect.height/2 + rocketSize.y/2)).tuple()

        # burnimgdif = pygame.transform.rotate(
        #     burnimgdif, -body_log[num].angle)

        display_surface.blit(burnimgdif, rect)

        if timeScale != 1:
            text = font.render(str(timeScale)+"x", True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.topleft = (textRect.center[0]/2, textRect.center[1])
            display_surface.blit(text, textRect)

        if isPaused:
            text = font.render("PAUSED", True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (offset.x, textRect.center[1]+20)
            display_surface.blit(text, textRect)
        elif isReversed:
            text = font.render("REWINDING", True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (offset.x, textRect.center[1]+20)
            display_surface.blit(text, textRect)

        # Update the display
        pygame.display.update()

        if not isPaused:
            if isReversed:
                num -= 1
            else:
                num += 1
            sleep(simStep / abs(timeScale))
        if num > len(body_log)-1:
            num = len(body_log)-1
        elif num < 0:
            num = 0
