import screeninfo
import pygame
import fileManager

size = width, height = (1024, 704)
screen = pygame.display.set_mode(size)
fullsize = tuple(map(int, '='.join(
    (str(screeninfo.get_monitors()).lstrip('[Monitor(').rstrip(')]').split(', '))[2: 4]).split('=')[1::2]))
fullsize = (1920, 1080)
# k = fullsize[1] // size[1]
# if k in [1, 2]:
#     lis = max([(int(height * 0.5 * x), 0.5 * x) for x in range(2, 5) if not int(height * 0.5 * x) > fullsize[1]])
#     k = lis[1]
k = 1.5
otstupx = (fullsize[0] - size[0] * k) // 2
otstupy = (fullsize[1] - size[1] * k) * k // 2
fullscreen = fileManager.fullscreenImport()
