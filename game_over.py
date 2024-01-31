import pygame
import sys
import game
import menu
import windows
import consts
from load_image import load_image
from itemCreator import Button, Object
from itemAnimator import AnimatedGameOver
from itemChecker import fullscreenExportChecker, cursorGameChecker, fullscreenWindowsChecker


def game_over(whatFrame=0):
    screen, WIDTH, HEIGHT = fullscreenWindowsChecker(windows.fullscreen)

    pygame.mixer.music.load(r"data\sounds\game-over-sound.mp3")
    pygame.mixer.music.play(1)
    errorSound = pygame.mixer.Sound(r"data\sounds\error-sound.mp3")

    if not windows.fullscreen:
        field = Object(WIDTH - WIDTH, HEIGHT - HEIGHT, 1024, 704, r"objects\without text\windows-field-obj.png")
    else:
        field = Object(windows.otstupx, HEIGHT - HEIGHT, WIDTH - 2 * windows.otstupx, 1080,
                       r"objects\without text\windows-field-obj.png")

    bg_img_game_over = load_image(r"objects\animated\game-over-obj.png")
    bg_tr_game_over = pygame.transform.scale(bg_img_game_over,
                                             (bg_img_game_over.get_width() * 3, bg_img_game_over.get_height() * 3))
    game_over_bg = AnimatedGameOver(bg_tr_game_over, 14, 1, WIDTH // 2 - 3388 * 3 // 14 // 2, HEIGHT // 2 - 180)

    repeat_btn = Button(WIDTH // 2 - 94 // 2 + 120, HEIGHT // 2 - 45, 94, 104, r"buttons\without text\default-repeat-over-btn.png",
                        r"buttons\without text\hover-repeat-over-btn.png",
                        r"buttons\without text\press-repeat-over-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(WIDTH // 2 - 94 // 2 - 120, HEIGHT // 2 - 45, 94, 104,
                            r"buttons\without text\default-tolvlmenu-over-btn.png",
                            r"buttons\without text\hover-tolvlmenu-over-btn.png",
                            r"buttons\without text\press-tolvlmenu-over-btn.png", r"data\sounds\menu-button-sound.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fullscreenExportChecker(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if game_over_bg.cur_frame >= 130:
                    if windows.fullscreen:
                        running = False
                        consts.bg_group_over.empty()
                        windows.fullscreen = 0
                        game_over(1)
                    else:
                        running = False
                        consts.bg_group_over.empty()
                        windows.fullscreen = 1
                        game_over(1)
                else:
                    pygame.mixer.Sound.set_volume(errorSound, menu.volS)
                    errorSound.play()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                consts.bg_group_over.empty()
                menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                consts.bg_group_over.empty()
                game.game_def(menu.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, menu.volS)

        field.draw(screen)

        if whatFrame:
            game_over_bg.cur_frame = 129
            pygame.mixer.music.stop()
        game_over_bg.update(screen, repeat_btn, to_lvlmenu_btn)
        consts.bg_group_over.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        cursorGameChecker(x_c, y_c, consts.cursor, screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
