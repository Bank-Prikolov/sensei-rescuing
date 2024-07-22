import pygame

from config import MenuGameConsts, MenuConsts, MenuSprites, WindowsSettings
from items.scenes.dialogue import AnimatedError
from gameplay import level_generating
from misc import terminate, load_image
from managing import boss_theme


def boss_win_cutscene():
    field = AnimatedError(load_image(fr"cutscenes\boss-win\boss-win-field-obj.png"), 2, 1,
                          WindowsSettings.width // 2 - 1290 / 4,
                          WindowsSettings.height // 2 - 448 / 2)
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
                MenuSprites.animatedError.empty()
                boss_theme()

            if event.type == pygame.USEREVENT and event.button == no_btn:
                MenuSprites.animatedError.empty()
                game_over.game_over()

            if event.type == pygame.WINDOWEXPOSED:
                level_generating.rescreen()
                level_generating.updater()

            for button in [yes_btn, no_btn]:
                button.handle_event(event, MenuConsts.volS)

        MenuConsts.backgrBossWin.draw(WindowsSettings.screen)
        field.update()
        MenuSprites.animatedError.draw(WindowsSettings.screen)

        for button in [yes_btn, no_btn]:
            button.check_hover(pygame.mouse.get_pos())
            button.draw(WindowsSettings.screen)

        MenuGameConsts.clock.tick(MenuGameConsts.fps)
        pygame.display.flip()
