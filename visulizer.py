import pygame
import sys
import physics
from time import sleep


def run(body_log: list, simStep):
    pygame.init()

    maxX = 0
    minX = 0
    maxY = 0
    minY = 0

    for body in body_log:
        if body.position.x > maxX:
            maxX = body.position.x
        if body.position.y > maxY:
            maxY = body.position.y
        if body.position.x < minX:
            minX = body.position.x
        if body.position.y < minY:
            minY = body.position.y

    difX = abs(maxX)
    if abs(minX) > difX:
        difX = abs(minX)

    difY = abs(maxY)
    if abs(minY) > difY:
        difY = abs(minY)

    screensize = physics.Vector2(400, 800)

    paddedSpace = screensize*0.85

    offset = screensize/2

    offset.y = screensize.y-(screensize.y-paddedSpace.y)/2

    scaleX = (paddedSpace.x/2) / difX
    scaleY = paddedSpace.y / difY

    print(scaleX, scaleY, "   ", difX, difY)

    scale = scaleX
    if scaleY < scaleX:
        scale = scaleY

    display_surface = pygame.display.set_mode(screensize.tuple())

    # define a surface (RECTANGLE)
    image_orig = pygame.Surface(body_log[0].size.tuple())
    # for making transparent background while rotating an image
    image_orig.set_colorkey((255, 255, 255))
    # fill the rectangle / surface with green color
    image_orig.fill((255, 0, 0))
    # creating a copy of orignal image for smooth rotation
    image = image_orig.copy()
    image.set_colorkey((255, 255, 255))
    # define rect for placing the rectangle at the desired position
    rect = image.get_rect()

    num = 0
    isReversed = False
    timeScale = 1
    isPaused = False

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
        display_surface.fill((200, 250, 255))
        pygame.draw.rect(display_surface, (140, 255, 100),
                         (0, offset.y, screensize.x, offset.y))

        # Draw bread crumbs
        for body in body_log[0:num][0::int(1/simStep/4)]:
            pygame.draw.rect(display_surface, (255, 0, 0), (
                             (-body.position*scale+offset).tuple(),
                             physics.Vector2.one().tuple()))

        # Draw the rocket
        new_image = pygame.transform.rotate(
            image_orig, -body_log[num].angle)
        rect = new_image.get_rect()
        # set the rotated rectangle to the old center
        rect.center = (-body_log[num].position*scale+offset).tuple()
        # drawing the rotated rectangle to the screen
        display_surface.blit(new_image, rect)

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
