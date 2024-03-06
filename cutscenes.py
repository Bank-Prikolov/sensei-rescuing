import pygame
import windows
import consts
import game_over
import spriteGroups
import soundManager
from itemCreator import Button, Object
from processHelper import terminate, load_image
from cutsceneAnimator import AnimatedError


def hleb_greeting_cutscene():
    field = Object(windows.width - 1016, windows.height - 696, 806, 114,
                   r"cutscenes\hleb-greeting\test.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        field.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()


def boss_greeting_cutscene():
    pass


def boss_win_cutscene():
    field = AnimatedError(load_image(fr"cutscenes\boss-win\hero-lose-boss-field-obj.png"), 2, 1,
                          windows.width // 2 - 1290 / 4,
                          windows.height // 2 - 448 / 2)
    yes_btn = Button(field.x + 645 / 2 - 118, field.y + 374, 92, 38,
                     fr"cutscenes\boss-win\default-yes-btn.png",
                     fr"cutscenes\boss-win\hover-yes-btn.png",
                     "",
                     r"data\sounds\revive-sound.mp3")
    no_btn = Button(field.x + 645 / 2 + 20, field.y + 374, 92, 38,
                    fr"cutscenes\boss-win\default-no-btn.png",
                    fr"cutscenes\boss-win\hover-no-btn.png")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.USEREVENT and event.button == yes_btn:
                running = False
                spriteGroups.animatedError.empty()
                soundManager.boss_theme()

            if event.type == pygame.USEREVENT and event.button == no_btn:
                spriteGroups.animatedError.empty()
                game_over.game_over()

            for button in [yes_btn, no_btn]:
                button.handle_event(event, consts.volS)

        consts.backgrBossWin.draw(windows.screen)
        field.update()
        spriteGroups.animatedError.draw(windows.screen)

        for button in [yes_btn, no_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(windows.screen)

        consts.clock.tick(consts.fps)
        pygame.display.flip()


def boss_lose_cutscene():
    pass
