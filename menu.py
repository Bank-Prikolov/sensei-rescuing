import pygame
import sys
import webbrowser
from load_image import load_image
from buttons import Button
from objects import Object
from transition import transition
from consts import *

pygame.init()

size = WIDTH, HEIGHT = 1024, 704
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sensei Rescuing')
clock = pygame.time.Clock()

imgSI = load_image(bg1)
bgSI = pygame.transform.scale(imgSI, (imgSI.get_width() * 2, imgSI.get_height() * 2))

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)

img = load_image(r'backgrounds\main-menu-bg.png')
bg = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))


def main_menu():
    # pygame.mixer.music.load("data\sounds\menu-sound.mp3")
    # pygame.mixer.music.play(-1)

    title = Object(WIDTH // 2 - 886 // 2, 49, 886, 80, r"objects\menu-title-obj.png")

    start_btn = Button(WIDTH // 2 - 240 // 2, 186, 240, 100, r"buttons\start-btn.png",
                       r"buttons\hover-start-btn.png", r"data\sounds\menu-button-sound.mp3")
    settings_btn = Button(WIDTH // 2 - 240 // 2, 284, 240, 100, r"buttons\settings-btn.png",
                          r"buttons\hover-settings-btn.png", r"data\sounds\menu-button-sound.mp3")
    info_btn = Button(WIDTH // 2 - 240 // 2, 382, 240, 100, r"buttons\info-btn.png",
                      r"buttons\hover-info-btn.png", r"data\sounds\menu-button-sound.mp3")
    exit_btn = Button(WIDTH // 2 - 240 // 2, 480, 240, 100, r"buttons\exit-btn.png",
                      r"buttons\hover-exit-btn.png", r"data\sounds\menu-button-sound.mp3")

    buttons = [start_btn, settings_btn, info_btn, exit_btn]

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (event.type == pygame.USEREVENT and event.button == exit_btn):
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == start_btn:
                transition()
                levels_menu()

            if event.type == pygame.USEREVENT and event.button == settings_btn:
                transition()
                settings_menu()

            if event.type == pygame.USEREVENT and event.button == info_btn:
                transition()
                info_menu()

            for button in buttons:
                button.handle_event(event)

            title.handle_event(event)

        for button in buttons:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        title.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


def settings_menu():

    title = Object(WIDTH // 2 - 626 // 2 - 50, 85, 626, 82, r"objects\settings-title-obj.png")
    field_audio = Object(WIDTH // 2 - 450, 200, 420, 430, r"objects\audio-field-obj.png")
    field_video = Object(WIDTH // 2 + 30, 200, 420, 430, r"objects\video-field-obj.png")

    cross_btn = Button(WIDTH - 229, 93, 67, 72, r"buttons\cross-btn.png", r"buttons\hover-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    running = False

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                running = False

            title.handle_event(event)
            field_audio.handle_event(event)
            field_video.handle_event(event)

            cross_btn.handle_event(event)

        cross_btn.check_hover(pygame.mouse.get_pos())
        cross_btn.draw(screen)

        title.draw(screen)
        field_audio.draw(screen)
        field_video.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


def levels_menu():
    start_btn = Button(WIDTH // 2 - 240 // 2, 186, 240, 100, r"buttons\start-btn.png",
                       r"buttons\hover-start-btn.png", r"data\sounds\menu-button-sound.mp3")

    cross_btn = Button(WIDTH - 228, 93, 67, 72, r"buttons\cross-btn.png", r"buttons\hover-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    running = False

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                running = False

            if event.type == pygame.USEREVENT and event.button == start_btn:
                transition()
                levels_menu()

            cross_btn.handle_event(event)
            start_btn.handle_event(event)

        start_btn.check_hover(pygame.mouse.get_pos())
        start_btn.draw(screen)
        cross_btn.check_hover(pygame.mouse.get_pos())
        cross_btn.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


def info_menu():
    cross_btn = Button(WIDTH - 218, 93, 67, 72, r"buttons\cross-btn.png", r"buttons\hover-cross-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    github_left_btn = Button(WIDTH // 2 - 345, HEIGHT - 170, 67, 72, r"buttons\github-btn.png", r"buttons\hover-github-btn.png",
                       r"data\sounds\menu-button-sound.mp3")
    github_right_btn = Button(WIDTH // 2 + 100, HEIGHT - 170, 67, 72, r"buttons\github-btn.png", r"buttons\hover-github-btn.png",
                       r"data\sounds\menu-button-sound.mp3")

    title = Object(WIDTH // 2 - 640 // 2 - 46, 85, 640, 82, r"objects\info-title-obj.png")
    field = Object(WIDTH // 2 - 450, 200, 900, 430, r"objects\info-field-obj.png")
    alexandr = Object(WIDTH // 2 - 265, HEIGHT - 157, 269, 46, r"objects\alexandr-obj.png")
    igor = Object(WIDTH // 2 + 180, HEIGHT - 157, 142, 45, r"objects\igor-obj.png")

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    transition()
                    running = False

            if event.type == pygame.USEREVENT and event.button == cross_btn:
                transition()
                running = False

            if event.type == pygame.USEREVENT and event.button == github_left_btn:
                webbrowser.open('https://github.com/mikhalexandr')

            if event.type == pygame.USEREVENT and event.button == github_right_btn:
                webbrowser.open('https://github.com/WaizorSote')

            alexandr.handle_event(event)
            igor.handle_event(event)
            field.handle_event(event)
            title.handle_event(event)
            github_left_btn.handle_event(event)
            github_right_btn.handle_event(event)
            cross_btn.handle_event(event)

        field.draw(screen)
        title.draw(screen)
        alexandr.draw(screen)
        igor.draw(screen)

        github_right_btn.check_hover(pygame.mouse.get_pos())
        github_right_btn.draw(screen)
        github_left_btn.check_hover(pygame.mouse.get_pos())
        github_left_btn.draw(screen)
        cross_btn.check_hover(pygame.mouse.get_pos())
        cross_btn.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        if 1 <= x_c <= 1022 and 1 <= y_c <= 702:
            screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


main_menu()
