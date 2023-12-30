import screeninfo
import pygame

pygame.init()
size = width, height = 1024, 704
fullsize = tuple(map(int, '='.join(
    (str(screeninfo.get_monitors()).lstrip('[Monitor(').rstrip(')]').split(', '))[2: 4]).split('=')[1::2]))
k = fullsize[1] // size[1]
otstupx = (fullsize[0] - size[0] * k) // 2
otstupy = (fullsize[1] - size[1] * k) * k
screen = pygame.display.set_mode(size)
