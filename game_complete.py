import pygame
import levels_menu
import game
import windows
import consts
import starsRecorder
from processHelper import load_image, terminate
from itemCreator import Button, Object, Stars
from itemAnimator import AnimatedGameComplete


def game_complete(whatFrame=0):
    pygame.mixer.music.load(r"data\sounds\game-complete-sound.mp3")
    pygame.mixer.music.play(1)
    errorSound = pygame.mixer.Sound(r"data\sounds\error-sound.mp3")

    # if not windows.fullscreen:
    #     field = Object(WIDTH - WIDTH, HEIGHT - HEIGHT, 1024, 704, r"objects\without text\windows-field-obj.png")
    # else:
    #     field = Object(windows.otstupx, HEIGHT - HEIGHT, WIDTH - 2 * windows.otstupx, 1080,
    #                    r"objects\without text\windows-field-obj.png")

    field = Object(8, 8, 1008, 688, rf"objects\without text\games-window-obj.png")

    bg_img_game_complete = load_image(r"objects\animated\game-complete-obj.png")
    bg_tr = pygame.transform.scale(bg_img_game_complete,
                                   (bg_img_game_complete.get_width() * 3, bg_img_game_complete.get_height() * 3))
    game_complete_bg = AnimatedGameComplete(bg_tr, 16, 1, windows.width // 2 - 4752 * 3 // 16 // 2,
                                            windows.height // 2 - 180 - 15 * 3)

    record = starsRecorder.get_lastRecord(consts.lvlNow)
    zeroStars, oneStar, twoStars, threeStars = (
        r"objects\without text\stars-zero-obj.png", r"objects\without text\stars-one-obj.png",
        r"objects\without text\stars-two-obj.png", r"objects\without text\stars-three-obj.png")
    stars = Stars(windows.width // 2 - 152, windows.height // 2 - 40, 304, 88, zeroStars, oneStar, twoStars, threeStars)

    ButtonsFont = pygame.font.Font(r"data\fonts\PixelNumbers.ttf", 70)
    time = starsRecorder.get_lastSeconds(consts.lvlNow)
    time_sorted = f"{time // 60:02}:{time % 60:02}"
    levelTime = ButtonsFont.render(time_sorted, True, "#ffffff")
    levelTimeRect = levelTime.get_rect(center=(windows.width // 2, windows.height // 2 + 110))

    repeat_btn = Button(windows.width // 2 + 172, windows.height // 2 - 20, 94, 104,
                        r"buttons\without text\default-repeat-comp-btn.png",
                        r"buttons\without text\hover-repeat-comp-btn.png",
                        r"buttons\without text\press-repeat-comp-btn.png", r"data\sounds\menu-button-sound.mp3")
    to_lvlmenu_btn = Button(windows.width // 2 - 266, windows.height // 2 - 20, 94, 104,
                            r"buttons\without text\default-tolvlmenu-comp-btn.png",
                            r"buttons\without text\hover-tolvlmenu-comp-btn.png",
                            r"buttons\without text\press-tolvlmenu-comp-btn.png", r"data\sounds\menu-button-sound.mp3")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(windows.fullscreen)

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
                    pygame.mixer.Sound.set_volume(errorSound, consts.volS)
                    errorSound.play()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                consts.bg_group_complete.empty()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                consts.bg_group_complete.empty()
                game.game_def(consts.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, consts.volS)

        field.draw(windows.screen)

        if whatFrame:
            game_complete_bg.cur_frame = 149
            pygame.mixer.music.stop()
        game_complete_bg.update(windows.screen, record, stars, repeat_btn, to_lvlmenu_btn, levelTime, levelTimeRect)
        consts.bg_group_complete.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
