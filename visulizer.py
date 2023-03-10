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

    screensize = physics.Vector2(500, 1000)

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

    paddedSpace = screensize*0.8

    offset = paddedSpace/2

    offset.y = paddedSpace.y

    scaleX = paddedSpace.x / difX
    scaleY = paddedSpace.y / difY

    scale = scaleX
    if scaleY < scaleX:
        scale = scaleY

    while True:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if num < len(body_log):

            # Draw the rocket
            display_surface.fill((200, 250, 255))
            pygame.draw.rect(display_surface, (140, 255, 100),
                             (0, offset.y, screensize.x, offset.y))

            # rotating the orignal image
            new_image = pygame.transform.rotate(
                image_orig, -body_log[num].angle)
            rect = new_image.get_rect()
            # set the rotated rectangle to the old center
            rect.center = (-body_log[num].position*scale+offset).tuple()
            # drawing the rotated rectangle to the screen
            display_surface.blit(new_image, rect)

            # Update the display
            pygame.display.update()

            num += 1
            sleep(simStep)
