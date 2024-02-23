import pygame
import levels_menu
import game
import windows
import consts
import starsRecorder
import soundManager
import spriteGroups
from processHelper import load_image, terminate, transition
from itemCreator import Button, Stars
from itemAnimator import AnimatedTypedText


def game_complete():
    soundManager.game_complete_sound(consts.languageNow)

    if consts.languageNow == 'rus':
        img_game_complete = load_image(r"objects\animated\game-complete-rus-obj.png")
        tr_game_complete = pygame.transform.scale(img_game_complete,
                                                (img_game_complete.get_width() * 3, img_game_complete.get_height() * 3))
        game_complete_obj = AnimatedTypedText(tr_game_complete, 16, 1, windows.width // 2 - 4752 * 3 // 16 // 2,
                                              windows.height // 2 - 225)
    else:
        img_game_complete = load_image(r"objects\animated\game-complete-eng-obj.png")
        tr_game_complete = pygame.transform.scale(img_game_complete,
                                                  (img_game_complete.get_width() * 3,
                                                   img_game_complete.get_height() * 3))
        game_complete_obj = AnimatedTypedText(tr_game_complete, 16, 1, windows.width // 2 - 6032 * 3 // 16 // 2,
                                              windows.height // 2 - 225)

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
                spriteGroups.animatedTypedText.empty()
                transition()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                spriteGroups.animatedTypedText.empty()
                transition()
                game.game_def(consts.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, consts.volS)

        consts.game_state_field.draw(windows.screen)

        game_complete_obj.update_game_complete(windows.screen, record, stars, repeat_btn, to_lvlmenu_btn, levelTime,
                                              levelTimeRect,
                                              consts.languageNow)
        spriteGroups.animatedTypedText.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
