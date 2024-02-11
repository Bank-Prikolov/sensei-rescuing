import pygame
import game
import levels_menu
import windows
import consts
from processHelper import load_image, terminate, transition
from itemCreator import Button
from itemAnimator import AnimatedGameOver
from itemChanger import windowsFullscreenChanger


def game_over(whatFrame=0):
    pygame.mixer.music.load(r"data\sounds\game-over-sound.mp3")
    pygame.mixer.music.play(1)
    errorSound = pygame.mixer.Sound(r"data\sounds\error-sound.mp3")

    bg_img_game_over = load_image(r"objects\animated\game-over-obj.png")
    bg_tr_game_over = pygame.transform.scale(bg_img_game_over,
                                             (bg_img_game_over.get_width() * 3, bg_img_game_over.get_height() * 3))
    game_over_bg = AnimatedGameOver(bg_tr_game_over, 14, 1, windows.width // 2 - 3388 * 3 // 14 // 2,
                                    windows.height // 2 - 180)

    repeat_btn = Button(windows.width // 2 - 94 // 2 + 120, windows.height // 2 - 45, 94, 104,
                        r"buttons\without text\default-repeat-over-btn.png",
                        r"buttons\without text\hover-repeat-over-btn.png",
                        r"buttons\without text\press-repeat-over-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(windows.width // 2 - 94 // 2 - 120, windows.height // 2 - 45, 94, 104,
                            r"buttons\without text\default-tolvlmenu-over-btn.png",
                            r"buttons\without text\hover-tolvlmenu-over-btn.png",
                            r"buttons\without text\press-tolvlmenu-over-btn.png", r"data\sounds\menu-button-sound.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(windows.fullscreen)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                if game_over_bg.cur_frame >= 130:
                    if windows.fullscreen:
                        running = False
                        consts.bg_group_over.empty()
                        windows.fullscreen = 0
                        windowsFullscreenChanger(windows.fullscreen)
                        game_over(1)
                    else:
                        running = False
                        consts.bg_group_over.empty()
                        windows.fullscreen = 1
                        windowsFullscreenChanger(windows.fullscreen)
                        game_over(1)
                else:
                    pygame.mixer.Sound.set_volume(errorSound, consts.volS)
                    errorSound.play()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                consts.bg_group_over.empty()
                transition()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                consts.bg_group_over.empty()
                game.game_def(consts.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, consts.volS)

        consts.game_state_filed.draw(windows.screen)

        if whatFrame:
            game_over_bg.cur_frame = 129
            pygame.mixer.music.stop()
        game_over_bg.update(windows.screen, repeat_btn, to_lvlmenu_btn)
        consts.bg_group_over.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
