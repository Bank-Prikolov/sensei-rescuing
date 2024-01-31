import pygame
import sys
import menu
import game
import windows
import consts
from load_image import load_image
from itemCreator import Button, Object, Stars
from itemAnimator import AnimatedGameComplete
from itemChecker import fullscreenExportChecker, cursorGameChecker, fullscreenWindowsChecker


def game_complete(whatFrame=0):
    screen, WIDTH, HEIGHT = fullscreenWindowsChecker(windows.fullscreen)

    pygame.mixer.music.load(r"data\sounds\game-complete-sound.mp3")
    pygame.mixer.music.play(1)
    errorSound = pygame.mixer.Sound(r"data\sounds\error-sound.mp3")

    if not windows.fullscreen:
        field = Object(WIDTH - WIDTH, HEIGHT - HEIGHT, 1024, 704, r"objects\without text\windows-field-obj.png")
    else:
        field = Object(windows.otstupx, HEIGHT - HEIGHT, WIDTH - 2 * windows.otstupx, 1080,
                       r"objects\without text\windows-field-obj.png")

    bg_img_game_complete = load_image(r"objects\animated\game-complete-obj.png")
    bg_tr = pygame.transform.scale(bg_img_game_complete,
                                   (bg_img_game_complete.get_width() * 3, bg_img_game_complete.get_height() * 3))
    game_complete_bg = AnimatedGameComplete(bg_tr, 16, 1, WIDTH // 2 - 4752 * 3 // 16 // 2, HEIGHT // 2 - 180 - 15 * 3)

    record = 3
    zeroStars, oneStar, twoStars, threeStars = (
        r"objects\without text\stars-zero-obj.png", r"objects\without text\stars-one-obj.png",
        r"objects\without text\stars-two-obj.png", r"objects\without text\stars-three-obj.png")
    stars = Stars(WIDTH // 2 - 152, HEIGHT // 2 - 40, 304, 88, zeroStars, oneStar, twoStars, threeStars)

    repeat_btn = Button(WIDTH // 2 + 172, HEIGHT // 2 - 45, 94, 104, r"buttons\without text\default-repeat-comp-btn.png",
                        r"buttons\without text\hover-repeat-comp-btn.png",
                        r"buttons\without text\press-repeat-comp-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(WIDTH // 2 - 266, HEIGHT // 2 - 45, 94, 104,
                            r"buttons\without text\default-tolvlmenu-comp-btn.png",
                            r"buttons\without text\hover-tolvlmenu-comp-btn.png",
                            r"buttons\without text\press-tolvlmenu-comp-btn.png", r"data\sounds\menu-button-sound.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fullscreenExportChecker(windows.fullscreen)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if game_complete_bg.cur_frame >= 150:
                    if windows.fullscreen:
                        running = False
                        consts.bg_group_complete.empty()
                        windows.fullscreen = 0
                        game_complete(1)
                    else:
                        running = False
                        consts.bg_group_complete.empty()
                        windows.fullscreen = 1
                        game_complete(1)
                else:
                    pygame.mixer.Sound.set_volume(errorSound, menu.volS)
                    errorSound.play()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                consts.bg_group_complete.empty()
                menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                consts.bg_group_complete.empty()
                game.game_def(menu.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, menu.volS)

        field.draw(screen)

        if whatFrame:
            game_complete_bg.cur_frame = 149
            pygame.mixer.music.stop()
        game_complete_bg.update(screen, record, stars, repeat_btn, to_lvlmenu_btn)
        consts.bg_group_complete.draw(screen)

        x_c, y_c = pygame.mouse.get_pos()
        cursorGameChecker(x_c, y_c, consts.cursor, screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()

# game_complete()
