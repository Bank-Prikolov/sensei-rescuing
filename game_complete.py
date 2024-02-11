import pygame
import levels_menu
import game
import windows
import consts
import starsRecorder
from processHelper import load_image, terminate, transition
from itemCreator import Button, Stars
from itemAnimator import AnimatedGameComplete


def game_complete(whatFrame=0):
    pygame.mixer.music.load(r"data\sounds\game-complete-sound.mp3")
    pygame.mixer.music.play(1)

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
                terminate()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                consts.bg_group_complete.empty()
                transition()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                consts.bg_group_complete.empty()
                transition()
                game.game_def(consts.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, consts.volS)

        consts.game_state_filed.draw(windows.screen)

        if whatFrame:
            game_complete_bg.cur_frame = 149
            pygame.mixer.music.stop()
        game_complete_bg.update(windows.screen, record, stars, repeat_btn, to_lvlmenu_btn, levelTime, levelTimeRect)
        consts.bg_group_complete.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
