import pygame, sys, screeninfo
from load_image import *

size = WIDTH, HEIGHT = 800, 400
clock = pygame.time.Clock()
FPS = 50
screen = pygame.display.set_mode(size)

def terminate():
    pygame.quit()
    sys.exit()


def start_menu():
    intro_text = ["SENSEI RESCUING",
                  "СТАРТ",
                  "НАСТРОЙКИ",
                  "ОБ АВТОРАХ"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
