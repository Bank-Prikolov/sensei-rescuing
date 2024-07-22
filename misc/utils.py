import pygame
import sys
import os

from config import MenuGameConsts, WindowsSettings
from managing import con


def load_image(name, colorkey=None):
    fullname = os.path.join('../data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def transition():
    transition_level = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        transition_surface = pygame.Surface((WindowsSettings.width, WindowsSettings.height))
        transition_surface.fill((0, 0, 0))
        transition_surface.set_alpha(transition_level)
        WindowsSettings.screen.blit(transition_surface, (0, 0))

        transition_level += 5
        if transition_level >= 105:
            transition_level = 255
            running = False

        MenuGameConsts.clock.tick(70)
        pygame.display.flip()


def terminate():
    con.close()
    pygame.quit()
    sys.exit()
