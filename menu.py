import pygame, sys, screeninfo
from load_image import *
from buttons import Button
from const import *
pygame.init()

size = WIDTH, HEIGHT = 600, 550
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Menu')

start_btn = Button(WIDTH / 2 - (252 / 2), 100, 252, 74, "", "start-btn.png", "hover-start-btn.png")


def start_menu():
    running = True
    fps = 60
    screen.blit(load_image('background1.png'), (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(fps)

        start_btn.check_hover(pygame.mouse.get_pos())
        start_btn.draw(screen)
        pygame.display.flip()


start_menu()

