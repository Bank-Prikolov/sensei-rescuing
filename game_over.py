import pygame
import game
import levels_menu
import windows
import consts
import soundManager
import spriteGroups
from processHelper import load_image, terminate, transition
from itemCreator import Button
from itemAnimator import AnimatedObject


def game_over():
    soundManager.game_over_sound(consts.languageNow)

    if consts.languageNow == 'rus':
        img_game_over = load_image(r"objects\animated\game-over-rus-obj.png")
        tr_game_over = pygame.transform.scale(img_game_over,
                                              (img_game_over.get_width() * 3, img_game_over.get_height() * 3))
        game_over_obj = AnimatedObject(tr_game_over, 14, 1, windows.width // 2 - 3388 * 3 // 14 // 2,
                                       windows.height // 2 - 180)
    else:
        img_game_over = load_image(r"objects\animated\game-over-eng-obj.png")
        tr_game_over = pygame.transform.scale(img_game_over,
                                              (img_game_over.get_width() * 3, img_game_over.get_height() * 3))
        game_over_obj = AnimatedObject(tr_game_over, 10, 1, windows.width // 2 - 1780 * 3 // 10 // 2,
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
                terminate()

            if event.type == pygame.USEREVENT and event.button == to_lvlmenu_btn:
                running = False
                spriteGroups.animatedObjects.empty()
                transition()
                levels_menu.levels_menu()

            if event.type == pygame.USEREVENT and event.button == repeat_btn:
                running = False
                spriteGroups.animatedObjects.empty()
                transition()
                game.game_def(consts.lvlNow)

            for button in [repeat_btn, to_lvlmenu_btn]:
                button.handle_event(event, consts.volS)

        consts.game_state_field.draw(windows.screen)

        game_over_obj.update_game_over(windows.screen, repeat_btn, to_lvlmenu_btn, consts.languageNow)
        spriteGroups.animatedObjects.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()
