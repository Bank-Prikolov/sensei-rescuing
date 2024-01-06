import pygame, sys, screeninfo
from load_image import *
from buttons import Button
from const import *

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sensei Rescuing')
clock = pygame.time.Clock()


# pygame.mixer.music.load("data\sounds\menu-sound.mp3")
# pygame.mixer.music.play(-1)


def main_menu():
    img = load_image('buttons\pp_menu_bg.png')
    bg = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))

    start_btn = Button(WIDTH - 265, 168, 190, 80, "buttons\start-btn.png", "buttons\hover-start-btn.png",
                       "data\sounds\menu-button-sound.mp3")
    settings_btn = Button(WIDTH - 265, 248, 190, 80, "buttons\settings-btn.png", "buttons\hover-settings-btn.png",
                          "data\sounds\menu-button-sound.mp3")
    info_btn = Button(WIDTH - 265, 328, 190, 80, "buttons\info-btn.png", "buttons\hover-info-btn.png",
                      "data\sounds\menu-button-sound.mp3")
    exit_btn = Button(WIDTH - 265, 408, 190, 80, "buttons\exit-btn.png", "buttons\hover-exit-btn.png",
                      "data\sounds\menu-button-sound.mp3")

    buttons = [start_btn, settings_btn, info_btn, exit_btn]

    running = True
    screen.blit(bg, (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            for button in buttons:
                button.handle_event(event)

        for button in buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        pygame.display.flip()


def settings_menu():
    pass


def about_authors_menu():
    pass


main_menu()
