import pygame
import windows
import consts
import modeSelection
from itemCreator import Object, Button
from processHelper import terminate, transition


def phpStorm_menu():

    running = True
    while running:

        windows.screen.blit(consts.menu_bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    modeSelection.modeSelection()

        consts.clock.tick(consts.fps)
        pygame.display.flip()
