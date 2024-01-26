import pygame
import sys
from load_image import load_image
from itemCreator import Button, Object
import menu
import game
import windows

clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

cursor = load_image(r'objects\cursor-obj.png')
pygame.mouse.set_visible(False)


def game_pause():
    if windows.fullscreen:
        size = WIDTH, HEIGHT = 1920, 1080
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        size = WIDTH, HEIGHT = 1024, 704
        screen = pygame.display.set_mode(size)

    title = Object(WIDTH // 2 - 150, HEIGHT // 2 - 145, 300, 100, r"objects\pause-title-obj.png")

    if not windows.fullscreen:
        field = Object(WIDTH - 1016, HEIGHT - 696, 1008, 688, r"objects\windows-field-obj.png")
    else:
        field = Object(WIDTH - 1916, HEIGHT - 1076, 1904, 1064, r"objects\windows-field-obj.png")

    repeat_btn = Button(WIDTH // 2 - 150 + 102, HEIGHT // 2 - 30, 94, 104, r"buttons\default-repeat-btn.png",
                        r"buttons\hover-repeat-btn.png",
                        r"buttons\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(WIDTH // 2 - 150 + 212, HEIGHT // 2 - 30, 94, 104, r"buttons\default-tolvlmenu-btn.png",
                            r"buttons\hover-tolvlmenu-btn.png",
                            r"buttons\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")
    play_btn = Button(WIDTH // 2 - 150 - 7, HEIGHT // 2 - 30, 94, 104, r"buttons\default-play-btn.png",
                      r"buttons\hover-play-btn.png",
                      r"buttons\press-play-btn.png", r"data\sounds\menu-button-sound.mp3")

    running = True
    fps = 60
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                menu.levels_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if windows.fullscreen:
                    windows.fullscreen = 0
                    game_pause()
                else:
                    windows.fullscreen = 1
                    game_pause()

            for button in [repeat_btn, to_lvlmenu_btn, play_btn]:
                button.handle_event(event)
                button.handle_event(event)

        for obj in [field, title]:
            obj.draw(screen)

        for button in [repeat_btn, to_lvlmenu_btn, play_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        clock.tick(fps)

        x_c, y_c = pygame.mouse.get_pos()
        if not windows.fullscreen:
            if 8 <= x_c <= 992 and 7 <= y_c <= 667:
                screen.blit(cursor, (x_c, y_c))
        else:
            if 8 <= x_c <= 1880 and 7 <= y_c <= 1040:
                screen.blit(cursor, (x_c, y_c))

        pygame.display.flip()


# game_pause()
