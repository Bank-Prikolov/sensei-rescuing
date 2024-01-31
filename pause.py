import pygame
import sys
from load_image import load_image
from itemCreator import Button, Object
from itemChecker import fullscreenExportChecker, cursorGameChecker, languageImportChecker
import menu
import game
import windows

clock = pygame.time.Clock()
pygame.display.set_caption('Sensei Rescuing')

cursor = load_image(r'objects\without text\cursor-obj.png')
pygame.mouse.set_visible(False)

languageNow = languageImportChecker()


def game_pause():
    if windows.fullscreen:
        size = WIDTH, HEIGHT = 1920, 1080
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    else:
        size = WIDTH, HEIGHT = 1024, 704
        screen = pygame.display.set_mode(size)

    title = Object(WIDTH // 2 - 150, HEIGHT // 2 - 145, 300, 100, fr"objects\{languageNow}\pause-title-obj.png")

    if not windows.fullscreen:
        field = Object(WIDTH - WIDTH, HEIGHT - HEIGHT, 1024, 704, r"objects\without text\windows-field-obj.png")
    else:
        # 1535
        field = Object(windows.otstupx, HEIGHT - HEIGHT, WIDTH - 2 * windows.otstupx, 1080,
                       r"objects\without text\windows-field-obj.png")

    repeat_btn = Button(WIDTH // 2 - 150 + 102, HEIGHT // 2 - 30, 94, 104,
                        r"buttons\without text\default-repeat-btn.png",
                        r"buttons\without text\hover-repeat-btn.png",
                        r"buttons\without text\press-repeat-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(WIDTH // 2 - 150 + 212, HEIGHT // 2 - 30, 94, 104,
                            r"buttons\without text\default-tolvlmenu-btn.png",
                            r"buttons\without text\hover-tolvlmenu-btn.png",
                            r"buttons\without text\press-tolvlmenu-btn.png", r"data\sounds\menu-button-sound.mp3")
    play_btn = Button(WIDTH // 2 - 150 - 7, HEIGHT // 2 - 30, 94, 104, r"buttons\without text\default-play-btn.png",
                      r"buttons\without text\hover-play-btn.png",
                      r"buttons\without text\press-play-btn.png", r"data\sounds\menu-button-sound.mp3")
    control_btn = Button(WIDTH // 2 - 150, HEIGHT // 2 + 85, 300, 80,
                         fr"buttons\{languageNow}\default-controls-btn.png",
                         fr"buttons\{languageNow}\hover-controls-btn.png")
    control_field = Object(WIDTH // 2 - 250, HEIGHT // 2 - 170, 504, 252, fr"objects\{languageNow}\controls-field-obj.png")
    running = True
    fps = 60
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fullscreenExportChecker(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if windows.fullscreen:
                    running = False
                    windows.fullscreen = 0
                    game_pause()
                else:
                    running = False
                    windows.fullscreen = 1
                    game_pause()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                game.game_def(menu.lvlNow)

            if event.type == pygame.USEREVENT and event.button == play_btn:
                running = False

            for button in [repeat_btn, to_lvlmenu_btn, play_btn]:
                button.handle_event(event, menu.volS)

        for obj in [field, title]:
            obj.draw(screen)

        for button in [repeat_btn, to_lvlmenu_btn, play_btn, control_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(screen)

        if control_btn.rect.collidepoint(pygame.mouse.get_pos()):
            control_field.draw(screen)

        clock.tick(fps)

        x_c, y_c = pygame.mouse.get_pos()
        cursorGameChecker(x_c, y_c, cursor, screen)

        pygame.display.flip()

# game_pause()
