import pygame, sys, screeninfo
from load_image import *
from buttons import Button

pygame.init()


def terminate():
    pygame.quit()
    sys.exit()


def start_menu():
    size = WIDTH, HEIGHT = 800, 400
    clock = pygame.time.Clock()
    FPS = 60
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Menu')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
                sys.exit()
        pygame.display.flip()
        clock.tick(FPS)

    running = True
    fps = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


start_menu()

