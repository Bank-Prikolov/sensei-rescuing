import pygame, sys, screeninfo
from load_image import *
from buttons import Button
from const import *
pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

pygame.mixer.music.load("data\sounds\menu-sound.mp3")
pygame.mixer.music.play(-1)

start_btn = Button(WIDTH - 312, 100, 260, 100, "buttons\start-btn.png", "buttons\hover-start-btn.png",
                   "data\sounds\menu-button-sound.mp3")

tmp = load_image('buttons\pp_menu_bg.png')
tmp1 = pygame.transform.scale(tmp, (tmp.get_width() * 2, tmp.get_height() * 2))


def start_menu():
    running = True
    fps = 60
    screen.blit(tmp1, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            start_btn.handle_event(event)

        clock.tick(fps)

        start_btn.check_hover(pygame.mouse.get_pos())
        start_btn.draw(screen)
        pygame.display.flip()


start_menu()

